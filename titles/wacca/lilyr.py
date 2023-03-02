from typing import Any, List, Dict
from datetime import datetime, timedelta
import json

from core.config import CoreConfig
from titles.wacca.lily import WaccaLily
from titles.wacca.config import WaccaConfig
from titles.wacca.const import WaccaConstants
from titles.wacca.handlers import *

class WaccaLilyR(WaccaLily):
    def __init__(self, cfg: CoreConfig, game_cfg: WaccaConfig) -> None:
        super().__init__(cfg, game_cfg)
        self.version = WaccaConstants.VER_WACCA_LILY_R
        self.season = 2

        self.OPTIONS_DEFAULTS["set_nav_id"] = 210002
        self.allowed_stages = [
            (2514, 14),
            (2513, 13),
            (2512, 12),
            (2511, 11),
            (2510, 10),
            (2509, 9),
            (2508, 8),
            (2507, 7),
            (2506, 6),
            (2505, 5),
            (2504, 4),
            (2503, 3),
            (2501, 2),
            (2501, 1),
            (210001, 0),
            (210002, 0),
            (210003, 0),
        ]

    def handle_user_status_create_request(self, data: Dict)-> Dict:
        req = UserStatusCreateRequest(data)
        resp = super().handle_user_status_create_request(data)

        self.data.item.put_item(req.aimeId, WaccaConstants.ITEM_TYPES["navigator"], 210054) # Added lily r
        self.data.item.put_item(req.aimeId, WaccaConstants.ITEM_TYPES["navigator"], 210055) # Added lily r
        self.data.item.put_item(req.aimeId, WaccaConstants.ITEM_TYPES["navigator"], 210056) # Added lily r
        self.data.item.put_item(req.aimeId, WaccaConstants.ITEM_TYPES["navigator"], 210057) # Added lily r
        self.data.item.put_item(req.aimeId, WaccaConstants.ITEM_TYPES["navigator"], 210058) # Added lily r
        self.data.item.put_item(req.aimeId, WaccaConstants.ITEM_TYPES["navigator"], 210059) # Added lily r
        self.data.item.put_item(req.aimeId, WaccaConstants.ITEM_TYPES["navigator"], 210060) # Added lily r
        self.data.item.put_item(req.aimeId, WaccaConstants.ITEM_TYPES["navigator"], 210061) # Added lily r
        
        return resp

    def handle_user_status_logout_request(self, data: Dict)-> Dict:
        return BaseResponse().make()
