from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse
from starlette.routing import Route
import yaml
import logging
import coloredlogs
from logging.handlers import TimedRotatingFileHandler
from os import path
from typing import Tuple, List, Dict
import importlib
import asyncio

from core.config import CoreConfig
from core.title import BaseServlet
from .config import IDZConfig
from .const import IDZConstants
from .userdb import IDZUserDB, IDZKey
from .echo import IDZEcho


class IDZServlet(BaseServlet):
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        super().__init__(core_cfg, cfg_dir)
        self.game_cfg = IDZConfig()
        if path.exists(f"{cfg_dir}/{IDZConstants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{IDZConstants.CONFIG_NAME}"))
            )

        self.logger = logging.getLogger("idz")
        if not hasattr(self.logger, "inited"):
            log_fmt_str = "[%(asctime)s] IDZ | %(levelname)s | %(message)s"
            log_fmt = logging.Formatter(log_fmt_str)
            fileHandler = TimedRotatingFileHandler(
                "{0}/{1}.log".format(self.core_cfg.server.log_dir, "idz"),
                encoding="utf8",
                when="d",
                backupCount=10,
            )

            self.rsa_keys: List[IDZKey] = []

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

    @classmethod
    def rsaHashKeyN(cls, data):
        hash_ = 0
        for i in data:
            hash_ = (
                hash_ * IDZConstants.HASH_MUL + (i ^ IDZConstants.HASH_XOR)
                ^ IDZConstants.HASH_LUT[i & 0xF]
            )
            hash_ &= 0xFFFFFFFF
        return hash_

    @classmethod
    def is_game_enabled(
        cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str
    ) -> bool:
        game_cfg = IDZConfig()
        if path.exists(f"{cfg_dir}/{IDZConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{IDZConstants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return False

        if len(game_cfg.rsa_keys) <= 0 or not game_cfg.server.aes_key:
            logging.getLogger("idz").error("IDZ: No RSA/AES  keys! IDZ cannot start")
            return False

        return True
    
    def get_routes(self) -> List[Route]:
        return [
            Route("/idz/news/{endpoint:str}", self.render_GET),
            Route("/idz/error", self.render_GET)
        ]
    
    def get_allnet_info(self, game_code: str, game_ver: int, keychip: str) -> Tuple[str, str]:
        hostname = (
            self.core_cfg.server.hostname
            if not self.game_cfg.server.hostname
            else self.game_cfg.server.hostname
        )
        return (
            f"",
            f"{hostname}:{self.game_cfg.ports.userdb}",
        )

    def setup(self):
        for key in self.game_cfg.rsa_keys:
            if "N" not in key or "d" not in key or "e" not in key:
                self.logger.error(f"Invalid IDZ key {key}")
                continue

            hashN = self.rsaHashKeyN(str(key["N"]).encode())
            self.rsa_keys.append(IDZKey(key["N"], key["d"], key["e"], hashN))

        if len(self.rsa_keys) <= 0:
            self.logger.error("No valid RSA keys provided! IDZ cannot start!")
            return

        handler_map = [{} for _ in range(IDZConstants.NUM_VERS)]
        handler_mod = mod = importlib.import_module(f"titles.idz.handlers")

        for cls_name in dir(handler_mod):
            if cls_name.startswith("__"):
                continue

            try:
                mod = getattr(handler_mod, cls_name)
                mod_cmds: List = getattr(mod, "cmd_codes")
                while len(mod_cmds) < IDZConstants.NUM_VERS:
                    mod_cmds.append(None)

                for i in range(len(mod_cmds)):
                    if mod_cmds[i] is None:
                        mod_cmds[i] = mod_cmds[i - 1]

                    handler_map[i][mod_cmds[i]] = mod

            except AttributeError as e:
                continue
        
        loop = asyncio.get_running_loop()
        IDZUserDB(self.core_cfg, self.game_cfg, self.rsa_keys, handler_map)
        asyncio.create_task(
            loop.create_datagram_endpoint(
                lambda: IDZEcho(),
                local_addr=(self.core_cfg.server.listen_address, self.game_cfg.ports.echo)
            )
        )
        asyncio.create_task(
            loop.create_datagram_endpoint(
                lambda: IDZEcho(),
                local_addr=(self.core_cfg.server.listen_address, self.game_cfg.ports.match)
            )
        )
        asyncio.create_task(
            loop.create_datagram_endpoint(
                lambda: IDZEcho(),
                local_addr=(self.core_cfg.server.listen_address, self.game_cfg.ports.userdb + 1)
            )
        )

        self.logger.info(f"UserDB Listening on port {self.game_cfg.ports.userdb}")

    async def render_GET(self, request: Request) -> bytes:
        url_path = request.path_params.get('endpoint', '')
        if not url_path:
            return Response()

        self.logger.info(f"IDZ GET request: {url_path}")

        news = (
            self.game_cfg.server.news
            if self.game_cfg.server.news
            else f"Welcome to Initial D Arcade Stage Zero on {self.core_cfg.server.name}!"
        )
        news += "\r\n"
        news = "1979/01/01 00:00:00 2099/12/31 23:59:59 " + news

        return PlainTextResponse(news, media_type="text/plain; charset=utf-8", headers={"Last-Modified": "Sun, 23 Apr 2023 05:33:20 GMT"})
