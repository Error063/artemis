from datetime import datetime, date, timedelta
from typing import Any, Dict
import logging

from core.config import CoreConfig
from titles.mai2.const import Mai2Constants
from titles.mai2.config import Mai2Config
from titles.mai2.database import Mai2Data


class Mai2Base:
    def __init__(self, cfg: CoreConfig, game_cfg: Mai2Config) -> None:
        self.core_config = cfg
        self.game_config = game_cfg
        self.version = Mai2Constants.VER_MAIMAI
        self.data = Mai2Data(cfg)
        self.logger = logging.getLogger("mai2")
        
        if self.core_config.server.is_develop and self.core_config.title.port > 0:
            self.old_server = f"http://{self.core_config.title.hostname}:{self.core_config.title.port}/SDEY/197/"
        
        else:
            self.old_server = f"http://{self.core_config.title.hostname}/SDEY/197/"

    def handle_get_game_setting_api_request(self, data: Dict):
        return {
            "gameSetting": {
                "isMaintenance": "false",
                "requestInterval": 10,
                "rebootStartTime": "2020-01-01 07:00:00.0",
                "rebootEndTime": "2020-01-01 07:59:59.0",
                "movieUploadLimit": 10000,
                "movieStatus": 0,
                "movieServerUri": "",
                "deliverServerUri": self.old_server + "deliver",
                "oldServerUri": self.old_server + "old",
                "usbDlServerUri": self.old_server + "usbdl",
                "rebootInterval": 0,
            },
            "isAouAccession": "true",
        }

    def handle_get_game_ranking_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "gameRankingList": []}

    def handle_get_game_tournament_info_api_request(self, data: Dict) -> Dict:
        # TODO: Tournament support
        return {"length": 0, "gameTournamentInfoList": []}

    def handle_get_game_event_api_request(self, data: Dict) -> Dict:
        events = self.data.static.get_enabled_events(self.version)
        print(self.version)
        events_lst = []
        if events is None or not events:
            self.logger.warn("No enabled events, did you run the reader?")
            return {"type": data["type"], "length": 0, "gameEventList": []}

        for event in events:
            events_lst.append(
                {
                    "type": event["type"],
                    "id": event["eventId"],
                    # actually use the startDate from the import so it
                    # properly shows all the events when new ones are imported
                    "startDate": datetime.strftime(
                        event["startDate"], f"{Mai2Constants.DATE_TIME_FORMAT}.0"
                    ),
                    "endDate": "2099-12-31 00:00:00.0",
                }
            )

        return {
            "type": data["type"],
            "length": len(events_lst),
            "gameEventList": events_lst,
        }

    def handle_get_game_ng_music_id_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "musicIdList": []}

    def handle_get_game_charge_api_request(self, data: Dict) -> Dict:
        game_charge_list = self.data.static.get_enabled_tickets(self.version, 1)
        if game_charge_list is None:
            return {"length": 0, "gameChargeList": []}

        charge_list = []
        for i, charge in enumerate(game_charge_list):
            charge_list.append(
                {
                    "orderId": i,
                    "chargeId": charge["ticketId"],
                    "price": charge["price"],
                    "startDate": "2017-12-05 07:00:00.0",
                    "endDate": "2099-12-31 00:00:00.0",
                }
            )

        return {"length": len(charge_list), "gameChargeList": charge_list}

    def handle_upsert_client_setting_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "UpsertClientSettingApi"}

    def handle_upsert_client_upload_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "UpsertClientUploadApi"}

    def handle_upsert_client_bookkeeping_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "UpsertClientBookkeepingApi"}

    def handle_upsert_client_testmode_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "UpsertClientTestmodeApi"}

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
            "lastDataVersion": profile["lastDataVersion"],
            "lastLoginDate": profile["lastLoginDate"],
            "lastPlayDate": profile["lastPlayDate"],
            "playerRating": profile["playerRating"],
            "nameplateId": 0,  # Unused            
            "frameId": profile["frameId"],
            "iconId": profile["iconId"],
            "trophyId": 0,  # Unused
            "partnerId": profile["partnerId"],
            "dispRate": option["dispRate"],  # 0: all, 1: dispRate, 2: dispDan, 3: hide
            "dispRank": 0,  # TODO
            "dispHomeRanker": 0,  # TODO
            "dispTotalLv": 0,  # TODO
            "totalLv": 0,  # TODO
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
