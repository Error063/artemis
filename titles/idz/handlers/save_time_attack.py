import struct

from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig
from ..const import IDZConstants

class IDZHandlerSaveTimeAttack(IDZHandlerBase):
    cmd_codes = [0x00CD, 0x0136, 0x0136, 0x0136]
    rsp_codes = [0x00ce, 0x00ce, 0x00cd, 0x00cd]
    name = "save_time_attack"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x00b0

        if self.version > IDZConstants.VER_IDZ_130:
            self.size = 0x00f0
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        return ret