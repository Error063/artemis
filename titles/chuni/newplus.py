from typing import Dict, Any

from core.utils import Utils
from core.config import CoreConfig
from titles.chuni.new import ChuniNew
from titles.chuni.const import ChuniConstants
from titles.chuni.config import ChuniConfig

class ChuniNewPlus(ChuniNew):
    def __init__(self, core_cfg: CoreConfig, game_cfg: ChuniConfig) -> None:
        super().__init__(core_cfg, game_cfg)
        self.version = ChuniConstants.VER_CHUNITHM_NEW_PLUS

    def handle_cm_get_user_preview_api_request(self, data: Dict) -> Dict:
        user_data = super().handle_cm_get_user_preview_api_request(data)

        # hardcode lastDataVersion for CardMaker 1.35 A028
        user_data["lastDataVersion"] = "2.05.00"
        return user_data