from datetime import date, datetime, timedelta
from typing import Any, Dict, List
import json
import logging
from enum import Enum

from core.config import CoreConfig
from core.data.cache import cached
from titles.ongeki.const import OngekiConstants
from titles.ongeki.config import OngekiConfig
from titles.ongeki.database import OngekiData
from titles.ongeki.config import OngekiConfig


class OngekiBattleGrade(Enum):
    FAILED = 0
    DRAW = 1
    USUALLY = 2
    GOOD = 3
    GREAT = 4
    EXCELLENT = 5
    UNBELIEVABLE_GOLD = 6
    UNBELIEVABLE_RAINBOW = 7


class OngekiBattlePointGrade(Enum):
    FRESHMAN = 0
    KYU10 = 1
    KYU9 = 2
    KYU8 = 3
    KYU7 = 4
    KYU6 = 5
    KYU5 = 6
    KYU4 = 7
    KYU3 = 8
    KYU2 = 9
    KYU1 = 10
    DAN1 = 11
    DAN2 = 12
    DAN3 = 13
    DAN4 = 14
    DAN5 = 15
    DAN6 = 16
    DAN7 = 17
    DAN8 = 18
    DAN9 = 19
    DAN10 = 20
    SODEN = 21


class OngekiTechnicalGrade(Enum):
    D = 0
    C = 1
    B = 2
    BB = 3
    BBB = 4
    A = 5
    AA = 6
    AAA = 7
    S = 8
    SS = 9
    SSS = 10
    SSSp = 11


class OngekiDifficulty(Enum):
    BASIC = 0
    ADVANCED = 1
    EXPERT = 2
    MASTER = 3
    LUNATIC = 10


class OngekiGPLogKind(Enum):
    NONE = 0
    BUY1_START = 1
    BUY2_START = 2
    BUY3_START = 3
    BUY1_ADD = 4
    BUY2_ADD = 5
    BUY3_ADD = 6
    FIRST_PLAY = 7
    COMPENSATION = 8

    PAY_PLAY = 11
    PAY_TIME = 12
    PAY_MAS_UNLOCK = 13
    PAY_MONEY = 14


class OngekiBase:
    def __init__(self, core_cfg: CoreConfig, game_cfg: OngekiConfig) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.data = OngekiData(core_cfg)
        self.date_time_format = "%Y-%m-%d %H:%M:%S"
        self.date_time_format_ext = (
            "%Y-%m-%d %H:%M:%S.%f"  # needs to be lopped off at [:-5]
        )
        self.date_time_format_short = "%Y-%m-%d"
        self.logger = logging.getLogger("ongeki")
        self.game = OngekiConstants.GAME_CODE
        self.version = OngekiConstants.VER_ONGEKI

    def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        reboot_start = date.strftime(
            datetime.now() + timedelta(hours=3), self.date_time_format
        )
        reboot_end = date.strftime(
            datetime.now() + timedelta(hours=4), self.date_time_format
        )
        return {
            "gameSetting": {
                "dataVersion": "1.00.00",
                "onlineDataVersion": "1.00.00",
                "isMaintenance": "false",
                "requestInterval": 10,
                "rebootStartTime": reboot_start,
                "rebootEndTime": reboot_end,
                "isBackgroundDistribute": "false",
                "maxCountCharacter": 50,
                "maxCountCard": 300,
                "maxCountItem": 300,
                "maxCountMusic": 50,
                "maxCountMusicItem": 300,
                "macCountRivalMusic": 300,
            },
            "isDumpUpload": "false",
            "isAou": "true",
        }

    def handle_get_game_idlist_api_request(self, data: Dict) -> Dict:
        """
        Gets lists of song IDs, either disabled songs or recomended songs depending on type?
        """
        # type - int
        # id - int
        return {"type": data["type"], "length": 0, "gameIdlistList": []}

    def handle_get_game_ranking_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "gameRankingList": []}

    def handle_get_game_point_api_request(self, data: Dict) -> Dict:
        """
        Sets the GP amount for A and B sets for 1 - 3 credits
        """
        return {
            "length": 6,
            "gamePointList": [
                {
                    "type": 0,
                    "cost": 100,
                    "startDate": "2000-01-01 05:00:00.0",
                    "endDate": "2099-01-01 05:00:00.0",
                },
                {
                    "type": 1,
                    "cost": 230,
                    "startDate": "2000-01-01 05:00:00.0",
                    "endDate": "2099-01-01 05:00:00.0",
                },
                {
                    "type": 2,
                    "cost": 370,
                    "startDate": "2000-01-01 05:00:00.0",
                    "endDate": "2099-01-01 05:00:00.0",
                },
                {
                    "type": 3,
                    "cost": 120,
                    "startDate": "2000-01-01 05:00:00.0",
                    "endDate": "2099-01-01 05:00:00.0",
                },
                {
                    "type": 4,
                    "cost": 240,
                    "startDate": "2000-01-01 05:00:00.0",
                    "endDate": "2099-01-01 05:00:00.0",
                },
                {
                    "type": 5,
                    "cost": 360,
                    "startDate": "2000-01-01 05:00:00.0",
                    "endDate": "2099-01-01 05:00:00.0",
                },
            ],
        }

    def handle_game_login_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "gameLogin"}

    def handle_game_logout_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "gameLogout"}

    def handle_extend_lock_time_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "ExtendLockTimeApi"}

    def handle_get_game_reward_api_request(self, data: Dict) -> Dict:
        # TODO: reward list
        return {"length": 0, "gameRewardList": []}

    def handle_get_game_present_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "gamePresentList": []}

    def handle_get_game_message_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "gameMessageList": []}

    def handle_get_game_sale_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "gameSaleList": []}

    def handle_get_game_tech_music_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "gameTechMusicList": []}

    def handle_upsert_client_setting_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "UpsertClientSettingApi"}

    def handle_upsert_client_testmode_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "UpsertClientTestmodeApi"}

    def handle_upsert_client_bookkeeping_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "upsertClientBookkeeping"}

    def handle_upsert_client_develop_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "upsertClientDevelop"}

    def handle_upsert_client_error_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "upsertClientError"}

    def handle_upsert_user_gplog_api_request(self, data: Dict) -> Dict:
        user = data["userId"]
        if user >= 200000000000000:  # Account for guest play
            user = None

        self.data.log.put_gp_log(
            user,
            data["usedCredit"],
            data["placeName"],
            data["userGplog"]["trxnDate"],
            data["userGplog"]["placeId"],
            data["userGplog"]["kind"],
            data["userGplog"]["pattern"],
            data["userGplog"]["currentGP"],
        )

        return {"returnCode": 1, "apiName": "UpsertUserGplogApi"}

    def handle_extend_lock_time_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "ExtendLockTimeApi"}

    def handle_get_game_event_api_request(self, data: Dict) -> Dict:
        evts = self.data.static.get_enabled_events(self.version)

        evt_list = []
        for event in evts:
            evt_list.append(
                {
                    "type": event["type"],
                    "id": event["eventId"],
                    # actually use the startDate from the import so it
                    # properly shows all the events when new ones are imported
                    "startDate": datetime.strftime(
                        event["startDate"], "%Y-%m-%d %H:%M:%S.0"
                    ),
                    "endDate": "2099-12-31 00:00:00.0",
                }
            )

        return {
            "type": data["type"],
            "length": len(evt_list),
            "gameEventList": evt_list,
        }

    def handle_get_game_id_list_api_request(self, data: Dict) -> Dict:
        game_idlist: List[str, Any] = []  # 1 to 230 & 8000 to 8050

        if data["type"] == 1:
            for i in range(1, 231):
                game_idlist.append({"type": 1, "id": i})
            return {
                "type": data["type"],
                "length": len(game_idlist),
                "gameIdlistList": game_idlist,
            }
        elif data["type"] == 2:
            for i in range(8000, 8051):
                game_idlist.append({"type": 2, "id": i})
            return {
                "type": data["type"],
                "length": len(game_idlist),
                "gameIdlistList": game_idlist,
            }

    def handle_get_user_region_api_request(self, data: Dict) -> Dict:
        return {"userId": data["userId"], "length": 0, "userRegionList": []}

    def handle_get_user_preview_api_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile_preview(data["userId"], self.version)

        if profile is None:
            return {
                "userId": data["userId"],
                "isLogin": False,
                "lastLoginDate": "0000-00-00 00:00:00",
                "userName": "",
                "reincarnationNum": 0,
                "level": 0,
                "exp": 0,
                "playerRating": 0,
                "lastGameId": "",
                "lastRomVersion": "",
                "lastDataVersion": "",
                "lastPlayDate": "",
                "nameplateId": 0,
                "trophyId": 0,
                "cardId": 0,
                "dispPlayerLv": 0,
                "dispRating": 0,
                "dispBP": 0,
                "headphone": 0,
                "banStatus": 0,
                "isWarningConfirmed": True,
            }

        return {
            "userId": data["userId"],
            "isLogin": False,
            "lastLoginDate": profile["lastPlayDate"],
            "userName": profile["userName"],
            "reincarnationNum": profile["reincarnationNum"],
            "level": profile["level"],
            "exp": profile["exp"],
            "playerRating": profile["playerRating"],
            "lastGameId": profile["lastGameId"],
            "lastRomVersion": profile["lastRomVersion"],
            "lastDataVersion": profile["lastDataVersion"],
            "lastPlayDate": profile["lastPlayDate"],
            "nameplateId": profile["nameplateId"],
            "trophyId": profile["trophyId"],
            "cardId": profile["cardId"],
            "dispPlayerLv": profile["dispPlayerLv"],
            "dispRating": profile["dispRating"],
            "dispBP": profile["dispBP"],
            "headphone": profile["headphone"],
            "banStatus": profile["banStatus"],
            "isWarningConfirmed": True,
        }

    def handle_get_user_tech_count_api_request(self, data: Dict) -> Dict:
        """
        Gets the number of AB and ABPs a player has per-difficulty (7, 7+, 8, etc)
        The game sends this in upsert so we don't have to calculate it all out thankfully
        """
        utcl = self.data.score.get_tech_count(data["userId"])
        userTechCountList = []

        for tc in utcl:
            tc.pop("id")
            tc.pop("user")
            userTechCountList.append(tc)

        return {
            "userId": data["userId"],
            "length": len(userTechCountList),
            "userTechCountList": userTechCountList,
        }

    def handle_get_user_tech_event_api_request(self, data: Dict) -> Dict:
        user_tech_event_list = self.data.item.get_tech_event(data["userId"])
        if user_tech_event_list is None:
            return {}

        tech_evt = []
        for evt in user_tech_event_list:
            tmp = evt._asdict()
            tmp.pop("id")
            tmp.pop("user")
            tech_evt.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(tech_evt),
            "userTechEventList": tech_evt,
        }

    def handle_get_user_tech_event_ranking_api_request(self, data: Dict) -> Dict:
        # user_event_ranking_list = self.data.item.get_tech_event_ranking(data["userId"])
        # if user_event_ranking_list is None: return {}

        evt_ranking = []
        # for evt in user_event_ranking_list:
        #    tmp = evt._asdict()
        #    tmp.pop("id")
        #    tmp.pop("user")
        #    evt_ranking.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(evt_ranking),
            "userTechEventRankingList": evt_ranking,
        }

    def handle_get_user_kop_api_request(self, data: Dict) -> Dict:
        kop_list = self.data.profile.get_kop(data["userId"])
        if kop_list is None:
            return {}

        for kop in kop_list:
            kop.pop("user")
            kop.pop("id")

        return {
            "userId": data["userId"],
            "length": len(kop_list),
            "userKopList": kop_list,
        }

    def handle_get_user_music_api_request(self, data: Dict) -> Dict:
        song_list = self.util_generate_music_list(data["userId"])
        max_ct = data["maxCount"]
        next_idx = data["nextIndex"]
        start_idx = next_idx
        end_idx = max_ct + start_idx

        if len(song_list[start_idx:]) > max_ct:
            next_idx += max_ct

        else:
            next_idx = -1

        return {
            "userId": data["userId"],
            "length": len(song_list[start_idx:end_idx]),
            "nextIndex": next_idx,
            "userMusicList": song_list[start_idx:end_idx],
        }

    def handle_get_user_item_api_request(self, data: Dict) -> Dict:
        kind = data["nextIndex"] / 10000000000
        p = self.data.item.get_items(data["userId"], kind)

        if p is None:
            return {
                "userId": data["userId"],
                "nextIndex": -1,
                "itemKind": kind,
                "userItemList": [],
            }

        items: List[Dict[str, Any]] = []
        for i in range(data["nextIndex"] % 10000000000, len(p)):
            if len(items) > data["maxCount"]:
                break
            tmp = p[i]._asdict()
            tmp.pop("user")
            tmp.pop("id")
            items.append(tmp)

        xout = kind * 10000000000 + (data["nextIndex"] % 10000000000) + len(items)

        if len(items) < data["maxCount"] or data["maxCount"] == 0:
            nextIndex = 0
        else:
            nextIndex = xout

        return {
            "userId": data["userId"],
            "nextIndex": int(nextIndex),
            "itemKind": int(kind),
            "length": len(items),
            "userItemList": items,
        }

    def handle_get_user_option_api_request(self, data: Dict) -> Dict:
        o = self.data.profile.get_profile_options(data["userId"])
        if o is None:
            return {}

        # get the dict representation of the row so we can modify values
        user_opts = o._asdict()

        # remove the values the game doesn't want
        user_opts.pop("id")
        user_opts.pop("user")

        return {"userId": data["userId"], "userOption": user_opts}

    def handle_get_user_data_api_request(self, data: Dict) -> Dict:
        p = self.data.profile.get_profile_data(data["userId"], self.version)
        if p is None:
            return {}

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

        # TODO: replace datetime objects with strings

        # add access code that we don't store
        user_data["accessCode"] = cards[0]["access_code"]

        return {"userId": data["userId"], "userData": user_data}

    def handle_get_user_event_ranking_api_request(self, data: Dict) -> Dict:
        # user_event_ranking_list = self.data.item.get_event_ranking(data["userId"])
        # if user_event_ranking_list is None: return {}

        evt_ranking = []
        # for evt in user_event_ranking_list:
        #    tmp = evt._asdict()
        #    tmp.pop("id")
        #    tmp.pop("user")
        #    evt_ranking.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(evt_ranking),
            "userEventRankingList": evt_ranking,
        }

    def handle_get_user_login_bonus_api_request(self, data: Dict) -> Dict:
        user_login_bonus_list = self.data.item.get_login_bonuses(data["userId"])
        if user_login_bonus_list is None:
            return {}

        login_bonuses = []
        for scenerio in user_login_bonus_list:
            tmp = scenerio._asdict()
            tmp.pop("id")
            tmp.pop("user")
            login_bonuses.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(login_bonuses),
            "userLoginBonusList": login_bonuses,
        }

    def handle_get_user_bp_base_request(self, data: Dict) -> Dict:
        p = self.data.profile.get_profile(
            self.game, self.version, user_id=data["userId"]
        )
        if p is None:
            return {}
        profile = json.loads(p["data"])
        return {
            "userId": data["userId"],
            "length": len(profile["userBpBaseList"]),
            "userBpBaseList": profile["userBpBaseList"],
        }

    def handle_get_user_recent_rating_api_request(self, data: Dict) -> Dict:
        recent_rating = self.data.profile.get_profile_recent_rating(data["userId"])
        if recent_rating is None:
            return {
                "userId": data["userId"],
                "length": 0,
                "userRecentRatingList": [],
            }

        userRecentRatingList = recent_rating["recentRating"]

        return {
            "userId": data["userId"],
            "length": len(userRecentRatingList),
            "userRecentRatingList": userRecentRatingList,
        }

    def handle_get_user_activity_api_request(self, data: Dict) -> Dict:
        activity = self.data.profile.get_profile_activity(data["userId"], data["kind"])
        if activity is None:
            return {}

        user_activity = []

        for act in activity:
            user_activity.append(
                {
                    "kind": act["kind"],
                    "id": act["activityId"],
                    "sortNumber": act["sortNumber"],
                    "param1": act["param1"],
                    "param2": act["param2"],
                    "param3": act["param3"],
                    "param4": act["param4"],
                }
            )

        return {
            "userId": data["userId"],
            "length": len(user_activity),
            "kind": data["kind"],
            "userActivityList": user_activity,
        }

    def handle_get_user_story_api_request(self, data: Dict) -> Dict:
        user_stories = self.data.item.get_stories(data["userId"])
        if user_stories is None:
            return {}

        story_list = []
        for story in user_stories:
            tmp = story._asdict()
            tmp.pop("id")
            tmp.pop("user")
            story_list.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(story_list),
            "userStoryList": story_list,
        }

    def handle_get_user_chapter_api_request(self, data: Dict) -> Dict:
        user_chapters = self.data.item.get_chapters(data["userId"])
        if user_chapters is None:
            return {}

        chapter_list = []
        for chapter in user_chapters:
            tmp = chapter._asdict()
            tmp.pop("id")
            tmp.pop("user")
            chapter_list.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(chapter_list),
            "userChapterList": chapter_list,
        }

    def handle_get_user_training_room_by_key_api_request(self, data: Dict) -> Dict:
        return {
            "userId": data["userId"],
            "length": 0,
            "userTrainingRoomList": [],
        }

    def handle_get_user_character_api_request(self, data: Dict) -> Dict:
        user_characters = self.data.item.get_characters(data["userId"])
        if user_characters is None:
            return {}

        character_list = []
        for character in user_characters:
            tmp = character._asdict()
            tmp.pop("id")
            tmp.pop("user")
            character_list.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(character_list),
            "userCharacterList": character_list,
        }

    def handle_get_user_card_api_request(self, data: Dict) -> Dict:
        user_cards = self.data.item.get_cards(data["userId"])
        if user_cards is None:
            return {}

        card_list = []
        for card in user_cards:
            tmp = card._asdict()
            tmp.pop("id")
            tmp.pop("user")
            card_list.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(card_list),
            "userCardList": card_list,
        }

    def handle_get_user_deck_by_key_api_request(self, data: Dict) -> Dict:
        # Auth key doesn't matter, it just wants all the decks
        decks = self.data.item.get_decks(data["userId"])
        if decks is None:
            return {}

        deck_list = []
        for deck in decks:
            tmp = deck._asdict()
            tmp.pop("user")
            tmp.pop("id")
            deck_list.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(deck_list),
            "userDeckList": deck_list,
        }

    def handle_get_user_trade_item_api_request(self, data: Dict) -> Dict:
        user_trade_items = self.data.item.get_trade_items(data["userId"])
        if user_trade_items is None:
            return {}

        trade_item_list = []
        for trade_item in user_trade_items:
            tmp = trade_item._asdict()
            tmp.pop("id")
            tmp.pop("user")
            trade_item_list.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(trade_item_list),
            "userTradeItemList": trade_item_list,
        }

    def handle_get_user_scenario_api_request(self, data: Dict) -> Dict:
        user_scenerio = self.data.item.get_scenerios(data["userId"])
        if user_scenerio is None:
            return {}

        scenerio_list = []
        for scenerio in user_scenerio:
            tmp = scenerio._asdict()
            tmp.pop("id")
            tmp.pop("user")
            scenerio_list.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(scenerio_list),
            "userScenarioList": scenerio_list,
        }

    def handle_get_user_ratinglog_api_request(self, data: Dict) -> Dict:
        rating_log = self.data.profile.get_profile_rating_log(data["userId"])
        if rating_log is None:
            return {}

        userRatinglogList = []
        for rating in rating_log:
            tmp = rating._asdict()
            tmp.pop("id")
            tmp.pop("user")
            userRatinglogList.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(userRatinglogList),
            "userRatinglogList": userRatinglogList,
        }

    def handle_get_user_mission_point_api_request(self, data: Dict) -> Dict:
        user_mission_point_list = self.data.item.get_mission_points(data["userId"])
        if user_mission_point_list is None:
            return {}

        mission_point_list = []
        for evt_music in user_mission_point_list:
            tmp = evt_music._asdict()
            tmp.pop("id")
            tmp.pop("user")
            mission_point_list.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(mission_point_list),
            "userMissionPointList": mission_point_list,
        }

    def handle_get_user_event_point_api_request(self, data: Dict) -> Dict:
        user_event_point_list = self.data.item.get_event_points(data["userId"])
        if user_event_point_list is None:
            return {}

        event_point_list = []
        for evt_music in user_event_point_list:
            tmp = evt_music._asdict()
            tmp.pop("id")
            tmp.pop("user")
            event_point_list.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(event_point_list),
            "userEventPointList": event_point_list,
        }

    def handle_get_user_music_item_api_request(self, data: Dict) -> Dict:
        user_music_item_list = self.data.item.get_music_items(data["userId"])
        if user_music_item_list is None:
            return {}

        music_item_list = []
        for evt_music in user_music_item_list:
            tmp = evt_music._asdict()
            tmp.pop("id")
            tmp.pop("user")
            music_item_list.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(music_item_list),
            "userMusicItemList": music_item_list,
        }

    def handle_get_user_event_music_api_request(self, data: Dict) -> Dict:
        user_evt_music_list = self.data.item.get_event_music(data["userId"])
        if user_evt_music_list is None:
            return {}

        evt_music_list = []
        for evt_music in user_evt_music_list:
            tmp = evt_music._asdict()
            tmp.pop("id")
            tmp.pop("user")
            evt_music_list.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(evt_music_list),
            "userEventMusicList": evt_music_list,
        }

    def handle_get_user_boss_api_request(self, data: Dict) -> Dict:
        p = self.data.item.get_bosses(data["userId"])
        if p is None:
            return {}

        boss_list = []
        for boss in p:
            tmp = boss._asdict()
            tmp.pop("id")
            tmp.pop("user")
            boss_list.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(boss_list),
            "userBossList": boss_list,
        }

    def handle_upsert_user_all_api_request(self, data: Dict) -> Dict:
        upsert = data["upsertUserAll"]
        user_id = data["userId"]

        # The isNew fields are new as of Red and up. We just won't use them for now.

        if "userData" in upsert and len(upsert["userData"]) > 0:
            self.data.profile.put_profile_data(
                user_id, self.version, upsert["userData"][0]
            )

        if "userOption" in upsert and len(upsert["userOption"]) > 0:
            self.data.profile.put_profile_options(user_id, upsert["userOption"][0])

        if "userPlaylogList" in upsert:
            for playlog in upsert["userPlaylogList"]:
                self.data.score.put_playlog(user_id, playlog)

        if "userActivityList" in upsert:
            for act in upsert["userActivityList"]:
                self.data.profile.put_profile_activity(
                    user_id,
                    act["kind"],
                    act["id"],
                    act["sortNumber"],
                    act["param1"],
                    act["param2"],
                    act["param3"],
                    act["param4"],
                )

        if "userRecentRatingList" in upsert:
            self.data.profile.put_profile_recent_rating(
                user_id, upsert["userRecentRatingList"]
            )

        if "userBpBaseList" in upsert:
            self.data.profile.put_profile_bp_list(user_id, upsert["userBpBaseList"])

        if "userMusicDetailList" in upsert:
            for x in upsert["userMusicDetailList"]:
                self.data.score.put_best_score(user_id, x)

        if "userCharacterList" in upsert:
            for x in upsert["userCharacterList"]:
                self.data.item.put_character(user_id, x)

        if "userCardList" in upsert:
            for x in upsert["userCardList"]:
                self.data.item.put_card(user_id, x)

        if "userDeckList" in upsert:
            for x in upsert["userDeckList"]:
                self.data.item.put_deck(user_id, x)

        if "userTrainingRoomList" in upsert:
            for x in upsert["userTrainingRoomList"]:
                self.data.profile.put_training_room(user_id, x)

        if "userStoryList" in upsert:
            for x in upsert["userStoryList"]:
                self.data.item.put_story(user_id, x)

        if "userChapterList" in upsert:
            for x in upsert["userChapterList"]:
                self.data.item.put_chapter(user_id, x)

        if "userMemoryChapterList" in upsert:
            for x in upsert["userMemoryChapterList"]:
                self.data.item.put_memorychapter(user_id, x)

        if "userItemList" in upsert:
            for x in upsert["userItemList"]:
                self.data.item.put_item(user_id, x)

        if "userMusicItemList" in upsert:
            for x in upsert["userMusicItemList"]:
                self.data.item.put_music_item(user_id, x)

        if "userLoginBonusList" in upsert:
            for x in upsert["userLoginBonusList"]:
                self.data.item.put_login_bonus(user_id, x)

        if "userEventPointList" in upsert:
            for x in upsert["userEventPointList"]:
                self.data.item.put_event_point(user_id, x)

        if "userMissionPointList" in upsert:
            for x in upsert["userMissionPointList"]:
                self.data.item.put_mission_point(user_id, x)

        if "userRatinglogList" in upsert:
            for x in upsert["userRatinglogList"]:
                self.data.profile.put_profile_rating_log(
                    user_id, x["dataVersion"], x["highestRating"]
                )

        if "userBossList" in upsert:
            for x in upsert["userBossList"]:
                self.data.item.put_boss(user_id, x)

        if "userTechCountList" in upsert:
            for x in upsert["userTechCountList"]:
                self.data.score.put_tech_count(user_id, x)

        if "userScenerioList" in upsert:
            for x in upsert["userScenerioList"]:
                self.data.item.put_scenerio(user_id, x)

        if "userTradeItemList" in upsert:
            for x in upsert["userTradeItemList"]:
                self.data.item.put_trade_item(user_id, x)

        if "userEventMusicList" in upsert:
            for x in upsert["userEventMusicList"]:
                self.data.item.put_event_music(user_id, x)

        if "userTechEventList" in upsert:
            for x in upsert["userTechEventList"]:
                self.data.item.put_tech_event(user_id, x)

        if "userKopList" in upsert:
            for x in upsert["userKopList"]:
                self.data.profile.put_kop(user_id, x)

        return {"returnCode": 1, "apiName": "upsertUserAll"}

    def handle_get_user_rival_api_request(self, data: Dict) -> Dict:
        """
        Added in Bright
        """

        rival_list = []
        user_rivals = self.data.profile.get_rivals(data["userId"])
        for rival in user_rivals:
            tmp = {}
            tmp["rivalUserId"] = rival[0]
            rival_list.append(tmp)

        if user_rivals is None or len(rival_list) < 1:
            return {
                "userId": data["userId"],
                "length": 0,
                "userRivalList": [],
            }
        return {
            "userId": data["userId"],
            "length": len(rival_list),
            "userRivalList": rival_list,
        }

    def handle_get_user_rival_data_api_request(self, data: Dict) -> Dict:
        """
        Added in Bright
        """
        rivals = []
        for rival in data["userRivalList"]:
            name = self.data.profile.get_profile_name(
                rival["rivalUserId"], self.version
            )
            if name is None:
                continue
            rivals.append({"rivalUserId": rival["rivalUserId"], "rivalUserName": name})
        return {
            "userId": data["userId"],
            "length": len(rivals),
            "userRivalDataList": rivals,
        }

    def handle_get_user_rival_music_api_request(self, data: Dict) -> Dict:
        """
        Added in Bright
        """
        rival_id = data["rivalUserId"]
        next_idx = data["nextIndex"]
        max_ct = data["maxCount"]
        music = self.handle_get_user_music_api_request(
            {"userId": rival_id, "nextIndex": next_idx, "maxCount": max_ct}
        )

        for song in music["userMusicList"]:
            song["userRivalMusicDetailList"] = song["userMusicDetailList"]
            song.pop("userMusicDetailList")
        print(music["userMusicList"])
        return {
            "userId": data["userId"],
            "rivalUserId": rival_id,
            "length": music["length"],
            "nextIndex": music["nextIndex"],
            "userRivalMusicList": music["userMusicList"],
        }

    @cached(2)
    def util_generate_music_list(self, user_id: int) -> List:
        music_detail = self.data.score.get_best_scores(user_id)
        song_list = []

        for md in music_detail:
            found = False
            tmp = md._asdict()
            tmp.pop("user")
            tmp.pop("id")

            for song in song_list:
                if song["userMusicDetailList"][0]["musicId"] == tmp["musicId"]:
                    found = True
                    song["userMusicDetailList"].append(tmp)
                    song["length"] = len(song["userMusicDetailList"])
                    break

            if not found:
                song_list.append({"length": 1, "userMusicDetailList": [tmp]})

        return song_list
