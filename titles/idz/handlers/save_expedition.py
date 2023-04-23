from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig
from ..const import IDZConstants

class IDZHandlerSaveExpedition(IDZHandlerBase):
    cmd_codes = [0x008c, 0x013f]
    name = "save_expedition"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
    
    def handle(self, data: bytes) -> bytearray:
        return super().handle(data)
