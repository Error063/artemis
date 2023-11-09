from typing import Tuple, Dict, List
from twisted.web.http import Request
import yaml
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
from os import path
from Crypto.Cipher import Blowfish

from core import CoreConfig, Utils
from core.title import BaseServlet
from titles.sao.config import SaoConfig
from titles.sao.const import SaoConstants
from titles.sao.base import SaoBase
from titles.sao.handlers.base import *


class SaoServlet(BaseServlet):
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        super().__init__(core_cfg, cfg_dir)
        self.config_dir = cfg_dir
        self.game_cfg = SaoConfig()
        if path.exists(f"{cfg_dir}/sao.yaml"):
            self.game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/sao.yaml")))

        self.logger = logging.getLogger("sao")
        if not hasattr(self.logger, "inited"):
            log_fmt_str = "[%(asctime)s] SAO | %(levelname)s | %(message)s"
            log_fmt = logging.Formatter(log_fmt_str)
            fileHandler = TimedRotatingFileHandler(
                "{0}/{1}.log".format(self.core_cfg.server.log_dir, "sao"),
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

        self.base = SaoBase(core_cfg, self.game_cfg)
    
    def get_endpoint_matchers(self) -> Tuple[List[Tuple[str, str, Dict]], List[Tuple[str, str, Dict]]]:
        return (
            [], 
            [("render_POST", "/{datecode}/proto/if/{category}/{endpoint}", {})]
        )
    
    @classmethod
    def is_game_enabled(cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str) -> bool:
        game_cfg = SaoConfig()

        if path.exists(f"{cfg_dir}/{SaoConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{SaoConstants.CONFIG_NAME}"))
            )
    
        if not game_cfg.server.enable:
            return False
        
        return True
    
    def get_allnet_info(self, game_code: str, game_ver: int, keychip: str) -> Tuple[str, str]:
        tport = Utils.get_title_port(self.core_cfg)
        return (
            f"http://{self.core_cfg.title.hostname}:{tport}/",
            f"{self.core_cfg.title.hostname}/",
        )

    def get_mucha_info(self, core_cfg: CoreConfig, cfg_dir: str) -> Tuple[bool, str]:
        if not self.game_cfg.server.enable:
            return (False, "")

        return (True, "SAO1")


    def render_POST(self, request: Request, game_code: str, matchers: Dict) -> bytes:
        endpoint = matchers.get('endpoint', '')
        request.responseHeaders.addRawHeader(b"content-type", b"text/html; charset=utf-8")

        sao_request = request.content.getvalue().hex()

        handler = getattr(self.base, f"handle_{sao_request[:4]}", None)
        if handler is None:
            self.logger.info(f"Generic Handler for {endpoint} - {sao_request[:4]}")
            self.logger.debug(f"Request: {request.content.getvalue().hex()}")
            resp = SaoNoopResponse(int.from_bytes(bytes.fromhex(sao_request[:4]), "big")+1)
            self.logger.debug(f"Response: {resp.make().hex()}")
            return resp.make()

        self.logger.info(f"Handler {endpoint} - {sao_request[:4]} request")
        self.logger.debug(f"Request: {request.content.getvalue().hex()}")
        resp = handler(sao_request)
        self.logger.debug(f"Response: {resp.hex()}")
        return resp