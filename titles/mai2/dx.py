from typing import Any, List, Dict
from datetime import datetime, timedelta
import pytz
import json
from random import randint

from core.config import CoreConfig
from titles.mai2.base import Mai2Base
from titles.mai2.config import Mai2Config
from titles.mai2.const import Mai2Constants


class Mai2DX(Mai2Base):
    def __init__(self, cfg: CoreConfig, game_cfg: Mai2Config) -> None:
        super().__init__(cfg, game_cfg)
        self.version = Mai2Constants.VER_MAIMAI_DX
        
        if self.core_config.server.is_develop and self.core_config.title.port > 0:
            self.old_server = f"http://{self.core_config.title.hostname}:{self.core_config.title.port}/SDEZ/100/"
        
        else:
            self.old_server = f"http://{self.core_config.title.hostname}/SDEZ/100/"

    def handle_get_user_preview_api_request(self, data: Dict) -> Dict:
        p = self.data.profile.get_profile_detail(data["userId"], self.version)
        o = self.data.profile.get_profile_option(data["userId"], self.version)
        if p is None or o is None:
            return {}  # Register
        profile = p._asdict()
        option = o._asdict()

        return {
            "userId": data["userId"],
            "userName": profile["userName"],
            "isLogin": False,
            "lastGameId": profile["lastGameId"],
            "lastDataVersion": profile["lastDataVersion"],
            "lastRomVersion": profile["lastRomVersion"],
            "lastLoginDate": profile["lastLoginDate"],
            "lastPlayDate": profile["lastPlayDate"],
            "playerRating": profile["playerRating"],
            "nameplateId": 0,  # Unused
            "iconId": profile["iconId"],
            "trophyId": 0,  # Unused
            "partnerId": profile["partnerId"],
            "frameId": profile["frameId"],
            "dispRate": option[
                "dispRate"
            ],  # 0: all/begin, 1: disprate, 2: dispDan, 3: hide, 4: end
            "totalAwake": profile["totalAwake"],
            "isNetMember": profile["isNetMember"],
            "dailyBonusDate": profile["dailyBonusDate"],
            "headPhoneVolume": option["headPhoneVolume"],
            "isInherit": False,  # Not sure what this is or does??
            "banState": profile["banState"]
            if profile["banState"] is not None
            else 0,  # New with uni+
        }

    def handle_user_login_api_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile_detail(data["userId"], self.version)

        if profile is not None:
            lastLoginDate = profile["lastLoginDate"]
            loginCt = profile["playCount"]

            if "regionId" in data:
                self.data.profile.put_profile_region(data["userId"], data["regionId"])
        else:
            loginCt = 0
            lastLoginDate = "2017-12-05 07:00:00.0"

        return {
            "returnCode": 1,
            "lastLoginDate": lastLoginDate,
            "loginCount": loginCt,
            "consecutiveLoginCount": 0,  # We don't really have a way to track this...
            "loginId": loginCt,  # Used with the playlog!
        }

    def handle_upload_user_playlog_api_request(self, data: Dict) -> Dict:
        user_id = data["userId"]
        playlog = data["userPlaylog"]

        self.data.score.put_playlog(user_id, playlog)

        return {"returnCode": 1, "apiName": "UploadUserPlaylogApi"}

    def handle_upsert_user_chargelog_api_request(self, data: Dict) -> Dict:
        user_id = data["userId"]
        charge = data["userCharge"]

        # remove the ".0" from the date string, festival only?
        charge["purchaseDate"] = charge["purchaseDate"].replace(".0", "")
        self.data.item.put_charge(
            user_id,
            charge["chargeId"],
            charge["stock"],
            datetime.strptime(charge["purchaseDate"], Mai2Constants.DATE_TIME_FORMAT),
            datetime.strptime(charge["validDate"], Mai2Constants.DATE_TIME_FORMAT),
        )

        return {"returnCode": 1, "apiName": "UpsertUserChargelogApi"}

    def handle_upsert_user_all_api_request(self, data: Dict) -> Dict:
        user_id = data["userId"]
        upsert = data["upsertUserAll"]

        if "userData" in upsert and len(upsert["userData"]) > 0:
            upsert["userData"][0]["isNetMember"] = 1
            upsert["userData"][0].pop("accessCode")
            self.data.profile.put_profile_detail(
                user_id, self.version, upsert["userData"][0]
            )

        if "userExtend" in upsert and len(upsert["userExtend"]) > 0:
            self.data.profile.put_profile_extend(
                user_id, self.version, upsert["userExtend"][0]
            )

        if "userGhost" in upsert:
            for ghost in upsert["userGhost"]:
                self.data.profile.put_profile_extend(user_id, self.version, ghost)

        if "userOption" in upsert and len(upsert["userOption"]) > 0:
            self.data.profile.put_profile_option(
                user_id, self.version, upsert["userOption"][0]
            )

        if "userRatingList" in upsert and len(upsert["userRatingList"]) > 0:
            self.data.profile.put_profile_rating(
                user_id, self.version, upsert["userRatingList"][0]
            )

        if "userActivityList" in upsert and len(upsert["userActivityList"]) > 0:
            for k, v in upsert["userActivityList"][0].items():
                for act in v:
                    self.data.profile.put_profile_activity(user_id, act)

        if "userChargeList" in upsert and len(upsert["userChargeList"]) > 0:
            for charge in upsert["userChargeList"]:
                # remove the ".0" from the date string, festival only?
                charge["purchaseDate"] = charge["purchaseDate"].replace(".0", "")
                self.data.item.put_charge(
                    user_id,
                    charge["chargeId"],
                    charge["stock"],
                    datetime.strptime(
                        charge["purchaseDate"], Mai2Constants.DATE_TIME_FORMAT
                    ),
                    datetime.strptime(
                        charge["validDate"], Mai2Constants.DATE_TIME_FORMAT
                    ),
                )

        if "userCharacterList" in upsert and len(upsert["userCharacterList"]) > 0:
            for char in upsert["userCharacterList"]:
                self.data.item.put_character(
                    user_id,
                    char["characterId"],
                    char["level"],
                    char["awakening"],
                    char["useCount"],
                )

        if "userItemList" in upsert and len(upsert["userItemList"]) > 0:
            for item in upsert["userItemList"]:
                self.data.item.put_item(
                    user_id,
                    int(item["itemKind"]),
                    item["itemId"],
                    item["stock"],
                    item["isValid"],
                )

        if "userLoginBonusList" in upsert and len(upsert["userLoginBonusList"]) > 0:
            for login_bonus in upsert["userLoginBonusList"]:
                self.data.item.put_login_bonus(
                    user_id,
                    login_bonus["bonusId"],
                    login_bonus["point"],
                    login_bonus["isCurrent"],
                    login_bonus["isComplete"],
                )

        if "userMapList" in upsert and len(upsert["userMapList"]) > 0:
            for map in upsert["userMapList"]:
                self.data.item.put_map(
                    user_id,
                    map["mapId"],
                    map["distance"],
                    map["isLock"],
                    map["isClear"],
                    map["isComplete"],
                )

        if "userMusicDetailList" in upsert and len(upsert["userMusicDetailList"]) > 0:
            for music in upsert["userMusicDetailList"]:
                self.data.score.put_best_score(user_id, music)

        if "userCourseList" in upsert and len(upsert["userCourseList"]) > 0:
            for course in upsert["userCourseList"]:
                self.data.score.put_course(user_id, course)

        if "userFavoriteList" in upsert and len(upsert["userFavoriteList"]) > 0:
            for fav in upsert["userFavoriteList"]:
                self.data.item.put_favorite(user_id, fav["kind"], fav["itemIdList"])

        if (
            "userFriendSeasonRankingList" in upsert
            and len(upsert["userFriendSeasonRankingList"]) > 0
        ):
            for fsr in upsert["userFriendSeasonRankingList"]:
                fsr["recordDate"] = (
                    datetime.strptime(
                        fsr["recordDate"], f"{Mai2Constants.DATE_TIME_FORMAT}.0"
                    ),
                )
                self.data.item.put_friend_season_ranking(user_id, fsr)

        return {"returnCode": 1, "apiName": "UpsertUserAllApi"}

    def handle_user_logout_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1}

    def handle_get_user_data_api_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile_detail(data["userId"], self.version)
        if profile is None:
            return

        profile_dict = profile._asdict()
        profile_dict.pop("id")
        profile_dict.pop("user")
        profile_dict.pop("version")

        return {"userId": data["userId"], "userData": profile_dict}

    def handle_get_user_extend_api_request(self, data: Dict) -> Dict:
        extend = self.data.profile.get_profile_extend(data["userId"], self.version)
        if extend is None:
            return

        extend_dict = extend._asdict()
        extend_dict.pop("id")
        extend_dict.pop("user")
        extend_dict.pop("version")

        return {"userId": data["userId"], "userExtend": extend_dict}

    def handle_get_user_option_api_request(self, data: Dict) -> Dict:
        options = self.data.profile.get_profile_option(data["userId"], self.version)
        if options is None:
            return

        options_dict = options._asdict()
        options_dict.pop("id")
        options_dict.pop("user")
        options_dict.pop("version")

        return {"userId": data["userId"], "userOption": options_dict}

    def handle_get_user_card_api_request(self, data: Dict) -> Dict:
        user_cards = self.data.item.get_cards(data["userId"])
        if user_cards is None:
            return {"userId": data["userId"], "nextIndex": 0, "userCardList": []}

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
            tmp["startDate"] = datetime.strftime(
                tmp["startDate"], Mai2Constants.DATE_TIME_FORMAT
            )
            tmp["endDate"] = datetime.strftime(
                tmp["endDate"], Mai2Constants.DATE_TIME_FORMAT
            )
            card_list.append(tmp)

        return {
            "userId": data["userId"],
            "nextIndex": next_idx,
            "userCardList": card_list[start_idx:end_idx],
        }

    def handle_get_user_charge_api_request(self, data: Dict) -> Dict:
        user_charges = self.data.item.get_charges(data["userId"])
        if user_charges is None:
            return {"userId": data["userId"], "length": 0, "userChargeList": []}

        user_charge_list = []
        for charge in user_charges:
            tmp = charge._asdict()
            tmp.pop("id")
            tmp.pop("user")
            tmp["purchaseDate"] = datetime.strftime(
                tmp["purchaseDate"], Mai2Constants.DATE_TIME_FORMAT
            )
            tmp["validDate"] = datetime.strftime(
                tmp["validDate"], Mai2Constants.DATE_TIME_FORMAT
            )

            user_charge_list.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(user_charge_list),
            "userChargeList": user_charge_list,
        }

    def handle_get_user_item_api_request(self, data: Dict) -> Dict:
        kind = int(data["nextIndex"] / 10000000000)
        next_idx = int(data["nextIndex"] % 10000000000)
        user_item_list = self.data.item.get_items(data["userId"], kind)

        items: list[Dict[str, Any]] = []
        for i in range(next_idx, len(user_item_list)):
            tmp = user_item_list[i]._asdict()
            tmp.pop("user")
            tmp.pop("id")
            items.append(tmp)
            if len(items) >= int(data["maxCount"]):
                break

        xout = kind * 10000000000 + next_idx + len(items)

        if len(items) < int(data["maxCount"]):
            next_idx = 0
        else:
            next_idx = xout

        return {
            "userId": data["userId"],
            "nextIndex": next_idx,
            "itemKind": kind,
            "userItemList": items,
        }

    def handle_get_user_character_api_request(self, data: Dict) -> Dict:
        characters = self.data.item.get_characters(data["userId"])

        chara_list = []
        for chara in characters:
            tmp = chara._asdict()
            tmp.pop("id")
            tmp.pop("user")
            chara_list.append(tmp)

        return {"userId": data["userId"], "userCharacterList": chara_list}

    def handle_get_user_favorite_api_request(self, data: Dict) -> Dict:
        favorites = self.data.item.get_favorites(data["userId"], data["itemKind"])
        if favorites is None:
            return

        userFavs = []
        for fav in favorites:
            userFavs.append(
                {
                    "userId": data["userId"],
                    "itemKind": fav["itemKind"],
                    "itemIdList": fav["itemIdList"],
                }
            )

        return {"userId": data["userId"], "userFavoriteData": userFavs}

    def handle_get_user_ghost_api_request(self, data: Dict) -> Dict:
        ghost = self.data.profile.get_profile_ghost(data["userId"], self.version)
        if ghost is None:
            return

        ghost_dict = ghost._asdict()
        ghost_dict.pop("user")
        ghost_dict.pop("id")
        ghost_dict.pop("version_int")

        return {"userId": data["userId"], "userGhost": ghost_dict}

    def handle_get_user_rating_api_request(self, data: Dict) -> Dict:
        rating = self.data.profile.get_profile_rating(data["userId"], self.version)
        if rating is None:
            return

        rating_dict = rating._asdict()
        rating_dict.pop("user")
        rating_dict.pop("id")
        rating_dict.pop("version")

        return {"userId": data["userId"], "userRating": rating_dict}

    def handle_get_user_activity_api_request(self, data: Dict) -> Dict:
        """
        kind 1 is playlist, kind 2 is music list
        """
        playlist = self.data.profile.get_profile_activity(data["userId"], 1)
        musiclist = self.data.profile.get_profile_activity(data["userId"], 2)
        if playlist is None or musiclist is None:
            return

        plst = []
        mlst = []

        for play in playlist:
            tmp = play._asdict()
            tmp["id"] = tmp["activityId"]
            tmp.pop("activityId")
            tmp.pop("user")
            plst.append(tmp)

        for music in musiclist:
            tmp = music._asdict()
            tmp["id"] = tmp["activityId"]
            tmp.pop("activityId")
            tmp.pop("user")
            mlst.append(tmp)

        return {"userActivity": {"playList": plst, "musicList": mlst}}

    def handle_get_user_course_api_request(self, data: Dict) -> Dict:
        user_courses = self.data.score.get_courses(data["userId"])
        if user_courses is None:
            return {"userId": data["userId"], "nextIndex": 0, "userCourseList": []}

        course_list = []
        for course in user_courses:
            tmp = course._asdict()
            tmp.pop("user")
            tmp.pop("id")
            course_list.append(tmp)

        return {"userId": data["userId"], "nextIndex": 0, "userCourseList": course_list}

    def handle_get_user_portrait_api_request(self, data: Dict) -> Dict:
        # No support for custom pfps
        return {"length": 0, "userPortraitList": []}

    def handle_get_user_friend_season_ranking_api_request(self, data: Dict) -> Dict:
        friend_season_ranking = self.data.item.get_friend_season_ranking(data["userId"])
        if friend_season_ranking is None:
            return {
                "userId": data["userId"],
                "nextIndex": 0,
                "userFriendSeasonRankingList": [],
            }

        friend_season_ranking_list = []
        next_idx = int(data["nextIndex"])
        max_ct = int(data["maxCount"])

        for x in range(next_idx, len(friend_season_ranking)):
            tmp = friend_season_ranking[x]._asdict()
            tmp.pop("user")
            tmp.pop("id")
            tmp["recordDate"] = datetime.strftime(
                tmp["recordDate"], f"{Mai2Constants.DATE_TIME_FORMAT}.0"
            )
            friend_season_ranking_list.append(tmp)

            if len(friend_season_ranking_list) >= max_ct:
                break

        if len(friend_season_ranking) >= next_idx + max_ct:
            next_idx += max_ct
        else:
            next_idx = 0

        return {
            "userId": data["userId"],
            "nextIndex": next_idx,
            "userFriendSeasonRankingList": friend_season_ranking_list,
        }

    def handle_get_user_map_api_request(self, data: Dict) -> Dict:
        maps = self.data.item.get_maps(data["userId"])
        if maps is None:
            return {
                "userId": data["userId"],
                "nextIndex": 0,
                "userMapList": [],
            }

        map_list = []
        next_idx = int(data["nextIndex"])
        max_ct = int(data["maxCount"])

        for x in range(next_idx, len(maps)):
            tmp = maps[x]._asdict()
            tmp.pop("user")
            tmp.pop("id")
            map_list.append(tmp)

            if len(map_list) >= max_ct:
                break

        if len(maps) >= next_idx + max_ct:
            next_idx += max_ct
        else:
            next_idx = 0

        return {
            "userId": data["userId"],
            "nextIndex": next_idx,
            "userMapList": map_list,
        }

    def handle_get_user_login_bonus_api_request(self, data: Dict) -> Dict:
        login_bonuses = self.data.item.get_login_bonuses(data["userId"])
        if login_bonuses is None:
            return {
                "userId": data["userId"],
                "nextIndex": 0,
                "userLoginBonusList": [],
            }

        login_bonus_list = []
        next_idx = int(data["nextIndex"])
        max_ct = int(data["maxCount"])

        for x in range(next_idx, len(login_bonuses)):
            tmp = login_bonuses[x]._asdict()
            tmp.pop("user")
            tmp.pop("id")
            login_bonus_list.append(tmp)

            if len(login_bonus_list) >= max_ct:
                break

        if len(login_bonuses) >= next_idx + max_ct:
            next_idx += max_ct
        else:
            next_idx = 0

        return {
            "userId": data["userId"],
            "nextIndex": next_idx,
            "userLoginBonusList": login_bonus_list,
        }

    def handle_get_user_region_api_request(self, data: Dict) -> Dict:
        return {"userId": data["userId"], "length": 0, "userRegionList": []}

    def handle_get_user_music_api_request(self, data: Dict) -> Dict:
        songs = self.data.score.get_best_scores(data["userId"])
        music_detail_list = []
        next_index = 0

        if songs is not None:
            for song in songs:
                tmp = song._asdict()
                tmp.pop("id")
                tmp.pop("user")
                music_detail_list.append(tmp)

                if len(music_detail_list) == data["maxCount"]:
                    next_index = data["maxCount"] + data["nextIndex"]
                    break

        return {
            "userId": data["userId"],
            "nextIndex": next_index,
            "userMusicList": [{"userMusicDetailList": music_detail_list}],
        }

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
