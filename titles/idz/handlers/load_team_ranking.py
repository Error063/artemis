import struct

from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig


class IDZHandlerLoadTeamRankingA(IDZHandlerBase):
    cmd_codes = [0x00B9, 0x00B9, 0x00A7, 0x00A7]
    rsp_codes = [0x00B1] * 4
    name = "load_team_ranking_a"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0BA0

    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)


class IDZHandlerLoadTeamRankingB(IDZHandlerBase):
    cmd_codes = [0x00BB, 0x00BB, 0x00A9, 0x00A9]
    rsp_codes = [0x00A8] * 4
    name = "load_team_ranking_b"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0BA0

    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)
