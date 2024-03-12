from typing import Any, List, Dict
from datetime import datetime, timedelta
import pytz
import json

from core.config import CoreConfig
from titles.mai2.dxplus import Mai2DXPlus
from titles.mai2.config import Mai2Config
from titles.mai2.const import Mai2Constants


class Mai2Splash(Mai2DXPlus):
    def __init__(self, cfg: CoreConfig, game_cfg: Mai2Config) -> None:
        super().__init__(cfg, game_cfg)
        self.version = Mai2Constants.VER_MAIMAI_DX_SPLASH
