from datetime import datetime, timedelta
from typing import Any, Dict, List
import logging
from base64 import b64decode
from os import path, stat, remove
from PIL import ImageFile

import pytz
from core.config import CoreConfig
from core.utils import Utils
from .const import Mai2Constants
from .config import Mai2Config
from .database import Mai2Data


class Mai2Base:
    def __init__(self, cfg: CoreConfig, game_cfg: Mai2Config) -> None:
        self.core_config = cfg
        self.game_config = game_cfg
        self.version = Mai2Constants.VER_MAIMAI
        self.data = Mai2Data(cfg)
        self.logger = logging.getLogger("mai2")
        self.can_deliver = False
        self.can_usbdl = False
        self.old_server = ""
        self.date_time_format = "%Y-%m-%d %H:%M:%S"

        if not self.core_config.server.is_using_proxy and Utils.get_title_port(self.core_config) != 80:
            self.old_server = f"http://{self.core_config.server.hostname}:{Utils.get_title_port(cfg)}/197/MaimaiServlet/"

        else:
            self.old_server = f"http://{self.core_config.server.hostname}/197/MaimaiServlet/"

    async def handle_get_game_setting_api_request(self, data: Dict):
        # if reboot start/end time is not defined use the default behavior of being a few hours ago
        if self.core_config.title.reboot_start_time == "" or self.core_config.title.reboot_end_time == "":
            reboot_start = datetime.strftime(
                datetime.utcnow() + timedelta(hours=6), self.date_time_format
            )
            reboot_end = datetime.strftime(
                datetime.utcnow() + timedelta(hours=7), self.date_time_format
            )
        else:
            # get current datetime in JST
            current_jst = datetime.now(pytz.timezone('Asia/Tokyo')).date()

            # parse config start/end times into datetime
            reboot_start_time = datetime.strptime(self.core_config.title.reboot_start_time, "%H:%M")
            reboot_end_time = datetime.strptime(self.core_config.title.reboot_end_time, "%H:%M")

            # offset datetimes with current date/time
            reboot_start_time = reboot_start_time.replace(year=current_jst.year, month=current_jst.month, day=current_jst.day, tzinfo=pytz.timezone('Asia/Tokyo'))
            reboot_end_time = reboot_end_time.replace(year=current_jst.year, month=current_jst.month, day=current_jst.day, tzinfo=pytz.timezone('Asia/Tokyo'))

            # create strings for use in gameSetting
            reboot_start = reboot_start_time.strftime(self.date_time_format)
            reboot_end = reboot_end_time.strftime(self.date_time_format)


        return {
            "isDevelop": False,
            "isAouAccession": False,
            "gameSetting": {
                "isMaintenance": False,
                "requestInterval": 1800,
                "rebootStartTime": reboot_start,
                "rebootEndTime": reboot_end,
                "movieUploadLimit": 100,
                "movieStatus": 1,
                "movieServerUri": self.old_server + "api/movie" if self.game_config.uploads.movies else "movie",
                "deliverServerUri": self.old_server + "deliver/" if self.can_deliver and self.game_config.deliver.enable else "",
                "oldServerUri": self.old_server + "old",
                "usbDlServerUri": self.old_server + "usbdl/" if self.can_deliver and self.game_config.deliver.udbdl_enable else "",
            },
        }

    async def handle_get_game_ranking_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "gameRankingList": []}

    async def handle_get_game_tournament_info_api_request(self, data: Dict) -> Dict:
        # TODO: Tournament support
        return {"length": 0, "gameTournamentInfoList": []}

    async def handle_get_game_event_api_request(self, data: Dict) -> Dict:
        events = self.data.static.get_enabled_events(self.version)
        events_lst = []
        if events is None or not events:
            self.logger.warning("No enabled events, did you run the reader?")
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

    async def handle_get_game_ng_music_id_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "musicIdList": []}

    async def handle_get_game_charge_api_request(self, data: Dict) -> Dict:
        game_charge_list = self.data.static.get_enabled_tickets(self.version, 1)
        if game_charge_list is None:
            return {"length": 0, "gameChargeList": []}

        charge_list = []
        for i, charge in enumerate(game_charge_list):
            charge_list.append(
                {
                    "orderId": i + 1,
                    "chargeId": charge["ticketId"],
                    "price": charge["price"],
                    "startDate": "2017-12-05 07:00:00.0",
                    "endDate": "2099-12-31 00:00:00.0",
                }
            )

        return {"length": len(charge_list), "gameChargeList": charge_list}

    async def handle_upsert_client_setting_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "UpsertClientSettingApi"}

    async def handle_upsert_client_upload_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "UpsertClientUploadApi"}

    async def handle_upsert_client_bookkeeping_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "UpsertClientBookkeepingApi"}

    async def handle_upsert_client_testmode_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1, "apiName": "UpsertClientTestmodeApi"}

    async def handle_get_user_preview_api_request(self, data: Dict) -> Dict:
        p = self.data.profile.get_profile_detail(data["userId"], self.version, False)
        w = self.data.profile.get_web_option(data["userId"], self.version)
        if p is None or w is None:
            return {}  # Register
        profile = p._asdict()
        web_opt = w._asdict()

        return {
            "userId": data["userId"],
            "userName": profile["userName"],
            "isLogin": False,
            "lastDataVersion": profile["lastDataVersion"],
            "lastLoginDate": profile["lastPlayDate"],
            "lastPlayDate": profile["lastPlayDate"],
            "playerRating": profile["playerRating"],
            "nameplateId": profile["nameplateId"],
            "frameId": profile["frameId"],
            "iconId": profile["iconId"],
            "trophyId": profile["trophyId"],
            "dispRate": web_opt["dispRate"],  # 0: all, 1: dispRate, 2: dispDan, 3: hide
            "dispRank": web_opt["dispRank"],
            "dispHomeRanker": web_opt["dispHomeRanker"],
            "dispTotalLv": web_opt["dispTotalLv"],
            "totalLv": profile["totalLv"],
        }

    async def handle_user_login_api_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile_detail(data["userId"], self.version)
        consec = self.data.profile.get_consec_login(data["userId"], self.version)

        if profile is not None:
            lastLoginDate = profile["lastLoginDate"]
            loginCt = profile["playCount"]

            if "regionId" in data:
                self.data.profile.put_profile_region(data["userId"], data["regionId"])
        else:
            loginCt = 0
            lastLoginDate = "2017-12-05 07:00:00.0"
        
        if consec is None or not consec:
            consec_ct = 1
        
        else:
            lastlogindate_ = datetime.strptime(profile["lastLoginDate"], "%Y-%m-%d %H:%M:%S.%f").timestamp()
            today_midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
            yesterday_midnight = today_midnight - 86400

            if lastlogindate_ < today_midnight:
                consec_ct = consec['logins'] + 1                
                self.data.profile.add_consec_login(data["userId"], self.version)
            
            elif lastlogindate_ < yesterday_midnight:
                consec_ct = 1
                self.data.profile.reset_consec_login(data["userId"], self.version)

            else:
                consec_ct = consec['logins']
        

        return {
            "returnCode": 1,
            "lastLoginDate": lastLoginDate,
            "loginCount": loginCt,
            "consecutiveLoginCount": consec_ct, # Number of consecutive days we've logged in.
        }

    async def handle_upload_user_playlog_api_request(self, data: Dict) -> Dict:
        user_id = data["userId"]
        playlog = data["userPlaylog"]

        self.data.score.put_playlog(user_id, playlog)

        return {"returnCode": 1, "apiName": "UploadUserPlaylogApi"}

    async def handle_upsert_user_chargelog_api_request(self, data: Dict) -> Dict:
        user_id = data["userId"]
        charge = data["userCharge"]

        # remove the ".0" from the date string, festival only?
        charge["purchaseDate"] = charge["purchaseDate"].replace(".0", "")
        self.data.item.put_charge(
            user_id,
            charge["chargeId"],
            charge["stock"],
            charge["purchaseDate"], # Ideally these should be datetimes, but db was
            charge["validDate"] # set up with them being str, so str it is for now
        )

        return {"returnCode": 1, "apiName": "UpsertUserChargelogApi"}

    async def handle_upsert_user_all_api_request(self, data: Dict) -> Dict:
        user_id = data["userId"]
        upsert = data["upsertUserAll"]
        
        if int(user_id) & 1000000000001 == 1000000000001:
            self.logger.info("Guest play, ignoring.")
            return {"returnCode": 1, "apiName": "UpsertUserAllApi"}

        if "userData" in upsert and len(upsert["userData"]) > 0:
            upsert["userData"][0].pop("accessCode")
            upsert["userData"][0].pop("userId")

            self.data.profile.put_profile_detail(
                user_id, self.version, upsert["userData"][0], False
            )
        
        if "userWebOption" in upsert and len(upsert["userWebOption"]) > 0:            
            upsert["userWebOption"][0]["isNetMember"] = True
            self.data.profile.put_web_option(
                user_id, self.version, upsert["userWebOption"][0]
            )

        if "userGradeStatusList" in upsert and len(upsert["userGradeStatusList"]) > 0:
            self.data.profile.put_grade_status(
                user_id, upsert["userGradeStatusList"][0]
            )

        if "userBossList" in upsert and len(upsert["userBossList"]) > 0:
            self.data.profile.put_boss_list(
                user_id, upsert["userBossList"][0]
            )

        if "userPlaylogList" in upsert and len(upsert["userPlaylogList"]) > 0:
            for playlog in upsert["userPlaylogList"]:
                self.data.score.put_playlog(
                    user_id, playlog, False
                )

        if "userExtend" in upsert and len(upsert["userExtend"]) > 0:
            self.data.profile.put_profile_extend(
                user_id, self.version, upsert["userExtend"][0]
            )

        if "userGhost" in upsert:
            for ghost in upsert["userGhost"]:
                self.data.profile.put_profile_ghost(user_id, self.version, ghost)

        if "userRecentRatingList" in upsert:
            self.data.profile.put_recent_rating(user_id, upsert["userRecentRatingList"])

        if "userOption" in upsert and len(upsert["userOption"]) > 0:
            upsert["userOption"][0].pop("userId")
            self.data.profile.put_profile_option(
                user_id, self.version, upsert["userOption"][0], False
            )

        if "userRatingList" in upsert and len(upsert["userRatingList"]) > 0:
            self.data.profile.put_profile_rating(
                user_id, self.version, upsert["userRatingList"][0]
            )

        if "userActivityList" in upsert and len(upsert["userActivityList"]) > 0:
            for act in upsert["userActivityList"]:
                self.data.profile.put_profile_activity(user_id, act)

        if "userChargeList" in upsert and len(upsert["userChargeList"]) > 0:
            for charge in upsert["userChargeList"]:
                # remove the ".0" from the date string, festival only?
                charge["purchaseDate"] = charge["purchaseDate"].replace(".0", "")
                self.data.item.put_charge(
                    user_id,
                    charge["chargeId"],
                    charge["stock"],
                    charge["purchaseDate"],
                    charge["validDate"]
                )

        if "userCharacterList" in upsert and len(upsert["userCharacterList"]) > 0:
            for char in upsert["userCharacterList"]:
                self.data.item.put_character_(
                    user_id,
                    char
                )

        if "userItemList" in upsert and len(upsert["userItemList"]) > 0:
            for item in upsert["userItemList"]:
                self.data.item.put_item(
                    user_id,
                    int(item["itemKind"]),
                    item["itemId"],
                    item["stock"],
                    True
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
                self.data.score.put_best_score(user_id, music, False)

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

    async def handle_user_logout_api_request(self, data: Dict) -> Dict:
        return {"returnCode": 1}

    async def handle_get_user_data_api_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile_detail(data["userId"], self.version, False)
        if profile is None:
            return

        profile_dict = profile._asdict()
        profile_dict.pop("id")
        profile_dict.pop("user")
        profile_dict.pop("version")

        return {"userId": data["userId"], "userData": profile_dict}

    async def handle_get_user_extend_api_request(self, data: Dict) -> Dict:
        extend = self.data.profile.get_profile_extend(data["userId"], self.version)
        if extend is None:
            return

        extend_dict = extend._asdict()
        extend_dict.pop("id")
        extend_dict.pop("user")
        extend_dict.pop("version")

        return {"userId": data["userId"], "userExtend": extend_dict}

    async def handle_get_user_option_api_request(self, data: Dict) -> Dict:
        options = self.data.profile.get_profile_option(data["userId"], self.version, False)
        if options is None:
            return

        options_dict = options._asdict()
        options_dict.pop("id")
        options_dict.pop("user")
        options_dict.pop("version")

        return {"userId": data["userId"], "userOption": options_dict}

    async def handle_get_user_card_api_request(self, data: Dict) -> Dict:
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

    async def handle_get_user_charge_api_request(self, data: Dict) -> Dict:
        user_charges = self.data.item.get_charges(data["userId"])
        if user_charges is None:
            return {"userId": data["userId"], "length": 0, "userChargeList": []}

        user_charge_list = []
        for charge in user_charges:
            tmp = charge._asdict()
            tmp.pop("id")
            tmp.pop("user")

            user_charge_list.append(tmp)

        return {
            "userId": data["userId"],
            "length": len(user_charge_list),
            "userChargeList": user_charge_list,
        }

    async def handle_get_user_present_api_request(self, data: Dict) -> Dict:
        return { "userId": data.get("userId", 0), "length": 0, "userPresentList": []}
    
    async def handle_get_transfer_friend_api_request(self, data: Dict) -> Dict:
        return {}

    async def handle_get_user_present_event_api_request(self, data: Dict) -> Dict:
        return { "userId": data.get("userId", 0), "length": 0, "userPresentEventList": []}
    
    async def handle_get_user_boss_api_request(self, data: Dict) -> Dict:
        b = self.data.profile.get_boss_list(data["userId"])
        if b is None:
            return { "userId": data.get("userId", 0), "userBossData": {}}
        boss_lst = b._asdict()
        boss_lst.pop("id")
        boss_lst.pop("user")

        return { "userId": data.get("userId", 0), "userBossData": boss_lst}

    async def handle_get_user_item_api_request(self, data: Dict) -> Dict:
        kind = int(data["nextIndex"] / 10000000000)
        next_idx = int(data["nextIndex"] % 10000000000)
        user_item_list = self.data.item.get_items(data["userId"], kind)

        items: List[Dict[str, Any]] = []
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

    async def handle_get_user_character_api_request(self, data: Dict) -> Dict:
        characters = self.data.item.get_characters(data["userId"])

        chara_list = []
        for chara in characters:
            tmp = chara._asdict()
            tmp.pop("id")
            tmp.pop("user")
            tmp.pop("awakening")
            tmp.pop("useCount")
            chara_list.append(tmp)

        return {"userId": data["userId"], "userCharacterList": chara_list}

    async def handle_get_user_favorite_api_request(self, data: Dict) -> Dict:
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

    async def handle_get_user_ghost_api_request(self, data: Dict) -> Dict:
        ghost = self.data.profile.get_profile_ghost(data["userId"], self.version)
        if ghost is None:
            return

        ghost_dict = ghost._asdict()
        ghost_dict.pop("user")
        ghost_dict.pop("id")
        ghost_dict.pop("version_int")

        return {"userId": data["userId"], "userGhost": ghost_dict}

    async def handle_get_user_recent_rating_api_request(self, data: Dict) -> Dict:
        rating = self.data.profile.get_recent_rating(data["userId"])
        if rating is None:
            return
        
        r = rating._asdict()
        lst = r.get("userRecentRatingList", [])
        
        return {"userId": data["userId"], "length": len(lst), "userRecentRatingList": lst}

    async def handle_get_user_rating_api_request(self, data: Dict) -> Dict:
        rating = self.data.profile.get_profile_rating(data["userId"], self.version)
        if rating is None:
            return

        rating_dict = rating._asdict()
        rating_dict.pop("user")
        rating_dict.pop("id")
        rating_dict.pop("version")

        return {"userId": data["userId"], "userRating": rating_dict}

    async def handle_get_user_activity_api_request(self, data: Dict) -> Dict:
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

    async def handle_get_user_course_api_request(self, data: Dict) -> Dict:
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

    async def handle_get_user_portrait_api_request(self, data: Dict) -> Dict:
        # No support for custom pfps
        return {"length": 0, "userPortraitList": []}

    async def handle_get_user_friend_season_ranking_api_request(self, data: Dict) -> Dict:
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

    async def handle_get_user_map_api_request(self, data: Dict) -> Dict:
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

    async def handle_get_user_login_bonus_api_request(self, data: Dict) -> Dict:
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

    async def handle_get_user_region_api_request(self, data: Dict) -> Dict:
        return {"userId": data["userId"], "length": 0, "userRegionList": []}
    
    async def handle_get_user_web_option_api_request(self, data: Dict) -> Dict:
        w = self.data.profile.get_web_option(data["userId"], self.version)
        if  w is None:
            return {"userId": data["userId"], "userWebOption": {}}
        
        web_opt = w._asdict()        
        web_opt.pop("id")
        web_opt.pop("user")
        web_opt.pop("version")

        return {"userId": data["userId"], "userWebOption": web_opt}

    async def handle_get_user_survival_api_request(self, data: Dict) -> Dict:
        return {"userId": data["userId"], "length": 0, "userSurvivalList": []}

    async def handle_get_user_grade_api_request(self, data: Dict) -> Dict:
        g = self.data.profile.get_grade_status(data["userId"])
        if g is None:
            return {"userId": data["userId"], "userGradeStatus": {}, "length": 0, "userGradeList": []}
        grade_stat = g._asdict()
        grade_stat.pop("id")
        grade_stat.pop("user")

        return {"userId": data["userId"], "userGradeStatus": grade_stat, "length": 0, "userGradeList": []}

    async def handle_get_user_music_api_request(self, data: Dict) -> Dict:
        user_id = data.get("userId", 0)        
        next_index = data.get("nextIndex", 0)
        max_ct = data.get("maxCount", 50)
        upper_lim = next_index + max_ct
        music_detail_list = []

        if user_id <= 0:
            self.logger.warning("handle_get_user_music_api_request: Could not find userid in data, or userId is 0")
            return {}
        
        songs = self.data.score.get_best_scores(user_id, is_dx=False)
        if songs is None:
            self.logger.debug("handle_get_user_music_api_request: get_best_scores returned None!")
            return {
            "userId": data["userId"],
            "nextIndex": 0,
            "userMusicList": [],
        }

        num_user_songs = len(songs)

        for x in range(next_index, upper_lim):
            if num_user_songs <= x:
                break

            tmp = songs[x]._asdict()
            tmp.pop("id")
            tmp.pop("user")
            music_detail_list.append(tmp)

        next_index = 0 if len(music_detail_list) < max_ct or num_user_songs == upper_lim else upper_lim
        self.logger.info(f"Send songs {next_index}-{upper_lim} ({len(music_detail_list)}) out of {num_user_songs} for user {user_id} (next idx {next_index})")
        return {
            "userId": data["userId"],
            "nextIndex": next_index,
            "userMusicList": [{"userMusicDetailList": music_detail_list}],
        }

    async def handle_upload_user_portrait_api_request(self, data: Dict) -> Dict:
        self.logger.debug(data)

    async def handle_upload_user_photo_api_request(self, data: Dict) -> Dict:
        if not self.game_config.uploads.photos or not self.game_config.uploads.photos_dir:
            return {'returnCode': 0, 'apiName': 'UploadUserPhotoApi'}

        photo = data.get("userPhoto", {})

        if photo is None or not photo:
            return {'returnCode': 0, 'apiName': 'UploadUserPhotoApi'}
        
        order_id = int(photo.get("orderId", -1))
        user_id = int(photo.get("userId", -1))
        div_num = int(photo.get("divNumber", -1))
        div_len = int(photo.get("divLength", -1))
        div_data = photo.get("divData", "")
        playlog_id = int(photo.get("playlogId", -1))
        track_num = int(photo.get("trackNo", -1))
        upload_date = photo.get("uploadDate", "")

        if order_id < 0 or user_id <= 0 or div_num < 0 or div_len <= 0 or not div_data or playlog_id < 0 or track_num <= 0 or not upload_date:
            self.logger.warning(f"Malformed photo upload request")
            return {'returnCode': 0, 'apiName': 'UploadUserPhotoApi'}
        
        if order_id == 0 and div_num > 0:
            self.logger.warning(f"Failed to set orderId properly (still 0 after first chunk)")
            return {'returnCode': 0, 'apiName': 'UploadUserPhotoApi'}

        if div_num == 0 and order_id > 0:
            self.logger.warning(f"First chuck re-send, Ignore")
            return {'returnCode': 0, 'apiName': 'UploadUserPhotoApi'}
        
        if div_num >= div_len:
            self.logger.warning(f"Sent extra chunks ({div_num} >= {div_len})")
            return {'returnCode': 0, 'apiName': 'UploadUserPhotoApi'}

        if div_len >= 100:
            self.logger.warning(f"Photo too large ({div_len} * 10240 = {div_len * 10240} bytes)")
            return {'returnCode': 0, 'apiName': 'UploadUserPhotoApi'}
        
        ret_code = order_id + 1
        photo_chunk = b64decode(div_data)

        if len(photo_chunk) > 10240 or (len(photo_chunk) < 10240 and div_num + 1 != div_len):
            self.logger.warning(f"Incorrect data size after decoding (Expected 10240, got {len(photo_chunk)})")
            return {'returnCode': 0, 'apiName': 'UploadUserPhotoApi'}
        
        out_name = f"{self.game_config.uploads.photos_dir}/{user_id}_{playlog_id}_{track_num}"

        if not path.exists(f"{out_name}.bin") and div_num != 0:
            self.logger.warning(f"Out of order photo upload (div_num {div_num})")
            return {'returnCode': 0, 'apiName': 'UploadUserPhotoApi'}
    
        if path.exists(f"{out_name}.bin") and div_num == 0:
            self.logger.warning(f"Duplicate file upload")
            return {'returnCode': 0, 'apiName': 'UploadUserPhotoApi'}
        
        elif path.exists(f"{out_name}.bin"):
            fstats = stat(f"{out_name}.bin")
            if fstats.st_size != 10240 * div_num:
                self.logger.warning(f"Out of order photo upload (trying to upload div {div_num}, expected div {fstats.st_size / 10240} for file sized {fstats.st_size} bytes)")
                return {'returnCode': 0, 'apiName': 'UploadUserPhotoApi'}
        
        try:
            with open(f"{out_name}.bin", "ab") as f:
                f.write(photo_chunk)
        
        except Exception:
            self.logger.error(f"Failed writing to {out_name}.bin")
            return {'returnCode': 0, 'apiName': 'UploadUserPhotoApi'}

        if div_num + 1 == div_len and path.exists(f"{out_name}.bin"):
            try:
                p = ImageFile.Parser()
                with open(f"{out_name}.bin", "rb") as f:
                    p.feed(f.read())
                
                im = p.close()
                im.save(f"{out_name}.jpeg")
            except Exception:
                self.logger.error(f"File {out_name}.bin failed image validation")
            
            try:
                remove(f"{out_name}.bin")
            
            except Exception:
                self.logger.error(f"Failed to delete {out_name}.bin, please remove it manually")

        return {'returnCode': ret_code, 'apiName': 'UploadUserPhotoApi'}
