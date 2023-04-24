import logging
import struct
from core.data import Data
from core.config import CoreConfig
from ..config import IDZConfig
from ..const import IDZConstants


class IDZHandlerBase:
    name = "generic"
    cmd_codes = [0x0000] * IDZConstants.NUM_VERS
    rsp_codes = [0x0001] * IDZConstants.NUM_VERS

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        self.core_config = core_cfg
        self.game_cfg = game_cfg
        self.data = Data(core_cfg)
        self.logger = logging.getLogger("idz")
        self.game = IDZConstants.GAME_CODE
        self.version = version
        self.size = 0x30

    def handle(self, data: bytes) -> bytearray:
        ret = bytearray([0] * self.size)
        struct.pack_into("<H", ret, 0x0, self.rsp_codes[self.version])
        return ret
