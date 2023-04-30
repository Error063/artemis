from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig
from ..const import IDZConstants


class IDZHandlerSaveExpedition(IDZHandlerBase):
    cmd_codes = [0x008C, 0x013F]
    name = "save_expedition"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)

    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)
