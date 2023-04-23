import struct

from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig

class IDZHandlerUnknown(IDZHandlerBase):
    cmd_codes = [0x00ad, 0x00ad, 0x00a2, 0x00a2]
    name = "unknown"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
