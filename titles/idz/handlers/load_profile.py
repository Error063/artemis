import struct

from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig
from ..const import IDZConstants

class IDZHandlerLoadProfile(IDZHandlerBase):
    cmd_codes = [0x0067, 0x012f, 0x012f, 0x0142]
    rsp_codes = [0x0065, 0x012e, 0x012e, 0x0141]
    name = "load_profile"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)

        if self.version == IDZConstants.VER_IDZ_110:
            self.size = 0x0d30
        elif self.version == IDZConstants.VER_IDZ_130:
            self.size = 0x0ea0
        elif self.version == IDZConstants.VER_IDZ_210:
            self.size = 0x1360
        elif self.version == IDZConstants.VER_IDZ_230:
            self.size = 0x1640
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        aime_id = struct.unpack_from("<L", data, 0x04)[0]
        return ret
