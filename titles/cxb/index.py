from twisted.web.http import Request
from twisted.web import resource, server
from twisted.internet import reactor, endpoints
import yaml
import json
import re
import inflection
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
from typing import Dict, Tuple
from os import path

from core.config import CoreConfig
from titles.cxb.config import CxbConfig
from titles.cxb.const import CxbConstants
from titles.cxb.rev import CxbRev
from titles.cxb.rss1 import CxbRevSunriseS1
from titles.cxb.rss2 import CxbRevSunriseS2


class CxbServlet(resource.Resource):
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
    def get_allnet_info(
        cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str
    ) -> Tuple[bool, str, str]:
        game_cfg = CxbConfig()
        if path.exists(f"{cfg_dir}/{CxbConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{CxbConstants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return (False, "", "")

        if core_cfg.server.is_develop:
            return (
                True,
                f"http://{core_cfg.title.hostname}:{core_cfg.title.port}/{game_code}/$v/",
                "",
            )

        return (True, f"http://{core_cfg.title.hostname}/{game_code}/$v/", "")

    def setup(self):
        if self.game_cfg.server.enable:
            endpoints.serverFromString(
                reactor,
                f"tcp:{self.game_cfg.server.port}:interface={self.core_cfg.server.listen_address}",
            ).listen(server.Site(CxbServlet(self.core_cfg, self.cfg_dir)))

            if self.core_cfg.server.is_develop and self.game_cfg.server.ssl_enable:
                endpoints.serverFromString(
                    reactor,
                    f"ssl:{self.game_cfg.server.port_secure}"
                    f":interface={self.core_cfg.server.listen_address}:privateKey={self.game_cfg.server.ssl_key}:"
                    f"certKey={self.game_cfg.server.ssl_cert}",
                ).listen(server.Site(CxbServlet(self.core_cfg, self.cfg_dir)))

                self.logger.info(
                    f"Ready on ports {self.game_cfg.server.port} & {self.game_cfg.server.port_secure}"
                )
            else:
                self.logger.info(
                    f"Ready on port {self.game_cfg.server.port}"
                )

    def render_POST(self, request: Request):
        version = 0
        internal_ver = 0
        func_to_find = ""
        cmd = ""
        subcmd = ""
        req_url = request.uri.decode()
        url_split = req_url.split("/")
        req_bytes = request.content.getvalue()

        try:
            req_json: Dict = json.loads(req_bytes)

        except Exception as e:
            try:
                req_json: Dict = json.loads(
                    req_bytes.decode().replace('"', '\\"').replace("'", '"')
                )

            except Exception as f:
                self.logger.warn(
                    f"Error decoding json: {e} / {f} - {req_url} - {req_bytes}"
                )
                return b""

        if req_json == {}:
            self.logger.warn(f"Empty json request to {req_url}")
            return b""

        cmd = url_split[len(url_split) - 1]
        subcmd = list(req_json.keys())[0]

        if subcmd == "dldate":
            if (
                not type(req_json["dldate"]) is dict
                or "filetype" not in req_json["dldate"]
            ):
                self.logger.warn(f"Malformed dldate request: {req_url} {req_json}")
                return b""

            filetype = req_json["dldate"]["filetype"]
            filetype_split = filetype.split("/")
            version = int(filetype_split[0])
            filetype_inflect_split = inflection.underscore(filetype).split("/")

            match = re.match(
                "^([A-Za-z]*)(\d\d\d\d)$", filetype_split[len(filetype_split) - 1]
            )
            if match:
                subcmd = f"{inflection.underscore(match.group(1))}xxxx"
            else:
                subcmd = f"{filetype_inflect_split[len(filetype_inflect_split) - 1]}"
        else:
            filetype = subcmd

        func_to_find = f"handle_{cmd}_{subcmd}_request"

        if version <= 10102:
            version_string = "Rev"
            internal_ver = CxbConstants.VER_CROSSBEATS_REV

        elif version == 10113 or version == 10103:
            version_string = "Rev SunriseS1"
            internal_ver = CxbConstants.VER_CROSSBEATS_REV_SUNRISE_S1

        elif version >= 10114 or version == 10104:
            version_string = "Rev SunriseS2"
            internal_ver = CxbConstants.VER_CROSSBEATS_REV_SUNRISE_S2

        else:
            version_string = "Base"

        self.logger.info(f"{version_string} Request {req_url} -> {filetype}")
        self.logger.debug(req_json)

        try:
            handler = getattr(self.versions[internal_ver], func_to_find)
            resp = handler(req_json)

        except AttributeError as e:
            self.logger.warning(f"Unhandled {version_string} request {req_url} - {e}")
            resp = {}

        except Exception as e:
            self.logger.error(f"Error handling {version_string} method {req_url} - {e}")
            raise

        self.logger.debug(f"{version_string} Response {resp}")
        return json.dumps(resp, ensure_ascii=False).encode("utf-8")
