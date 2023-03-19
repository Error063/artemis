from typing import Dict, Any

from core.config import CoreConfig
from titles.ongeki.base import OngekiBase
from titles.ongeki.const import OngekiConstants
from titles.ongeki.config import OngekiConfig


class OngekiSummer(OngekiBase):
    def __init__(self, core_cfg: CoreConfig, game_cfg: OngekiConfig) -> None:
        super().__init__(core_cfg, game_cfg)
        self.version = OngekiConstants.VER_ONGEKI_SUMMER

    def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        ret = super().handle_get_game_setting_api_request(data)
        ret["gameSetting"]["dataVersion"] = "1.10.00"
        ret["gameSetting"]["onlineDataVersion"] = "1.10.00"
        return ret
