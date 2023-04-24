from twisted.internet.protocol import DatagramProtocol
import logging

from core.config import CoreConfig
from .config import IDZConfig


class IDZEcho(DatagramProtocol):
    def __init__(self, cfg: CoreConfig, game_cfg: IDZConfig) -> None:
        super().__init__()
        self.core_config = cfg
        self.game_config = game_cfg
        self.logger = logging.getLogger("idz")

    def datagramReceived(self, data, addr):
        self.logger.debug(
            f"Echo from from {addr[0]}:{addr[1]} -> {self.transport.getHost().port} - {data.hex()}"
        )
        self.transport.write(data, addr)
