from typing import Dict

from core.config import CoreConfig
from titles.mai2.festivalplus import Mai2FestivalPlus
from titles.mai2.const import Mai2Constants
from titles.mai2.config import Mai2Config


class Mai2Buddies(Mai2FestivalPlus):
    def __init__(self, cfg: CoreConfig, game_cfg: Mai2Config) -> None:
        super().__init__(cfg, game_cfg)
        self.version = Mai2Constants.VER_MAIMAI_DX_BUDDIES

    async def handle_cm_get_user_preview_api_request(self, data: Dict) -> Dict:
        user_data = await super().handle_cm_get_user_preview_api_request(data)

        # hardcode lastDataVersion for CardMaker
        user_data["lastDataVersion"] = "1.40.00"
        return user_data

    async def handle_get_game_ng_word_list_api_request(self, data: Dict) -> Dict:
        return {
            "ngWordExactMatchLength":0,
            "ngWordExactMatchList":[],
            "ngWordPartialMatchLength":0,
            "ngWordPartialMatchList":[]
        }

    async def handle_get_user_new_item_api_request(self, data: Dict) -> Dict:
        # TODO: Added in 1.41, implement this?
        user_id = data["userId"]
        version = data.get("version", 1041000)
        user_playlog_list = data.get("userPlaylogList", [])
        
        return {
            "userId": user_id,
            "itemKind": -1,
            "itemId": -1,
        }

