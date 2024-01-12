import logging
import socket

from socketserver import BaseRequestHandler, TCPServer
from typing import Tuple

from core.config import CoreConfig
from titles.idac.config import IDACConfig
from titles.idac.database import IDACData


class IDACEchoUDP:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        logging.getLogger('idz').debug(f'Received echo from {addr}')
        self.transport.sendto(data, addr)



class IDACEchoTCP(BaseRequestHandler):
    def __init__(
        self, request, client_address, server, cfg: CoreConfig, game_cfg: IDACConfig
    ) -> None:
        self.core_config = cfg
        self.game_config = game_cfg
        self.logger = logging.getLogger("idac")
        self.data = IDACData(cfg)
        super().__init__(request, client_address, server)

    def handle(self):
        data = self.request.recv(1024).strip()
        self.logger.debug(
            f"TCP Ping from {self.client_address[0]}:{self.client_address[1]} -> {self.server.server_address[1]}: {data.hex()}"
        )
        self.request.sendall(data)
        self.request.shutdown(socket.SHUT_WR)


class IDACEchoTCPFactory(TCPServer):
    def __init__(
        self,
        server_address: Tuple[str, int],
        RequestHandlerClass,
        cfg: CoreConfig,
        game_cfg: IDACConfig,
        bind_and_activate: bool = ...,
    ) -> None:
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.core_config = cfg
        self.game_config = game_cfg

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(
            request, client_address, self, self.core_config, self.game_config
        )
