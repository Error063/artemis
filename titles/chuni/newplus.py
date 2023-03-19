from datetime import datetime, timedelta
from typing import Dict, Any
import pytz

from core.config import CoreConfig
from titles.chuni.new import ChuniNew
from titles.chuni.const import ChuniConstants
from titles.chuni.config import ChuniConfig


class ChuniNewPlus(ChuniNew):
    def __init__(self, core_cfg: CoreConfig, game_cfg: ChuniConfig) -> None:
        super().__init__(core_cfg, game_cfg)
        self.version = ChuniConstants.VER_CHUNITHM_NEW_PLUS

    def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        ret = super().handle_get_game_setting_api_request(data)
        ret["gameSetting"]["romVersion"] = "2.05.00"
        ret["gameSetting"]["dataVersion"] = "2.05.00"
        ret["gameSetting"][
            "matchingUri"
        ] = f"http://{self.core_cfg.title.hostname}:{self.core_cfg.title.port}/SDHD/205/ChuniServlet/"
        ret["gameSetting"][
            "matchingUriX"
        ] = f"http://{self.core_cfg.title.hostname}:{self.core_cfg.title.port}/SDHD/205/ChuniServlet/"
        ret["gameSetting"][
            "udpHolePunchUri"
        ] = f"http://{self.core_cfg.title.hostname}:{self.core_cfg.title.port}/SDHD/205/ChuniServlet/"
        ret["gameSetting"][
            "reflectorUri"
        ] = f"http://{self.core_cfg.title.hostname}:{self.core_cfg.title.port}/SDHD/205/ChuniServlet/"
        return ret

    def handle_cm_get_user_preview_api_request(self, data: Dict) -> Dict:
        user_data = super().handle_cm_get_user_preview_api_request(data)

        # hardcode lastDataVersion for CardMaker 1.35
        user_data["lastDataVersion"] = "2.05.00"
        return user_data
