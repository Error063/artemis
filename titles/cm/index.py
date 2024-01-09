import json
import inflection
import yaml
import string
import logging
import coloredlogs
import zlib
from starlette.routing import Route
from starlette.responses import Response
from starlette.requests import Request
from os import path
from typing import List
from logging.handlers import TimedRotatingFileHandler

from core.config import CoreConfig
from core.utils import Utils
from core.title import BaseServlet
from .config import CardMakerConfig
from .const import CardMakerConstants
from .base import CardMakerBase
from .cm135 import CardMaker135

class CardMakerServlet(BaseServlet):
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        super().__init__(core_cfg, cfg_dir)
        self.game_cfg = CardMakerConfig()
        if path.exists(f"{cfg_dir}/{CardMakerConstants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{CardMakerConstants.CONFIG_NAME}"))
            )

        self.versions = [
            CardMakerBase(core_cfg, self.game_cfg),
            CardMaker135(core_cfg, self.game_cfg)
        ]

        self.logger = logging.getLogger("cardmaker")
        log_fmt_str = "[%(asctime)s] Card Maker | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        fileHandler = TimedRotatingFileHandler(
            "{0}/{1}.log".format(self.core_cfg.server.log_dir, "cardmaker"),
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
    
    @classmethod
    def is_game_enabled(
        cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str
    ) -> bool:
        game_cfg = CardMakerConfig()
        if path.exists(f"{cfg_dir}/{CardMakerConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{CardMakerConstants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return False

        return True
    
    def get_routes(self) -> List[Route]:
        return [
            Route("/SDED/{version:int}/{endpoint:str}", self.render_POST)
        ]
    
    async def render_POST(self, request: Request) -> bytes:
        version: int = request.path_params.get('version')
        endpoint: str = request.path_params.get('endpoint')
        req_raw = await request.body()
        internal_ver = 0
        client_ip = Utils.get_ip_addr(request)

        if version >= 130 and version < 135:  # Card Maker
            internal_ver = CardMakerConstants.VER_CARD_MAKER
        elif version >= 135 and version < 140:  # Card Maker 1.35
            internal_ver = CardMakerConstants.VER_CARD_MAKER_135

        if all(c in string.hexdigits for c in endpoint) and len(endpoint) == 32:
            # If we get a 32 character long hex string, it's a hash and we're
            # doing encrypted. The likelyhood of false positives is low but
            # technically not 0
            self.logger.error("Encryption not supported at this time")

        try:
            unzip = zlib.decompress(req_raw)

        except zlib.error as e:
            self.logger.error(
                f"Failed to decompress v{version} {endpoint} request -> {e}"
            )
            return Response(zlib.compress(b'{"stat": "0"}'))

        req_data = json.loads(unzip)

        self.logger.info(f"v{version} {endpoint} request from {client_ip}")
        self.logger.debug(req_data)

        func_to_find = "handle_" + inflection.underscore(endpoint) + "_request"

        if not hasattr(self.versions[internal_ver], func_to_find):
            self.logger.warning(f"Unhandled v{version} request {endpoint}")
            return Response(zlib.compress(b'{"returnCode": 1}'))

        try:
            handler = getattr(self.versions[internal_ver], func_to_find)
            resp = handler(req_data)

        except Exception as e:
            self.logger.error(f"Error handling v{version} method {endpoint} - {e}")
            raise
            return Response(zlib.compress(b'{"stat": "0"}'))

        if resp is None:
            resp = {"returnCode": 1}

        self.logger.debug(f"Response {resp}")

        return Response(zlib.compress(json.dumps(resp, ensure_ascii=False).encode("utf-8")))
