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


class CardMaker135(CardMakerBase):
    def __init__(self, core_cfg: CoreConfig, game_cfg: CardMakerConfig) -> None:
        super().__init__(core_cfg, game_cfg)
        self.version = CardMakerConstants.VER_CARD_MAKER_135

    def handle_get_game_connect_api_request(self, data: Dict) -> Dict:
        ret = super().handle_get_game_connect_api_request(data)
        if self.core_cfg.server.is_develop:
            uri = f"http://{self.core_cfg.title.hostname}:{self.core_cfg.title.port}"
        else:
            uri = f"http://{self.core_cfg.title.hostname}"

        ret["gameConnectList"][0]["titleUri"] = f"{uri}/SDHD/205/"
        ret["gameConnectList"][1]["titleUri"] = f"{uri}/SDEZ/125/"
        ret["gameConnectList"][2]["titleUri"] = f"{uri}/SDDT/135/"

        return ret

    def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        ret = super().handle_get_game_setting_api_request(data)
        ret["gameSetting"]["dataVersion"] = "1.35.00"
        ret["gameSetting"]["ongekiCmVersion"] = "1.35.03"
        ret["gameSetting"]["chuniCmVersion"] = "2.05.00"
        ret["gameSetting"]["maimaiCmVersion"] = "1.25.00"
        return ret
