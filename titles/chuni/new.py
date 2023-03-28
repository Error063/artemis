import logging
from datetime import datetime, timedelta
from random import randint
from typing import Dict

from core.config import CoreConfig
from titles.chuni.const import ChuniConstants
from titles.chuni.database import ChuniData
from titles.chuni.base import ChuniBase
from titles.chuni.config import ChuniConfig


class ChuniNew(ChuniBase):
    ITEM_TYPE = {"character": 20, "story": 21, "card": 22}

    def __init__(self, core_cfg: CoreConfig, game_cfg: ChuniConfig) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.data = ChuniData(core_cfg)
        self.date_time_format = "%Y-%m-%d %H:%M:%S"
        self.logger = logging.getLogger("chuni")
        self.game = ChuniConstants.GAME_CODE
        self.version = ChuniConstants.VER_CHUNITHM_NEW

    def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        match_start = datetime.strftime(
            datetime.now() - timedelta(hours=10), self.date_time_format
        )
        match_end = datetime.strftime(
            datetime.now() + timedelta(hours=10), self.date_time_format
        )
        reboot_start = datetime.strftime(
            datetime.now() - timedelta(hours=11), self.date_time_format
        )
        reboot_end = datetime.strftime(
            datetime.now() - timedelta(hours=10), self.date_time_format
        )
        return {
            "gameSetting": {
                "isMaintenance": "false",
                "requestInterval": 10,
                "rebootStartTime": reboot_start,
                "rebootEndTime": reboot_end,
                "isBackgroundDistribute": "false",
                "maxCountCharacter": 300,
                "maxCountItem": 300,
                "maxCountMusic": 300,
                "matchStartTime": match_start,
                "matchEndTime": match_end,
                "matchTimeLimit": 99,
                "matchErrorLimit": 9999,
                "romVersion": self.game_cfg.version.version(self.version)["rom"],
                "dataVersion": self.game_cfg.version.version(self.version)["data"],
                "matchingUri": f"http://{self.core_cfg.title.hostname}:{self.core_cfg.title.port}/SDHD/200/ChuniServlet/",
                "matchingUriX": f"http://{self.core_cfg.title.hostname}:{self.core_cfg.title.port}/SDHD/200/ChuniServlet/",
                "udpHolePunchUri": f"http://{self.core_cfg.title.hostname}:{self.core_cfg.title.port}/SDHD/200/ChuniServlet/",
                "reflectorUri": f"http://{self.core_cfg.title.hostname}:{self.core_cfg.title.port}/SDHD/200/ChuniServlet/",
            },
            "isDumpUpload": "false",
            "isAou": "false",
        }

    def handle_remove_token_api_request(self, data: Dict) -> Dict:
        return {"returnCode": "1"}

    def handle_delete_token_api_request(self, data: Dict) -> Dict:
        return {"returnCode": "1"}

    def handle_create_token_api_request(self, data: Dict) -> Dict:
        return {"returnCode": "1"}

    def handle_get_user_map_area_api_request(self, data: Dict) -> Dict:
        user_map_areas = self.data.item.get_map_areas(data["userId"])

        map_areas = []
        for map_area in user_map_areas:
            tmp = map_area._asdict()
            tmp.pop("id")
            tmp.pop("user")
            map_areas.append(tmp)

        return {"userId": data["userId"], "userMapAreaList": map_areas}

    def handle_get_user_symbol_chat_setting_api_request(self, data: Dict) -> Dict:
        return {"userId": data["userId"], "symbolCharInfoList": []}

    def handle_get_user_preview_api_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile_preview(data["userId"], self.version)
        if profile is None:
            return None
        profile_character = self.data.item.get_character(
            data["userId"], profile["characterId"]
        )

        if profile_character is None:
            chara = {}
        else:
            chara = profile_character._asdict()
            chara.pop("id")
            chara.pop("user")

        data1 = {
            "userId": data["userId"],
            # Current Login State
            "isLogin": False,
            "lastLoginDate": profile["lastPlayDate"],
            # User Profile
            "userName": profile["userName"],
            "reincarnationNum": profile["reincarnationNum"],
            "level": profile["level"],
            "exp": profile["exp"],
            "playerRating": profile["playerRating"],
            "lastGameId": profile["lastGameId"],
            "lastRomVersion": profile["lastRomVersion"],
            "lastDataVersion": profile["lastDataVersion"],
            "lastPlayDate": profile["lastPlayDate"],
            "emoneyBrandId": 0,
            "trophyId": profile["trophyId"],
            # Current Selected Character
            "userCharacter": chara,
            # User Game Options
            "playerLevel": profile["playerLevel"],
            "rating": profile["rating"],
            "headphone": profile["headphone"],
            # Enables favorites and teams
            "chargeState": 1,
            "userNameEx": "",
            "banState": 0,
            "classEmblemMedal": profile["classEmblemMedal"],
            "classEmblemBase": profile["classEmblemBase"],
            "battleRankId": profile["battleRankId"],
        }
        return data1

    def handle_cm_get_user_preview_api_request(self, data: Dict) -> Dict:
        p = self.data.profile.get_profile_data(data["userId"], self.version)
        if p is None:
            return {}

        return {
            "userName": p["userName"],
            "level": p["level"],
            "medal": p["medal"],
            "lastDataVersion": "2.00.00",
            "isLogin": False,
        }

    def handle_printer_login_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1}

    def handle_printer_logout_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1}

    def handle_get_game_gacha_api_request(self, data: Dict) -> Dict:
        """
        returns all current active banners (gachas)
        """
        game_gachas = self.data.static.get_gachas(self.version)

        # clean the database rows
        game_gacha_list = []
        for gacha in game_gachas:
            tmp = gacha._asdict()
            tmp.pop("id")
            tmp.pop("version")
            tmp["startDate"] = datetime.strftime(tmp["startDate"], "%Y-%m-%d %H:%M:%S")
            tmp["endDate"] = datetime.strftime(tmp["endDate"], "%Y-%m-%d %H:%M:%S")
            tmp["noticeStartDate"] = datetime.strftime(
                tmp["noticeStartDate"], "%Y-%m-%d %H:%M:%S"
            )
            tmp["noticeEndDate"] = datetime.strftime(
                tmp["noticeEndDate"], "%Y-%m-%d %H:%M:%S"
            )

            game_gacha_list.append(tmp)

        return {
            "length": len(game_gacha_list),
            "gameGachaList": game_gacha_list,
            # no clue
            "registIdList": [],
        }

    def handle_get_game_gacha_card_by_id_api_request(self, data: Dict) -> Dict:
        """
        returns all valid cards for a given gachaId
        """
        game_gacha_cards = self.data.static.get_gacha_cards(data["gachaId"])

        game_gacha_card_list = []
        for gacha_card in game_gacha_cards:
            tmp = gacha_card._asdict()
            tmp.pop("id")
            game_gacha_card_list.append(tmp)

        return {
            "gachaId": data["gachaId"],
            "length": len(game_gacha_card_list),
            # check isPickup from the chuni_static_gachas?
            "isPickup": False,
            "gameGachaCardList": game_gacha_card_list,
            # again no clue
            "emissionList": [],
            "afterCalcList": [],
            "ssrBookCalcList": [],
        }

    def handle_cm_get_user_data_api_request(self, data: Dict) -> Dict:
        p = self.data.profile.get_profile_data(data["userId"], self.version)
        if p is None:
            return {}

        profile = p._asdict()
        profile.pop("id")
        profile.pop("user")
        profile.pop("version")

        return {
            "userId": data["userId"],
            "userData": profile,
            "userEmoney": [
                {
                    "type": 0,
                    "emoneyCredit": 100,
                    "emoneyBrand": 1,
                    "ext1": 0,
                    "ext2": 0,
                    "ext3": 0,
                }
            ],
        }

    def handle_get_user_gacha_api_request(self, data: Dict) -> Dict:
        user_gachas = self.data.item.get_user_gachas(data["userId"])
        if user_gachas is None:
            return {"userId": data["userId"], "length": 0, "userGachaList": []}

        user_gacha_list = []
        for gacha in user_gachas:
            tmp = gacha._asdict()
            tmp.pop("id")
            tmp.pop("user")
            tmp["dailyGachaDate"] = datetime.strftime(tmp["dailyGachaDate"], "%Y-%m-%d")
            user_gacha_list.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(user_gacha_list),
            "userGachaList": user_gacha_list,
        }

    def handle_get_user_printed_card_api_request(self, data: Dict) -> Dict:
        user_print_list = self.data.item.get_user_print_states(
            data["userId"], has_completed=True
        )
        if user_print_list is None:
            return {
                "userId": data["userId"],
                "length": 0,
                "nextIndex": -1,
                "userPrintedCardList": [],
            }

        print_list = []
        next_idx = int(data["nextIndex"])
        max_ct = int(data["maxCount"])

        for x in range(next_idx, len(user_print_list)):
            tmp = user_print_list[x]._asdict()
            print_list.append(tmp["cardId"])

            if len(print_list) >= max_ct:
                break

        if len(print_list) >= max_ct:
            next_idx = next_idx + max_ct
        else:
            next_idx = -1

        return {
            "userId": data["userId"],
            "length": len(print_list),
            "nextIndex": next_idx,
            "userPrintedCardList": print_list,
        }

    def handle_get_user_card_print_error_api_request(self, data: Dict) -> Dict:
        user_id = data["userId"]

        user_print_states = self.data.item.get_user_print_states(
            user_id, has_completed=False
        )

        card_print_state_list = []
        for card in user_print_states:
            tmp = card._asdict()
            tmp["orderId"] = tmp["id"]
            tmp.pop("user")
            tmp["limitDate"] = datetime.strftime(tmp["limitDate"], "%Y-%m-%d")

            card_print_state_list.append(tmp)

        return {
            "userId": user_id,
            "length": len(card_print_state_list),
            "userCardPrintStateList": card_print_state_list,
        }

    def handle_cm_get_user_character_api_request(self, data: Dict) -> Dict:
        return super().handle_get_user_character_api_request(data)

    def handle_cm_get_user_item_api_request(self, data: Dict) -> Dict:
        return super().handle_get_user_item_api_request(data)

    def handle_roll_gacha_api_request(self, data: Dict) -> Dict:
        """
        Handle a gacha roll API request, with:
        gachaId: the gachaId where the cards should be pulled from
        times: the number of gacha rolls
        characterId: the character which the user wants
        """
        gacha_id = data["gachaId"]
        num_rolls = data["times"]
        chara_id = data["characterId"]

        rolled_cards = []

        # characterId is set after 10 rolls, where the user can select a card
        # from all gameGachaCards, therefore the correct cardId for a given
        # characterId should be returned
        if chara_id != -1:
            # get the
            card = self.data.static.get_gacha_card_by_character(gacha_id, chara_id)

            tmp = card._asdict()
            tmp.pop("id")

            rolled_cards.append(tmp)
        else:
            gacha_cards = self.data.static.get_gacha_cards(gacha_id)

            # get the card id for each roll
            for _ in range(num_rolls):
                # get the index from all possible cards
                card_idx = randint(0, len(gacha_cards) - 1)
                # remove the index from the cards so it wont get pulled again
                card = gacha_cards.pop(card_idx)

                # remove the "id" fronm the card
                tmp = card._asdict()
                tmp.pop("id")

                rolled_cards.append(tmp)

        return {"length": len(rolled_cards), "gameGachaCardList": rolled_cards}

    def handle_cm_upsert_user_gacha_api_request(self, data: Dict) -> Dict:
        upsert = data["cmUpsertUserGacha"]
        user_id = data["userId"]
        place_id = data["placeId"]

        # save the user data
        user_data = upsert["userData"]
        user_data.pop("rankUpChallengeResults")
        user_data.pop("userEmoney")

        self.data.profile.put_profile_data(user_id, self.version, user_data)

        # save the user gacha
        user_gacha = upsert["userGacha"]
        gacha_id = user_gacha["gachaId"]
        user_gacha.pop("gachaId")
        user_gacha.pop("dailyGachaDate")

        self.data.item.put_user_gacha(user_id, gacha_id, user_gacha)

        # save all user items
        if "userItemList" in upsert:
            for item in upsert["userItemList"]:
                self.data.item.put_item(user_id, item)

        # add every gamegachaCard to database
        for card in upsert["gameGachaCardList"]:
            self.data.item.put_user_print_state(
                user_id,
                hasCompleted=False,
                placeId=place_id,
                cardId=card["cardId"],
                gachaId=card["gachaId"],
            )

        # retrieve every game gacha card which has been added in order to get
        # the orderId for the next request
        user_print_states = self.data.item.get_user_print_states_by_gacha(
            user_id, gacha_id, has_completed=False
        )
        card_print_state_list = []
        for card in user_print_states:
            tmp = card._asdict()
            tmp["orderId"] = tmp["id"]
            tmp.pop("user")
            tmp["limitDate"] = datetime.strftime(tmp["limitDate"], "%Y-%m-%d")

            card_print_state_list.append(tmp)

        return {
            "returnCode": "1",
            "apiName": "CMUpsertUserGachaApi",
            "userCardPrintStateList": card_print_state_list,
        }

    def handle_cm_upsert_user_printlog_api_request(self, data: Dict) -> Dict:
        return {
            "returnCode": 1,
            "orderId": 0,
            "serialId": "11111111111111111111",
            "apiName": "CMUpsertUserPrintlogApi",
        }

    def handle_cm_upsert_user_print_api_request(self, data: Dict) -> Dict:
        user_print_detail = data["userPrintDetail"]
        user_id = data["userId"]

        # generate random serial id
        serial_id = "".join([str(randint(0, 9)) for _ in range(20)])

        # not needed because are either zero or unset
        user_print_detail.pop("orderId")
        user_print_detail.pop("printNumber")
        user_print_detail.pop("serialId")
        user_print_detail["printDate"] = datetime.strptime(
            user_print_detail["printDate"], "%Y-%m-%d"
        )

        # add the entry to the user print table with the random serialId
        self.data.item.put_user_print_detail(user_id, serial_id, user_print_detail)

        return {
            "returnCode": 1,
            "orderId": 0,
            "serialId": serial_id,
            "apiName": "CMUpsertUserPrintApi",
        }

    def handle_cm_upsert_user_print_subtract_api_request(self, data: Dict) -> Dict:
        upsert = data["userCardPrintState"]
        user_id = data["userId"]
        place_id = data["placeId"]

        # save all user items
        if "userItemList" in data:
            for item in data["userItemList"]:
                self.data.item.put_item(user_id, item)

        # set the card print state to success and use the orderId as the key
        self.data.item.put_user_print_state(
            user_id, id=upsert["orderId"], hasCompleted=True
        )

        return {"returnCode": "1", "apiName": "CMUpsertUserPrintSubtractApi"}

    def handle_cm_upsert_user_print_cancel_api_request(self, data: Dict) -> Dict:
        order_ids = data["orderIdList"]
        user_id = data["userId"]

        # set the card print state to success and use the orderId as the key
        for order_id in order_ids:
            self.data.item.put_user_print_state(user_id, id=order_id, hasCompleted=True)

        return {"returnCode": "1", "apiName": "CMUpsertUserPrintCancelApi"}
