import struct

from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig
from ..const import IDZConstants

class IDZHandleUpdateUserLog(IDZHandlerBase):
    cmd_codes = [0x00bd, 0x00bd, 0x00ab, 0x00b3]
    name = "update_user_log"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
    
    def handle(self, data: bytes) -> bytearray:
        ret =  super().handle(data)
        return ret
