from typing import Dict, Any

from core.config import CoreConfig
from titles.chuni.sun import ChuniSun
from titles.chuni.const import ChuniConstants
from titles.chuni.config import ChuniConfig


class ChuniSunPlus(ChuniSun):
    def __init__(self, core_cfg: CoreConfig, game_cfg: ChuniConfig) -> None:
        super().__init__(core_cfg, game_cfg)
        self.version = ChuniConstants.VER_CHUNITHM_SUN_PLUS

    def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        ret = super().handle_get_game_setting_api_request(data)
        ret["gameSetting"]["romVersion"] = self.game_cfg.version.version(self.version)["rom"]
        ret["gameSetting"]["dataVersion"] = self.game_cfg.version.version(self.version)["data"]
        ret["gameSetting"][
            "matchingUri"
        ] = f"http://{self.core_cfg.title.hostname}:{self.core_cfg.title.port}/SDHD/215/ChuniServlet/"
        ret["gameSetting"][
            "matchingUriX"
        ] = f"http://{self.core_cfg.title.hostname}:{self.core_cfg.title.port}/SDHD/215/ChuniServlet/"
        ret["gameSetting"][
            "udpHolePunchUri"
        ] = f"http://{self.core_cfg.title.hostname}:{self.core_cfg.title.port}/SDHD/215/ChuniServlet/"
        ret["gameSetting"][
            "reflectorUri"
        ] = f"http://{self.core_cfg.title.hostname}:{self.core_cfg.title.port}/SDHD/215/ChuniServlet/"
        return ret

    def handle_cm_get_user_preview_api_request(self, data: Dict) -> Dict:
        user_data = super().handle_cm_get_user_preview_api_request(data)

        # I don't know if lastDataVersion is going to matter, I don't think CardMaker 1.35 works this far up
        user_data["lastDataVersion"] = "2.15.00"
        return user_data
