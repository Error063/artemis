import struct

from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig
from ..const import IDZConstants


class IDZHandlerLoad2on2A(IDZHandlerBase):
    cmd_codes = [0x00B0, 0x00B0, 0x00A3, 0x00A3]
    rsp_codes = [0x00B1, 0x00B1, 0x00A4, 0x00A4]
    name = "load_2on2A"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x04C0

        if version >= IDZConstants.VER_IDZ_210:
            self.size = 0x1290

    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)


class IDZHandlerLoad2on2B(IDZHandlerBase):
    cmd_codes = [0x0132] * 4
    rsp_codes = [0x0133] * 4
    name = "load_2on2B"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x04C0

        if version >= IDZConstants.VER_IDZ_210:
            self.size = 0x0540

    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)
