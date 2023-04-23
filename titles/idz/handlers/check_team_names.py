import struct

from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig

class IDZHandlerCheckTeamName(IDZHandlerBase):
    cmd_codes = [0x00a2, 0x00a2, 0x0097, 0x0097]
    rsp_codes = [0x00a3, 0x00a3, 0x0098, 0x0098]
    name = "check_team_name"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0010
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        struct.pack_into("<I", ret, 0x4, 0x1)
        return data
