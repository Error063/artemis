import json
import traceback
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
import yaml
import logging
import coloredlogs
from os import path
from typing import Dict, List, Tuple
from logging.handlers import TimedRotatingFileHandler
import asyncio

from core.config import CoreConfig
from core.title import BaseServlet, JSONResponseNoASCII
from core.utils import Utils
from titles.idac.base import IDACBase
from titles.idac.season2 import IDACSeason2
from titles.idac.config import IDACConfig
from titles.idac.const import IDACConstants
from titles.idac.echo import IDACEchoUDP
from titles.idac.matching import IDACMatching


class IDACServlet(BaseServlet):
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = IDACConfig()
        if path.exists(f"{cfg_dir}/{IDACConstants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{IDACConstants.CONFIG_NAME}"))
            )

        self.versions = [
            IDACBase(core_cfg, self.game_cfg),
            IDACSeason2(core_cfg, self.game_cfg)
        ]

        self.logger = logging.getLogger("idac")
        log_fmt_str = "[%(asctime)s] IDAC | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        fileHandler = TimedRotatingFileHandler(
            "{0}/{1}.log".format(self.core_cfg.server.log_dir, "idac"),
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
    def is_game_enabled(cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str) -> bool:
        game_cfg = IDACConfig()

        if path.exists(f"{cfg_dir}/{IDACConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{IDACConstants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return False
        
        return True
    
    def get_routes(self) -> List[Route]:
        return [
            Route("/{version:int}/initiald/{category:str}/{endpoint:str}", self.render_POST, methods=["POST"]),
            Route("/{version:int}/initiald-matching/{endpoint:str}", self.render_matching, methods=["POST"]),
        ]

    def get_allnet_info(
        self, game_code: str, game_ver: int, keychip: str
    ) -> Tuple[bool, str, str]:
        title_port_int = Utils.get_title_port(self.core_cfg)
        t_port = f":{title_port_int}" if title_port_int and not self.core_cfg.server.is_using_proxy else ""

        return (
            f"",
            # requires http or else it defaults to https
            f"http://{self.core_cfg.server.hostname}{t_port}/{game_ver}/",
        )

    async def render_POST(self, request: Request) -> bytes:
        req_raw = await request.body()
        internal_ver = 0
        version: int = request.path_params.get('version')
        category: str = request.path_params.get('category')
        endpoint: str = request.path_params.get('endpoint')
        client_ip = Utils.get_ip_addr(request)

        if version >= 100 and version < 140:  # IDAC Season 1
            internal_ver = IDACConstants.VER_IDAC_SEASON_1
        elif version >= 140 and version < 171:  # IDAC Season 2
            internal_ver = IDACConstants.VER_IDAC_SEASON_2

        header_application = self.decode_header(request.headers.get("application", ""))

        req_data = json.loads(req_raw)

        self.logger.info(f"v{version} {endpoint} request from {client_ip}")
        self.logger.debug(f"Headers: {header_application}")
        self.logger.debug(req_data)

        # func_to_find = "handle_" + inflection.underscore(endpoint) + "_request"
        func_to_find = "handle_"
        func_to_find += f"{category.lower()}_" if not category == "" else ""
        func_to_find += f"{endpoint.lower()}_request"

        if not hasattr(self.versions[internal_ver], func_to_find):
            self.logger.warning(f"Unhandled v{version} request {endpoint}")
            return JSONResponse('{"status_code": "0"}')

        resp = None
        try:
            handler = getattr(self.versions[internal_ver], func_to_find)
            resp = handler(req_data, header_application)

        except Exception as e:
            traceback.print_exc()
            self.logger.error(f"Error handling v{version} method {endpoint} - {e}")
            return JSONResponse('{"status_code": "0"}')

        if resp is None:
            resp = {"status_code": "0"}

        self.logger.debug(f"Response {resp}")
        return JSONResponseNoASCII(resp)

    async def render_matching(self, request: Request):
        url: str = request.path_params.get("endpoint")
        ver: int = request.path_params.get("version")
        client_ip = Utils.get_ip_addr(request)
        req_data = await request.json()
        header_application = self.decode_header(request.headers.get('application', ''))
        user_id = int(header_application["session"])

        # self.getMatchingStatus(user_id)

        self.logger.info(
            f"IDAC Matching request from {client_ip}: {url} - {req_data}"
        )

        resp = {"status_code": "0"}
        if url == "/regist":
            self.queue = self.queue + 1
        elif url == "/status":
            if req_data.get("cancel_flag"):
                self.queue = self.queue - 1
                self.logger.info(
                    f"IDAC Matching endpoint {client_ip} had quited"
                )

            resp = {
                "status_code": "0",
                # Only IPv4 is supported
                "host": self.game_config.server.matching_host,
                "port": self.game_config.server.matching_p2p,
                "room_name": "INDTA",
                "state": 1,
            }

        self.logger.debug(f"Response {resp}")
        return JSONResponseNoASCII(resp)

    def decode_header(self, app: str) -> Dict:
        ret = {}

        for x in app.split(", "):
            y = x.split("=")
            ret[y[0]] = y[1].replace('"', "")

        return ret

    def setup(self):
        if self.game_cfg.server.enable:
            loop = asyncio.get_running_loop()
            asyncio.create_task(
                loop.create_datagram_endpoint(
                    lambda: IDACEchoUDP(),
                    local_addr=(self.core_cfg.server.listen_address, self.game_cfg.server.echo1)
                )
            )
            
            self.logger.info(f"Matching listening on {self.game_cfg.server.matching} with echo on {self.game_cfg.server.echo1}")
            
