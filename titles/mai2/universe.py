from typing import Any, List, Dict
from random import randint
from datetime import datetime, timedelta
import pytz
import json

from core.config import CoreConfig
from titles.mai2.base import Mai2Base
from titles.mai2.const import Mai2Constants
from titles.mai2.config import Mai2Config


class Mai2Universe(Mai2Base):
    def __init__(self, cfg: CoreConfig, game_cfg: Mai2Config) -> None:
        super().__init__(cfg, game_cfg)
        self.version = Mai2Constants.VER_MAIMAI_DX_UNIVERSE

    def handle_cm_get_user_preview_api_request(self, data: Dict) -> Dict:
        p = self.data.profile.get_profile_detail(data["userId"], self.version)
        if p is None:
            return {}

        return {
            "userName": p["userName"],
            "rating": p["playerRating"],
            # hardcode lastDataVersion for CardMaker 1.34
            "lastDataVersion": "1.20.00",
            "isLogin": False,
            "isExistSellingCard": False,
        }

    def handle_cm_get_user_data_api_request(self, data: Dict) -> Dict:
        # user already exists, because the preview checks that already
        p = self.data.profile.get_profile_detail(data["userId"], self.version)

        cards = self.data.card.get_user_cards(data["userId"])
        if cards is None or len(cards) == 0:
            # This should never happen
            self.logger.error(
                f"handle_get_user_data_api_request: Internal error - No cards found for user id {data['userId']}"
            )
            return {}

        # get the dict representation of the row so we can modify values
        user_data = p._asdict()

        # remove the values the game doesn't want
        user_data.pop("id")
        user_data.pop("user")
        user_data.pop("version")

        return {"userId": data["userId"], "userData": user_data}

    def handle_cm_login_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1}

    def handle_cm_logout_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1}

    def handle_cm_get_selling_card_api_request(self, data: Dict) -> Dict:
        selling_cards = self.data.static.get_enabled_cards(self.version)
        if selling_cards is None:
            return {"length": 0, "sellingCardList": []}

        selling_card_list = []
        for card in selling_cards:
            tmp = card._asdict()
            tmp.pop("id")
            tmp.pop("version")
            tmp.pop("cardName")
            tmp.pop("enabled")

            tmp["startDate"] = datetime.strftime(tmp["startDate"], "%Y-%m-%d %H:%M:%S")
            tmp["endDate"] = datetime.strftime(tmp["endDate"], "%Y-%m-%d %H:%M:%S")
            tmp["noticeStartDate"] = datetime.strftime(
                tmp["noticeStartDate"], "%Y-%m-%d %H:%M:%S"
            )
            tmp["noticeEndDate"] = datetime.strftime(
                tmp["noticeEndDate"], "%Y-%m-%d %H:%M:%S"
            )

            selling_card_list.append(tmp)

        return {"length": len(selling_card_list), "sellingCardList": selling_card_list}

    def handle_cm_get_user_card_api_request(self, data: Dict) -> Dict:
        user_cards = self.data.item.get_cards(data["userId"])
        if user_cards is None:
            return {"returnCode": 1, "length": 0, "nextIndex": 0, "userCardList": []}

        max_ct = data["maxCount"]
        next_idx = data["nextIndex"]
        start_idx = next_idx
        end_idx = max_ct + start_idx

        if len(user_cards[start_idx:]) > max_ct:
            next_idx += max_ct
        else:
            next_idx = 0

        card_list = []
        for card in user_cards:
            tmp = card._asdict()
            tmp.pop("id")
            tmp.pop("user")

            tmp["startDate"] = datetime.strftime(tmp["startDate"], "%Y-%m-%d %H:%M:%S")
            tmp["endDate"] = datetime.strftime(tmp["endDate"], "%Y-%m-%d %H:%M:%S")
            card_list.append(tmp)

        return {
            "returnCode": 1,
            "length": len(card_list[start_idx:end_idx]),
            "nextIndex": next_idx,
            "userCardList": card_list[start_idx:end_idx],
        }

    def handle_cm_get_user_item_api_request(self, data: Dict) -> Dict:
        super().handle_get_user_item_api_request(data)

    def handle_cm_get_user_character_api_request(self, data: Dict) -> Dict:
        characters = self.data.item.get_characters(data["userId"])

        chara_list = []
        for chara in characters:
            chara_list.append(
                {
                    "characterId": chara["characterId"],
                    # no clue why those values are even needed
                    "point": 0,
                    "count": 0,
                    "level": chara["level"],
                    "nextAwake": 0,
                    "nextAwakePercent": 0,
                    "favorite": False,
                    "awakening": chara["awakening"],
                    "useCount": chara["useCount"],
                }
            )

        return {
            "returnCode": 1,
            "length": len(chara_list),
            "userCharacterList": chara_list,
        }

    def handle_cm_get_user_card_print_error_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "userPrintDetailList": []}

    def handle_cm_upsert_user_print_api_request(self, data: Dict) -> Dict:
        user_id = data["userId"]
        upsert = data["userPrintDetail"]

        # set a random card serial number
        serial_id = "".join([str(randint(0, 9)) for _ in range(20)])

        user_card = upsert["userCard"]
        self.data.item.put_card(
            user_id,
            user_card["cardId"],
            user_card["cardTypeId"],
            user_card["charaId"],
            user_card["mapId"],
        )

        # properly format userPrintDetail for the database
        upsert.pop("userCard")
        upsert.pop("serialId")
        upsert["printDate"] = datetime.strptime(upsert["printDate"], "%Y-%m-%d")

        self.data.item.put_user_print_detail(user_id, serial_id, upsert)

        return {
            "returnCode": 1,
            "orderId": 0,
            "serialId": serial_id,
            "startDate": "2018-01-01 00:00:00",
            "endDate": "2038-01-01 00:00:00",
        }

    def handle_cm_upsert_user_printlog_api_request(self, data: Dict) -> Dict:
        return {
            "returnCode": 1,
            "orderId": 0,
            "serialId": data["userPrintlog"]["serialId"],
        }

    def handle_cm_upsert_buy_card_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1}
