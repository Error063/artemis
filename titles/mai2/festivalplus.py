from typing import Dict

from core.config import CoreConfig
from titles.mai2.festival import Mai2Festival
from titles.mai2.const import Mai2Constants
from titles.mai2.config import Mai2Config


class Mai2FestivalPlus(Mai2Festival):
    def __init__(self, cfg: CoreConfig, game_cfg: Mai2Config) -> None:
        super().__init__(cfg, game_cfg)
        self.version = Mai2Constants.VER_MAIMAI_DX_FESTIVAL_PLUS

    def handle_cm_get_user_preview_api_request(self, data: Dict) -> Dict:
        user_data = super().handle_cm_get_user_preview_api_request(data)

        # hardcode lastDataVersion for CardMaker
        user_data["lastDataVersion"] = "1.35.00"
        return user_data

    def handle_get_user_favorite_item_api_request(self, data: Dict) -> Dict:
        user_id = data.get("userId", 0)
        kind = data.get("kind", 2)
        next_index = data.get("nextIndex", 0)
        max_ct = data.get("maxCount", 100)
        is_all = data.get("isAllFavoriteItem", False)

        """
        class userFavoriteItemList:
            orderId: int
            id: int
        """
        return {
            "userId": user_id,
            "kind": kind,
            "nextIndex": 0,
            "userFavoriteItemList": [],
        }
