import struct

from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig

class IDZHandlerLoadRewardTable(IDZHandlerBase):
    cmd_codes = [0x0086, 0x0086, 0x007F, 0x007F]
    rsp_codes = [0x0087, 0x0087, 0x0080, 0x0080]
    name = "load_reward_table"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x01c0
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)
