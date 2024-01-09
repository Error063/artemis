from typing import Tuple, List, Dict
from starlette.requests import Request
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.routing import Route, WebSocketRoute
from starlette.websockets import WebSocket, WebSocketState, WebSocketDisconnect
import ast
from datetime import datetime
import yaml
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
import inflection
from os import path
from google.protobuf.message import DecodeError

from core import CoreConfig, Utils
from core.title import BaseServlet
from .config import PokkenConfig
from .base import PokkenBase
from .const import PokkenConstants
from .proto import jackal_pb2

class PokkenServlet(BaseServlet):
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        super().__init__(core_cfg, cfg_dir)
        self.config_dir = cfg_dir
        self.game_cfg = PokkenConfig()
        if path.exists(f"{cfg_dir}/pokken.yaml"):
            self.game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/pokken.yaml")))

        self.logger = logging.getLogger("pokken")
        if not hasattr(self.logger, "inited"):
            log_fmt_str = "[%(asctime)s] Pokken | %(levelname)s | %(message)s"
            log_fmt = logging.Formatter(log_fmt_str)
            fileHandler = TimedRotatingFileHandler(
                "{0}/{1}.log".format(self.core_cfg.server.log_dir, "pokken"),
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

        self.base = PokkenBase(core_cfg, self.game_cfg)

    @classmethod
    def is_game_enabled(cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str) -> bool:
        game_cfg = PokkenConfig()

        if path.exists(f"{cfg_dir}/{PokkenConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{PokkenConstants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return False
        
        return True
    
    def get_routes(self) -> List[Route]:
        return [
            Route("/pokken/", self.render_POST, methods=['POST']),
            Route("/pokken/matching", self.handle_matching, methods=['POST']),
            WebSocketRoute("/pokken/admission", self.handle_admission)
        ]
    
    def get_allnet_info(self, game_code: str, game_ver: int, keychip: str) -> Tuple[str, str]:
        return (
            f"https://{self.game_cfg.server.hostname}:{Utils.get_title_port_ssl(self.core_cfg)}/pokken/",
            f"{self.game_cfg.server.hostname}:{Utils.get_title_port_ssl(self.core_cfg)}/pokken/",
        )

    def get_mucha_info(self, core_cfg: CoreConfig, cfg_dir: str) -> Tuple[bool, str]:
        if not self.game_cfg.server.enable:
            return (False, [], [])

        return (True, PokkenConstants.GAME_CDS, PokkenConstants.NETID_PREFIX)
    
    async def handle_admission(self, ws: WebSocket) -> None:
        client_ip = Utils.get_ip_addr(ws)
        await ws.accept()
        while True:
            try:
                msg: Dict = await ws.receive_json()
            except WebSocketDisconnect as e:
                self.logger.debug(f"Client {client_ip} disconnected - {e}")
                break
            except Exception as e:                
                self.logger.error(f"Could not load JSON from message from {client_ip} - {e}")
                if ws.client_state != WebSocketState.DISCONNECTED:                    
                    await ws.close()
                break
            
            self.logger.debug(f"Admission: Message from {client_ip}:{ws.client.port} - {msg}")
            
            api = msg.get("api", "noop")
            handler = getattr(self.base, f"handle_admission_{api.lower()}")
            resp = await handler(msg, client_ip)
            
            if resp is None:
                resp = {}

            if "type" not in resp:
                resp['type'] = "res"
            if "data" not in resp:
                resp['data'] = {}
            if "api" not in resp:
                resp['api'] = api
            if "result" not in resp:
                resp['result'] = 'true'
            
            self.logger.debug(f"Websocket response: {resp}")
            try:
                await ws.send_json(resp)
            except WebSocketDisconnect as e:
                self.logger.debug(f"Client {client_ip} disconnected - {e}")
                break
            except Exception as e:                
                self.logger.error(f"Could not send JSON message to {client_ip} - {e}")
                break
        
        if ws.client_state != WebSocketState.DISCONNECTED:                    
            await ws.close()

    async def render_POST(self, request: Request) -> bytes:
        content = await request.body()
        if content == b"":
            self.logger.info("Empty request")
            return b""

        pokken_request = jackal_pb2.Request()
        try:
            pokken_request.ParseFromString(content)
        except DecodeError as e:
            self.logger.warning(f"{e} {content}")
            return b""

        endpoint = jackal_pb2.MessageType.DESCRIPTOR.values_by_number[
            pokken_request.type
        ].name.lower()

        self.logger.debug(pokken_request)

        handler = getattr(self.base, f"handle_{endpoint}", None)
        if handler is None:
            self.logger.warning(f"No handler found for message type {endpoint}")
            return self.base.handle_noop(pokken_request)

        self.logger.info(f"{endpoint} request from {Utils.get_ip_addr(request)}")

        ret = await handler(pokken_request)
        return Response(ret)

    async def handle_matching(self, request: Request) -> bytes:
        if not self.game_cfg.server.enable_matching:
            return Response()
        
        content = await request.body()
        client_ip = Utils.get_ip_addr(request)

        if content is None or content == b"":
            self.logger.info("Empty matching request")
            return JSONResponse(self.base.handle_matching_noop())

        json_content = ast.literal_eval(
            content.decode()
            .replace("null", "None")
            .replace("true", "True")
            .replace("false", "False")
        )
        self.logger.info(f"Matching {json_content['call']} request")
        self.logger.debug(json_content)

        handler = getattr(
            self.base,
            f"handle_matching_{inflection.underscore(json_content['call'])}",
            None,
        )
        if handler is None:
            self.logger.warning(
                f"No handler found for message type {json_content['call']}"
            )
            return JSONResponse(self.base.handle_matching_noop())

        ret = handler(json_content, client_ip)

        if ret is None:
            ret = {}
        if "result" not in ret:
            ret["result"] = "true"
        if "data" not in ret:
            ret["data"] = {}
        if "timestamp" not in ret:
            ret["timestamp"] = int(datetime.now().timestamp() * 1000)

        self.logger.debug(f"Response {ret}")

        return JSONResponse(ret)
