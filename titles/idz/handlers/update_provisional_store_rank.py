import struct

from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig

class IDZHandlerUpdateProvisionalStoreRank(IDZHandlerBase):
    cmd_codes = [0x0082, 0x0082, 0x007C, 0x007C]
    rsp_codes = [0x0083, 0x0083, 0x007D, 0x007D]
    name = "update_provisional_store_ranking"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x02b0
    
    def handle(self, data: bytes) -> bytearray:
        return  super().handle(data)
    
    def handle_common(cls, aime_id: int, ret: bytearray) -> bytearray:
        pass
