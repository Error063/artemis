from typing import Any, List, Dict
from datetime import datetime, timedelta
import pytz
import json

from core.config import CoreConfig
from titles.mai2.base import Mai2Base
from titles.mai2.config import Mai2Config
from titles.mai2.const import Mai2Constants


class Mai2Finale(Mai2Base):
    def __init__(self, cfg: CoreConfig, game_cfg: Mai2Config) -> None:
        super().__init__(cfg, game_cfg)
        self.version = Mai2Constants.VER_MAIMAI_FINALE
        self.can_deliver = True
        self.can_usbdl = True
        
        if self.core_config.server.is_develop and self.core_config.title.port > 0:
            self.old_server = f"http://{self.core_config.title.hostname}:{self.core_config.title.port}/SDEY/197/"
        
        else:
            self.old_server = f"http://{self.core_config.title.hostname}/SDEY/197/"
