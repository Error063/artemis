import struct

from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig

class IDZHandlerSaveProfile(IDZHandlerBase):
    cmd_codes = [0x0068, 0x0138, 0x0138, 0x0143]
    name = "save_profile"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)
