import struct

from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig
from ..const import IDZConstants

class IDZHandlerUpdateStoryClearNum(IDZHandlerBase):
    cmd_codes = [0x007f, 0x097f, 0x013d, 0x0144]
    rsp_codes = [0x0080, 0x013e, 0x013e, 0x0145]
    name = "update_story_clear_num"
    
    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)

        if self.version == IDZConstants.VER_IDZ_110:
            self.size = 0x0220
        elif self.version == IDZConstants.VER_IDZ_130:
            self.size = 0x04f0
        elif self.version == IDZConstants.VER_IDZ_210:
            self.size = 0x0510
        elif self.version == IDZConstants.VER_IDZ_230:
            self.size = 0x0800
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)
