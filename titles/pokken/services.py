from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import DatagramProtocol
from twisted.internet.protocol import Protocol
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from datetime import datetime
import logging
import json

from core.config import CoreConfig
from .config import PokkenConfig
from .base import PokkenBase

class PokkenStunProtocol(DatagramProtocol):
    def __init__(self, cfg: CoreConfig, game_cfg: PokkenConfig, type: str) -> None:
        super().__init__()
        self.core_config = cfg
        self.game_config = game_cfg
        self.logger = logging.getLogger("pokken")
        self.server_type = type

    def datagramReceived(self, data, addr):
        self.logger.debug(
            f"{self.server_type} from from {addr[0]}:{addr[1]} -> {self.transport.getHost().port} - {data.hex()}"
        )
        self.transport.write(data, addr)

# 474554202f20485454502f312e310d0a436f6e6e656374696f6e3a20557067726164650d0a486f73743a207469746c65732e6861793174732e6d653a393030330d0a5365632d576562536f636b65742d4b65793a204f4a6b6d522f376b646d6953326573483548783776413d3d0d0a5365632d576562536f636b65742d56657273696f6e3a2031330d0a557067726164653a20776562736f636b65740d0a557365722d4167656e743a20576562536f636b65742b2b2f302e332e300d0a0d0a
class PokkenAdmissionProtocol(WebSocketServerProtocol):
    def __init__(self, cfg: CoreConfig, game_cfg: PokkenConfig):
        super().__init__()
        self.core_config = cfg
        self.game_config = game_cfg
        self.logger = logging.getLogger("pokken")

        self.base = PokkenBase(cfg, game_cfg)

    def onMessage(self, payload, isBinary: bool) -> None:
        msg = json.loads(payload)
        self.logger.debug(f"WebSocket from from {self.transport.getPeer().host}:{self.transport.getPeer().port} -> {self.transport.getHost().port} - {msg}")
        
        handler = getattr(self.base, f"handle_admission_{msg['api'].lower()}")
        resp = handler(msg, self.transport.getPeer().host)

        if "type" not in resp:
            resp['type'] = "res"
        if "data" not in resp:
            resp['data'] = {}
        if "api" not in resp:
            resp['api'] = msg["api"]
        if "result" not in resp:
            resp['result'] = 'true'
        
        self.logger.debug(f"Websocket response: {resp}")
        self.sendMessage(json.dumps(resp).encode(), isBinary)

# 0001002c2112a442334a0506a62efa71477dcd698022002872655455524e2053796e6320436c69656e7420302e33202d20524643353338392f7475726e2d3132
class PokkenAdmissionFactory(WebSocketServerFactory):
    protocol = PokkenAdmissionProtocol

    def __init__(
        self,
        cfg: CoreConfig,
        game_cfg: PokkenConfig
    ) -> None:
        self.core_config = cfg
        self.game_config = game_cfg
        super().__init__(f"ws://{self.game_config.server.hostname}:{self.game_config.server.port_admission}")
    
    def buildProtocol(self, addr: IAddress) -> Protocol:
        p = self.protocol(self.core_config, self.game_config)
        p.factory = self
        return p
