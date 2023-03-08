from datetime import date, datetime, timedelta
from typing import Any, Dict, List
import json
import logging
from enum import Enum

from core.config import CoreConfig
from core.data.cache import cached
from titles.cm.base import CardMakerBase
from titles.cm.const import CardMakerConstants
from titles.cm.config import CardMakerConfig


class CardMaker136(CardMakerBase):
    def __init__(self, core_cfg: CoreConfig, game_cfg: CardMakerConfig) -> None:
        super().__init__(core_cfg, game_cfg)
        self.version = CardMakerConstants.VER_CARD_MAKER_136

    def handle_get_game_connect_api_request(self, data: Dict) -> Dict:
        uri = f"http://{self.core_cfg.title.hostname}:{self.core_cfg.title.port}"

        # CHUNITHM = 0, maimai = 1, ONGEKI = 2
        return {
            "length": 3,
            "gameConnectList": [
                {
                    "modelKind": 0,
                    "type": 1,
                    "titleUri": f"{uri}/SDHD/205/"
                },
                {
                    "modelKind": 1,
                    "type": 1,
                    "titleUri": f"{uri}/SDEZ/125/"
                },
                {
                    "modelKind": 2,
                    "type": 1,
                    "titleUri": f"{uri}/SDDT/135/"
                }
            ]
        }

    def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        ret = super().handle_get_game_setting_api_request(data)
        ret["gameSetting"]["dataVersion"] = "1.35.00"
        ret["gameSetting"]["ongekiCmVersion"] = "1.35.04"
        ret["gameSetting"]["chuniCmVersion"] = "2.05.00"
        ret["gameSetting"]["maimaiCmVersion"] = "1.25.00"
        return ret
