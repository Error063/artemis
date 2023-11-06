import logging

from core.config import CoreConfig
from titles.idac.config import IDACConfig
from titles.idac.const import IDACConstants
from titles.idac.database import IDACData


class IDACBase:
    def __init__(self, core_cfg: CoreConfig, game_cfg: IDACConfig) -> None:
        self.core_cfg = core_cfg
        self.game_config = game_cfg
        self.game = IDACConstants.GAME_CODE
        self.version = IDACConstants.VER_IDAC_SEASON_1
        self.data = IDACData(core_cfg)
        self.logger = logging.getLogger("idac")
