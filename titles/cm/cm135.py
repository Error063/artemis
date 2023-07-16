from typing import Dict

from core.config import CoreConfig
from core.data.cache import cached
from titles.cm.base import CardMakerBase
from titles.cm.const import CardMakerConstants
from titles.cm.config import CardMakerConfig


class CardMaker135(CardMakerBase):
    def __init__(self, core_cfg: CoreConfig, game_cfg: CardMakerConfig) -> None:
        super().__init__(core_cfg, game_cfg)
        self.version = CardMakerConstants.VER_CARD_MAKER_135

    def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        ret = super().handle_get_game_setting_api_request(data)
        ret["gameSetting"]["dataVersion"] = "1.35.00"
        return ret
