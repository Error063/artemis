from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Protocol
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from autobahn.websocket.types import ConnectionRequest
from typing import Dict
import logging
import json

from core.config import CoreConfig
from .config import PokkenConfig
from .base import PokkenBase

class PokkenAdmissionProtocol(WebSocketServerProtocol):
    def __init__(self, cfg: CoreConfig, game_cfg: PokkenConfig):
        super().__init__()
        self.core_config = cfg
        self.game_config = game_cfg
        self.logger = logging.getLogger("pokken")

        self.base = PokkenBase(cfg, game_cfg)
    
    def onConnect(self, request: ConnectionRequest) -> None:
        self.logger.debug(f"Admission: Connection from {request.peer}")
    
    def onClose(self, wasClean: bool, code: int, reason: str) -> None:
        self.logger.debug(f"Admission: Connection with {self.transport.getPeer().host} closed {'cleanly ' if wasClean else ''}with code {code} - {reason}")

    def onMessage(self, payload, isBinary: bool) -> None:
        msg: Dict = json.loads(payload)
        self.logger.debug(f"Admission: Message from {self.transport.getPeer().host}:{self.transport.getPeer().port} - {msg}")
        
        api = msg.get("api", "noop")
        handler = getattr(self.base, f"handle_admission_{api.lower()}")
        resp = handler(msg, self.transport.getPeer().host)
        
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
        self.sendMessage(json.dumps(resp).encode(), isBinary)

class PokkenAdmissionFactory(WebSocketServerFactory):
    protocol = PokkenAdmissionProtocol

    def __init__(
        self,
        cfg: CoreConfig,
        game_cfg: PokkenConfig
    ) -> None:
        self.core_config = cfg
        self.game_config = game_cfg
        super().__init__(f"ws://{self.game_config.server.hostname}:{self.game_config.ports.admission}")
    
    def buildProtocol(self, addr: IAddress) -> Protocol:
        p = self.protocol(self.core_config, self.game_config)
        p.factory = self
        return p
