import yaml
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
import logging
import json
from hashlib import md5
from twisted.web.http import Request
from typing import Dict, Tuple
from os import path

from core.config import CoreConfig
from titles.wacca.config import WaccaConfig
from titles.wacca.config import WaccaConfig
from titles.wacca.const import WaccaConstants
from titles.wacca.reverse import WaccaReverse
from titles.wacca.lilyr import WaccaLilyR
from titles.wacca.lily import WaccaLily
from titles.wacca.s import WaccaS
from titles.wacca.base import WaccaBase
from titles.wacca.handlers.base import BaseResponse
from titles.wacca.handlers.helpers import Version

class WaccaServlet():
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = WaccaConfig()
        if path.exists(f"{cfg_dir}/{WaccaConstants.CONFIG_NAME}"):
            self.game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/{WaccaConstants.CONFIG_NAME}")))

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
        fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.core_cfg.server.log_dir, "wacca"), encoding='utf8',
            when="d", backupCount=10)

        fileHandler.setFormatter(log_fmt)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        
        self.logger.setLevel(self.game_cfg.server.loglevel)
        coloredlogs.install(level=self.game_cfg.server.loglevel, logger=self.logger, fmt=log_fmt_str)
    
    @classmethod
    def get_allnet_info(cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str) -> Tuple[bool, str, str]:
        game_cfg = WaccaConfig()
        if path.exists(f"{cfg_dir}/{WaccaConstants.CONFIG_NAME}"):
            game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/{WaccaConstants.CONFIG_NAME}")))

        if not game_cfg.server.enable:
            return (False, "", "")
        
        if core_cfg.server.is_develop:
            return (True, f"http://{core_cfg.title.hostname}:{core_cfg.title.port}/{game_code}/$v", "")
        
        return (True, f"http://{core_cfg.title.hostname}/{game_code}/$v", "")

    def render_POST(self, request: Request, version: int, url_path: str) -> bytes:
        def end(resp: Dict) -> bytes:
            hash = md5(json.dumps(resp, ensure_ascii=False).encode()).digest()
            request.responseHeaders.addRawHeader(b"X-Wacca-Hash", hash.hex().encode())
            return json.dumps(resp).encode()
        
        try:
            req_json = json.loads(request.content.getvalue())
            version_full = Version(req_json["appVersion"])
        except:
            self.logger.error(f"Failed to parse request toi {request.uri} -> {request.content.getvalue()}")
            resp = BaseResponse()
            resp.status = 1
            resp.message = "不正なリクエスト エラーです"
            return end(resp.make())

        url_split = url_path.split("/")
        start_req_idx = url_split.index("api") + 1

        func_to_find = "handle_"
        for x in range(len(url_split) - start_req_idx):
            func_to_find += f"{url_split[x + start_req_idx]}_"
        func_to_find += "request"

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
            self.logger.warning(f"Unsupported version ({req_json['appVersion']}) request {url_path} - {req_json}")
            resp = BaseResponse()
            resp.status = 1
            resp.message = "不正なアプリバージョンエラーです"
            return end(resp.make())
        
        self.logger.info(f"v{req_json['appVersion']} {url_path} request from {request.getClientAddress().host} with chipId {req_json['chipId']}")
        self.logger.debug(req_json)

        if not hasattr(self.versions[internal_ver], func_to_find):
            self.logger.warn(f"{req_json['appVersion']} has no handler for {func_to_find}")
            resp = BaseResponse().make()
            return end(resp)

        try:
            handler = getattr(self.versions[internal_ver], func_to_find)
            resp = handler(req_json)
            
            self.logger.debug(f"{req_json['appVersion']} response {resp}")
            return end(resp)

        except Exception as e:
            self.logger.error(f"{req_json['appVersion']} Error handling method {url_path} -> {e}")
            if self.core_cfg.server.is_develop:
                raise
            
            resp = BaseResponse()
            resp.status = 1
            resp.message = "A server error occoured."
            return end(resp)
