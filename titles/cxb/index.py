from twisted.web.http import Request
import traceback
import sys
import yaml
import json
import re
import inflection
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
from typing import Dict, Tuple, List
from os import path

from core.config import CoreConfig
from core.title import BaseServlet
from core.utils import Utils
from .config import CxbConfig
from .const import CxbConstants
from .rev import CxbRev
from .rss1 import CxbRevSunriseS1
from .rss2 import CxbRevSunriseS2


class CxbServlet(BaseServlet):
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        self.isLeaf = True
        self.cfg_dir = cfg_dir
        self.core_cfg = core_cfg
        self.game_cfg = CxbConfig()
        if path.exists(f"{cfg_dir}/{CxbConstants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{CxbConstants.CONFIG_NAME}"))
            )

        self.logger = logging.getLogger("cxb")
        if not hasattr(self.logger, "inited"):
            log_fmt_str = "[%(asctime)s] CXB | %(levelname)s | %(message)s"
            log_fmt = logging.Formatter(log_fmt_str)
            fileHandler = TimedRotatingFileHandler(
                "{0}/{1}.log".format(self.core_cfg.server.log_dir, "cxb"),
                encoding="utf8",
                when="d",
                backupCount=10,
            )

            fileHandler.setFormatter(log_fmt)

            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(log_fmt)

            self.logger.addHandler(fileHandler)
            self.logger.addHandler(consoleHandler)

            self.logger.setLevel(self.game_cfg.server.loglevel)
            coloredlogs.install(
                level=self.game_cfg.server.loglevel, logger=self.logger, fmt=log_fmt_str
            )
            self.logger.inited = True

        self.versions = [
            CxbRev(core_cfg, self.game_cfg),
            CxbRevSunriseS1(core_cfg, self.game_cfg),
            CxbRevSunriseS2(core_cfg, self.game_cfg),
        ]

    @classmethod
    def is_game_enabled(cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str) -> bool:
        game_cfg = CxbConfig()
        if path.exists(f"{cfg_dir}/{CxbConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{CxbConstants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return False
        
        return True
    
    def get_allnet_info(self, game_code: str, game_ver: int, keychip: str) -> Tuple[str, str]:
        if not self.core_cfg.server.is_using_proxy and Utils.get_title_port_ssl(self.core_cfg):
            return (
                f"https://{self.core_cfg.title.hostname}:{self.core_cfg.title.port_ssl}",
                "",
            )

        return (f"https://{self.core_cfg.title.hostname}", "")
    
    def get_endpoint_matchers(self) -> Tuple[List[Tuple[str, str, Dict]], List[Tuple[str, str, Dict]]]:
        return (
            [], 
            [
                ("handle_data", "/data", {}),
                ("handle_action", "/action", {}),
                ("handle_action", "/v2/action", {}),
                ("handle_auth", "/auth", {}),
            ]
        )

    def preprocess(self, req: Request) -> Dict:
        try:
            req_bytes = req.content.getvalue()
        except:
            req_bytes = req.content.read() # Can we just use this one?
        
        try:
            req_json: Dict = json.loads(req_bytes)

        except Exception as e:
            try:
                req_json: Dict = json.loads(
                    req_bytes.decode().replace('"', '\\"').replace("'", '"')
                )

            except Exception as f:
                self.logger.warning(
                    f"Error decoding json to /data endpoint: {e} / {f} - {req_bytes}"
                )
                return b""
        
        return req_json

    def handle_data(self, request: Request, game_code: str, matchers: Dict) -> bytes:
        req_json = self.preprocess(request)
        func_to_find = "handle_data_"
        version_string = "Base"
        internal_ver = 0
        version = 0
        
        if req_json == {}:
            self.logger.warning(f"Empty json request to /data")
            return b""

        subcmd = list(req_json.keys())[0]
        if subcmd == "dldate":
        
            if (
                not type(req_json["dldate"]) is dict
                or "filetype" not in req_json["dldate"]
            ):
                self.logger.warning(f"Malformed dldate request: {req_json}")
                return b""

            filetype = req_json["dldate"]["filetype"]
            filetype_split = filetype.split("/")

            if len(filetype_split) < 2 or not filetype_split[0].isnumeric():
                self.logger.warning(f"Malformed dldate request: {req_json}")
                return b""

            version = int(filetype_split[0])
            filename = filetype_split[len(filetype_split) - 1]

            match = re.match(
                "^([A-Za-z]*)(\d\d\d\d)$", filetype_split[len(filetype_split) - 1]
            )
            if match:
                func_to_find += f"{inflection.underscore(match.group(1))}xxxx"
            else:
                func_to_find += f"{inflection.underscore(filename)}"
        else:
            filetype = subcmd
            func_to_find += filetype
        
        func_to_find += "_request"
        
        if version <= 10102:
            version_string = "Rev"
            internal_ver = CxbConstants.VER_CROSSBEATS_REV

        elif version == 10113 or version == 10103:
            version_string = "Rev SunriseS1"
            internal_ver = CxbConstants.VER_CROSSBEATS_REV_SUNRISE_S1

        elif version >= 10114 or version == 10104:
            version_string = "Rev SunriseS2"
            internal_ver = CxbConstants.VER_CROSSBEATS_REV_SUNRISE_S2

        if not hasattr(self.versions[internal_ver], func_to_find):
            self.logger.warn(f"{version_string} has no handler for filetype {filetype}")
            return ""
        
        self.logger.info(f"{version_string} request for filetype {filetype}")
        self.logger.debug(req_json)

        handler = getattr(self.versions[internal_ver], func_to_find)
        
        try:
            resp = handler(req_json)

        except Exception as e:
            self.logger.error(f"Error handling request for file {filetype} - {e}")
            if self.logger.level == logging.DEBUG:
                tp, val, tb  = sys.exc_info()
                traceback.print_exception(tp, val, tb, limit=1)
                with open("{0}/{1}.log".format(self.core_cfg.server.log_dir, "cxb"), "a") as f:
                    traceback.print_exception(tp, val, tb, limit=1, file=f)
            return ""
        
        self.logger.debug(f"{version_string} Response {resp}")
        return json.dumps(resp, ensure_ascii=False).encode("utf-8")

    def handle_action(self, request: Request, game_code: str, matchers: Dict) -> bytes:
        req_json = self.preprocess(request)
        subcmd = list(req_json.keys())[0]
        func_to_find = f"handle_action_{subcmd}_request"
        
        if not hasattr(self.versions[0], func_to_find):
            self.logger.warn(f"No handler for action {subcmd} request")
            return ""
        
        self.logger.info(f"Action {subcmd} Request")
        self.logger.debug(req_json)

        handler = getattr(self.versions[0], func_to_find)
        
        try:
            resp = handler(req_json)

        except Exception as e:
            self.logger.error(f"Error handling action {subcmd} request - {e}")
            if self.logger.level == logging.DEBUG:
                tp, val, tb  = sys.exc_info()
                traceback.print_exception(tp, val, tb, limit=1)
                with open("{0}/{1}.log".format(self.core_cfg.server.log_dir, "cxb"), "a") as f:
                    traceback.print_exception(tp, val, tb, limit=1, file=f)
            return ""
        
        self.logger.debug(f"Response {resp}")
        return json.dumps(resp, ensure_ascii=False).encode("utf-8")

    def handle_auth(self, request: Request, game_code: str, matchers: Dict) -> bytes:
        req_json = self.preprocess(request)
        subcmd = list(req_json.keys())[0]
        func_to_find = f"handle_auth_{subcmd}_request"
        
        if not hasattr(self.versions[0], func_to_find):
            self.logger.warn(f"No handler for auth {subcmd} request")
            return ""
        
        self.logger.info(f"Action {subcmd} Request")
        self.logger.debug(req_json)

        handler = getattr(self.versions[0], func_to_find)
        
        try:
            resp = handler(req_json)

        except Exception as e:
            self.logger.error(f"Error handling auth {subcmd} request - {e}")
            if self.logger.level == logging.DEBUG:
                tp, val, tb  = sys.exc_info()
                traceback.print_exception(tp, val, tb, limit=1)
                with open("{0}/{1}.log".format(self.core_cfg.server.log_dir, "cxb"), "a") as f:
                    traceback.print_exception(tp, val, tb, limit=1, file=f)
            return ""
        
        self.logger.debug(f"Response {resp}")
        return json.dumps(resp, ensure_ascii=False).encode("utf-8")
