from twisted.internet.protocol import DatagramProtocol
import logging

from core.config import CoreConfig
from .config import IDZConfig

class IDZEcho:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        logging.getLogger('idz').debug(f'Received echo from {addr}')
        self.transport.sendto(data, addr)
