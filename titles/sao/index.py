from typing import Tuple
from twisted.web.http import Request
from twisted.web import resource
import json, ast
from datetime import datetime
import yaml
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
import inflection
from os import path

from core import CoreConfig, Utils
from titles.sao.config import SaoConfig
from titles.sao.const import SaoConstants
from titles.sao.base import SaoBase
from titles.sao.handlers.base import *


class SaoServlet(resource.Resource):
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        self.isLeaf = True
        self.core_cfg = core_cfg
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

    @classmethod
    def get_allnet_info(
        cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str
    ) -> Tuple[bool, str, str]:
        game_cfg = SaoConfig()

        if path.exists(f"{cfg_dir}/{SaoConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{SaoConstants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return (False, "", "")

        return (
            True,
            f"http://{game_cfg.server.hostname}:{game_cfg.server.port}/{game_code}/$v/",
            f"{game_cfg.server.hostname}/SDEW/$v/",
        )

    @classmethod
    def get_mucha_info(
        cls, core_cfg: CoreConfig, cfg_dir: str
    ) -> Tuple[bool, str, str]:
        game_cfg = SaoConfig()

        if path.exists(f"{cfg_dir}/{SaoConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{SaoConstants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return (False, "")

        return (True, "SAO1")

    def setup(self) -> None:
        pass

    def render_POST(
        self, request: Request, version: int = 0, endpoints: str = ""
    ) -> bytes:
        req_url = request.uri.decode()
        if req_url == "/matching":
            self.logger.info("Matching request")

        request.responseHeaders.addRawHeader(b"content-type", b"text/html; charset=utf-8")

        sao_request = request.content.getvalue().hex()
        #sao_request = sao_request[:32]

        handler = getattr(self.base, f"handle_{sao_request[:4]}", None)
        if handler is None:
            self.logger.info(f"Generic Handler for {req_url} - {sao_request[:4]}")
            #self.logger.debug(f"Request: {request.content.getvalue().hex()}")
            resp = SaoNoopResponse(int.from_bytes(bytes.fromhex(sao_request[:4]), "big")+1)
            self.logger.debug(f"Response: {resp.make().hex()}")
            return resp.make()

        self.logger.info(f"Handler {req_url} - {sao_request[:4]} request")
        self.logger.debug(f"Request: {request.content.getvalue().hex()}")
        self.logger.debug(f"Response: {handler(sao_request).hex()}")
        return handler(sao_request)