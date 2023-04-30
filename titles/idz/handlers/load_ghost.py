import struct

from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig


class IDZHandlerLoadGhost(IDZHandlerBase):
    cmd_codes = [0x00A0, 0x00A0, 0x0095, 0x0095]
    rsp_codes = [0x00A1, 0x00A1, 0x0096, 0x0096]
    name = "load_ghost"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0070

    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        struct.pack_into("<I", ret, 0x02, 0x5)

        struct.pack_into("<L", ret, 0x04, 0x0)
        struct.pack_into("<l", ret, 0x08, -1)
        struct.pack_into("<L", ret, 0x0C, 0x1D4C0)
        struct.pack_into("<L", ret, 0x10, 0x1D4C0)
        struct.pack_into("<L", ret, 0x14, 0x1D4C0)

        struct.pack_into("<L", ret, 0x38, 0x0)
        struct.pack_into("<l", ret, 0x3C, -1)
        struct.pack_into("<L", ret, 0x40, 0x1D4C0)
        struct.pack_into("<L", ret, 0x44, 0x1D4C0)
        struct.pack_into("<L", ret, 0x48, 0x1D4C0)

        struct.pack_into("<L", ret, 0x4C, 0x1D4C0)
        struct.pack_into("<i", ret, 0x50, -1)
        struct.pack_into("<H", ret, 0x52, 0)
        struct.pack_into("<H", ret, 0x53, 0)
        struct.pack_into("<H", ret, 0x54, 0)
        struct.pack_into("<H", ret, 0x55, 0)
        struct.pack_into("<H", ret, 0x58, 0)
        return ret
