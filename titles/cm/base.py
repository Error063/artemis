from datetime import date, datetime, timedelta
from typing import Any, Dict, List
import json
import logging
from enum import Enum

from core.config import CoreConfig
from core.data.cache import cached
from titles.cm.const import CardMakerConstants
from titles.cm.config import CardMakerConfig


class CardMakerBase:
    def __init__(self, core_cfg: CoreConfig, game_cfg: CardMakerConfig) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.date_time_format = "%Y-%m-%d %H:%M:%S"
        self.date_time_format_ext = (
            "%Y-%m-%d %H:%M:%S.%f"  # needs to be lopped off at [:-5]
        )
        self.date_time_format_short = "%Y-%m-%d"
        self.logger = logging.getLogger("cardmaker")
        self.game = CardMakerConstants.GAME_CODE
        self.version = CardMakerConstants.VER_CARD_MAKER

    @staticmethod
    def _parse_int_ver(version: str) -> str:
        return version.replace(".", "")[:3]

    def handle_get_game_connect_api_request(self, data: Dict) -> Dict:
        if self.core_cfg.server.is_develop:
            uri = f"http://{self.core_cfg.title.hostname}:{self.core_cfg.title.port}"
        else:
            uri = f"http://{self.core_cfg.title.hostname}"

        # grab the dict with all games version numbers from user config
        games_ver = self.game_cfg.version.version(self.version)

        return {
            "length": 3,
            "gameConnectList": [
                # CHUNITHM
                {
                    "modelKind": 0,
                    "type": 1,
                    "titleUri": f"{uri}/SDHD/{self._parse_int_ver(games_ver['chuni'])}/",
                },
                # maimai DX
                {
                    "modelKind": 1,
                    "type": 1,
                    "titleUri": f"{uri}/SDEZ/{self._parse_int_ver(games_ver['maimai'])}/",
                },
                # ONGEKI
                {
                    "modelKind": 2,
                    "type": 1,
                    "titleUri": f"{uri}/SDDT/{self._parse_int_ver(games_ver['ongeki'])}/",
                },
            ],
        }

    def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        reboot_start = date.strftime(
            datetime.now() + timedelta(hours=3), self.date_time_format
        )
        reboot_end = date.strftime(
            datetime.now() + timedelta(hours=4), self.date_time_format
        )

        # grab the dict with all games version numbers from user config
        games_ver = self.game_cfg.version.version(self.version)

        return {
            "gameSetting": {
                "dataVersion": "1.30.00",
                "ongekiCmVersion": games_ver["ongeki"],
                "chuniCmVersion": games_ver["chuni"],
                "maimaiCmVersion": games_ver["maimai"],
                "requestInterval": 10,
                "rebootStartTime": reboot_start,
                "rebootEndTime": reboot_end,
                "maxCountCharacter": 100,
                "maxCountItem": 100,
                "maxCountCard": 100,
                "watermark": False,
                "isMaintenance": False,
                "isBackgroundDistribute": False,
            },
            "isDumpUpload": False,
            "isAou": False,
        }

    def handle_get_client_bookkeeping_api_request(self, data: Dict) -> Dict:
        return {"placeId": data["placeId"], "length": 0, "clientBookkeepingList": []}

    def handle_upsert_client_setting_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "UpsertClientSettingApi"}

    def handle_upsert_client_bookkeeping_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "UpsertClientBookkeepingApi"}
