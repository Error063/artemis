from datetime import datetime, timedelta
from typing import Dict, Any
import pytz

from core.config import CoreConfig
from titles.chuni.base import ChuniBase
from titles.chuni.const import ChuniConstants
from titles.chuni.config import ChuniConfig


class ChuniAmazonPlus(ChuniBase):
    def __init__(self, core_cfg: CoreConfig, game_cfg: ChuniConfig) -> None:
        super().__init__(core_cfg, game_cfg)
        self.version = ChuniConstants.VER_CHUNITHM_AMAZON_PLUS

    async def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        ret = await super().handle_get_game_setting_api_request(data)
        ret["gameSetting"]["dataVersion"] = "1.35.00"
        return ret
