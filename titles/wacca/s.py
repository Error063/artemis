from typing import Any, List, Dict
from datetime import datetime, timedelta
import json

from core.config import CoreConfig
from titles.wacca.base import WaccaBase
from titles.wacca.config import WaccaConfig
from titles.wacca.const import WaccaConstants

from titles.wacca.handlers import *

class WaccaS(WaccaBase):
    allowed_stages = [
        (1501, 1),
        (1502, 2),
        (1503, 3),
        (1504, 4),
        (1505, 5),
        (1506, 6),
        (1507, 7),
        (1508, 8),
        (1509, 9),
        (1510, 10),
        (1511, 11),
        (1512, 12),
        (1513, 13),
    ]
    
    def __init__(self, cfg: CoreConfig, game_cfg: WaccaConfig) -> None:
        super().__init__(cfg, game_cfg)
        self.version = WaccaConstants.VER_WACCA_S
    
    def handle_advertise_GetNews_request(self, data: Dict) -> List[Any]:
        resp = GetNewsResponseV2()
        return resp.make()
