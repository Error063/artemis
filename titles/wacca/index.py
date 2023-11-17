import yaml
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
import logging
import json
from hashlib import md5
from twisted.web.http import Request
from typing import Dict, Tuple, List
from os import path

from core import CoreConfig, Utils
from .config import WaccaConfig
from .config import WaccaConfig
from .const import WaccaConstants
from .reverse import WaccaReverse
from .lilyr import WaccaLilyR
from .lily import WaccaLily
from .s import WaccaS
from .base import WaccaBase
from .handlers.base import BaseResponse
from .handlers.helpers import Version


class WaccaServlet:
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = WaccaConfig()
        if path.exists(f"{cfg_dir}/{WaccaConstants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{WaccaConstants.CONFIG_NAME}"))
            )

        self.versions = [
            WaccaBase(core_cfg, self.game_cfg),
            WaccaS(core_cfg, self.game_cfg),
            WaccaLily(core_cfg, self.game_cfg),
            WaccaLilyR(core_cfg, self.game_cfg),
            WaccaReverse(core_cfg, self.game_cfg),
        ]

        self.logger = logging.getLogger("wacca")
        log_fmt_str = "[%(asctime)s] Wacca | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        fileHandler = TimedRotatingFileHandler(
            "{0}/{1}.log".format(self.core_cfg.server.log_dir, "wacca"),
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

    def get_endpoint_matchers(self) -> Tuple[List[Tuple[str, str, Dict]], List[Tuple[str, str, Dict]]]:
        return (
            [], 
            [
                ("render_POST", "/WaccaServlet/api/{api}/{endpoint}", {}),
                ("render_POST", "/WaccaServlet/api/{api}/{branch}/{endpoint}", {})
            ]
        )

    @classmethod
    def is_game_enabled(cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str) -> bool:
        game_cfg = WaccaConfig()
        if path.exists(f"{cfg_dir}/{WaccaConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{WaccaConstants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return False

        return True
    
    def get_allnet_info(self, game_code: str, game_ver: int, keychip: str) -> Tuple[str, str]:
        if not self.core_cfg.server.is_using_proxy and Utils.get_title_port(self.core_cfg) != 80:
            return (
                f"http://{self.core_cfg.title.hostname}:{Utils.get_title_port(self.core_cfg)}/WaccaServlet",
                "",
            )

        return (f"http://{self.core_cfg.title.hostname}/WaccaServlet", "")
    
    def render_POST(self, request: Request, game_code: str, matchers: Dict) -> bytes:
        def end(resp: Dict) -> bytes:
            hash = md5(json.dumps(resp, ensure_ascii=False).encode()).digest()
            request.responseHeaders.addRawHeader(b"X-Wacca-Hash", hash.hex().encode())
            return json.dumps(resp).encode()

        api = matchers['api']
        branch = matchers.get('branch', '')
        endpoint = matchers['endpoint']
        client_ip = Utils.get_ip_addr(request)
        
        if branch:
            url_path = f"{api}/{branch}/{endpoint}"
            func_to_find = f"handle_{api}_{branch}_{endpoint}_request"

        else:
            url_path = f"{api}/{endpoint}"
            func_to_find = f"handle_{api}_{endpoint}_request"

        try:
            req_json = json.loads(request.content.getvalue())
            version_full = Version(req_json["appVersion"])
        
        except Exception:
            self.logger.error(
                f"Failed to parse request to {url_path} -> {request.content.getvalue()}"
            )
            resp = BaseResponse()
            resp.status = 1
            resp.message = "不正なリクエスト エラーです"
            return end(resp.make())

        ver_search = int(version_full)

        if ver_search < 15000:
            internal_ver = WaccaConstants.VER_WACCA

        elif ver_search >= 15000 and ver_search < 20000:
            internal_ver = WaccaConstants.VER_WACCA_S

        elif ver_search >= 20000 and ver_search < 25000:
            internal_ver = WaccaConstants.VER_WACCA_LILY

        elif ver_search >= 25000 and ver_search < 30000:
            internal_ver = WaccaConstants.VER_WACCA_LILY_R

        elif ver_search >= 30000:
            internal_ver = WaccaConstants.VER_WACCA_REVERSE

        else:
            self.logger.warning(
                f"Unsupported version ({req_json['appVersion']}) request {url_path} - {req_json}"
            )
            resp = BaseResponse()
            resp.status = 1
            resp.message = "不正なアプリバージョンエラーです"
            return end(resp.make())

        self.logger.info(
            f"v{req_json['appVersion']} {url_path} request from {client_ip} with chipId {req_json['chipId']}"
        )
        self.logger.debug(req_json)

        if not hasattr(self.versions[internal_ver], func_to_find):
            self.logger.warning(
                f"{req_json['appVersion']} has no handler for {func_to_find}"
            )
            resp = BaseResponse().make()
            return end(resp)

        try:
            handler = getattr(self.versions[internal_ver], func_to_find)
            resp = handler(req_json)

            self.logger.debug(f"{req_json['appVersion']} response {resp}")
            return end(resp)

        except Exception as e:
            self.logger.error(
                f"{req_json['appVersion']} Error handling method {url_path} -> {e}"
            )
            if self.core_cfg.server.is_develop:
                raise

            resp = BaseResponse()
            resp.status = 1
            resp.message = "A server error occoured."
            return end(resp.make())
