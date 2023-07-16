from typing import Dict

from core.config import CoreConfig
from titles.mai2.universe import Mai2Universe
from titles.mai2.const import Mai2Constants
from titles.mai2.config import Mai2Config


class Mai2UniversePlus(Mai2Universe):
    def __init__(self, cfg: CoreConfig, game_cfg: Mai2Config) -> None:
        super().__init__(cfg, game_cfg)
        self.version = Mai2Constants.VER_MAIMAI_DX_UNIVERSE_PLUS

    def handle_cm_get_user_preview_api_request(self, data: Dict) -> Dict:
        user_data = super().handle_cm_get_user_preview_api_request(data)

        # hardcode lastDataVersion for CardMaker 1.35
        user_data["lastDataVersion"] = "1.25.00"
        return user_data
