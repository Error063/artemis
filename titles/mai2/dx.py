from typing import Any, List, Dict
from datetime import datetime, timedelta
import pytz
import json
from random import randint

from core.config import CoreConfig
from core.utils import Utils
from titles.mai2.base import Mai2Base
from titles.mai2.config import Mai2Config
from titles.mai2.const import Mai2Constants


class Mai2DX(Mai2Base):
    def __init__(self, cfg: CoreConfig, game_cfg: Mai2Config) -> None:
        super().__init__(cfg, game_cfg)
        self.version = Mai2Constants.VER_MAIMAI_DX

        # DX earlier version need a efficient old server uri to work
        # game will auto add MaimaiServlet endpoint behind return uri
        # so do not add "MaimaiServlet"
        if not self.core_config.server.is_using_proxy and Utils.get_title_port(self.core_config) != 80:
            self.old_server = f"http://{self.core_config.server.hostname}:{Utils.get_title_port(cfg)}/SDEY/197/"

        else:
            self.old_server = f"http://{self.core_config.server.hostname}/SDEY/197/"

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
            "gameSetting": {
                "isMaintenance": False,
                "requestInterval": 1800,
                "rebootStartTime": reboot_start,
                "rebootEndTime": reboot_end,
                "rebootInterval": 0,
                "movieUploadLimit": 100,
                "movieStatus": 1 if self.game_config.uploads.movies else 0,
                "movieServerUri": "",
                "deliverServerUri": "",
                "oldServerUri": self.old_server,
                "usbDlServerUri": "",
                "maxCountRivalMusic": 100,
                "replicationDelayLimit": 10,
                "exclusionStartTime": "00:00:00",
                "exclusionEndTime": "00:00:00",
                "pingDisable": True,
                "packetTimeout": 20000,
                "packetTimeoutLong": 60000,
                "packetRetryCount": 10,
                "userDataDlErrTimeout": 300000,
                "userDataDlErrRetryCount": 1000,
                "userDataDlErrSamePacketRetryCount": 1000,
                "userDataUpSkipTimeout": 0,
                "userDataUpSkipRetryCount": 0,
                "iconPhotoDisable": not self.game_config.uploads.photos,
                "uploadPhotoDisable": not self.game_config.uploads.photos,
                "maxCountMusic": 0,
                "maxCountItem": 0},
            "isAouAccession": False,
        }

    async def handle_get_user_preview_api_request(self, data: Dict) -> Dict:
        p = await self.data.profile.get_profile_detail(data["userId"], self.version)
        o = await self.data.profile.get_profile_option(data["userId"], self.version)
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

    async def handle_upload_user_playlog_api_request(self, data: Dict) -> Dict:
        user_id = data["userId"]
        playlog = data["userPlaylog"]

        await self.data.score.put_playlog(user_id, playlog)

        return {"returnCode": 1, "apiName": "UploadUserPlaylogApi"}

    async def handle_upsert_user_chargelog_api_request(self, data: Dict) -> Dict:
        user_id = data["userId"]
        charge = data["userCharge"]

        # remove the ".0" from the date string, festival only?
        charge["purchaseDate"] = charge["purchaseDate"].replace(".0", "")
        await self.data.item.put_charge(
            user_id,
            charge["chargeId"],
            charge["stock"],
            datetime.strptime(charge["purchaseDate"], Mai2Constants.DATE_TIME_FORMAT),
            datetime.strptime(charge["validDate"], Mai2Constants.DATE_TIME_FORMAT),
        )

        return {"returnCode": 1, "apiName": "UpsertUserChargelogApi"}

    async def handle_upsert_user_all_api_request(self, data: Dict) -> Dict:
        user_id = data["userId"]
        upsert = data["upsertUserAll"]
        
        if int(user_id) & 0x1000000000001 == 0x1000000000001:
            place_id = int(user_id) & 0xFFFC00000000
            
            self.logger.info("Guest play from place ID %d, ignoring.", place_id)
            return {"returnCode": 1, "apiName": "UpsertUserAllApi"}

        if "userData" in upsert and len(upsert["userData"]) > 0:
            upsert["userData"][0]["isNetMember"] = 1
            upsert["userData"][0].pop("accessCode")
            await self.data.profile.put_profile_detail(
                user_id, self.version, upsert["userData"][0]
            )

        if "userExtend" in upsert and len(upsert["userExtend"]) > 0:
            await self.data.profile.put_profile_extend(
                user_id, self.version, upsert["userExtend"][0]
            )

        if "userGhost" in upsert:
            for ghost in upsert["userGhost"]:
                await self.data.profile.put_profile_ghost(user_id, self.version, ghost)

        if "userOption" in upsert and len(upsert["userOption"]) > 0:
            await self.data.profile.put_profile_option(
                user_id, self.version, upsert["userOption"][0]
            )

        if "userRatingList" in upsert and len(upsert["userRatingList"]) > 0:
            await self.data.profile.put_profile_rating(
                user_id, self.version, upsert["userRatingList"][0]
            )

        if "userActivityList" in upsert and len(upsert["userActivityList"]) > 0:
            for k, v in upsert["userActivityList"][0].items():
                for act in v:
                    await self.data.profile.put_profile_activity(user_id, act)

        if "userChargeList" in upsert and len(upsert["userChargeList"]) > 0:
            for charge in upsert["userChargeList"]:
                # remove the ".0" from the date string, festival only?
                charge["purchaseDate"] = charge["purchaseDate"].replace(".0", "")
                await self.data.item.put_charge(
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
                await self.data.item.put_character(
                    user_id,
                    char["characterId"],
                    char["level"],
                    char["awakening"],
                    char["useCount"],
                )

        if "userItemList" in upsert and len(upsert["userItemList"]) > 0:
            for item in upsert["userItemList"]:
                await self.data.item.put_item(
                    user_id,
                    int(item["itemKind"]),
                    item["itemId"],
                    item["stock"],
                    item["isValid"],
                )

        if "userLoginBonusList" in upsert and len(upsert["userLoginBonusList"]) > 0:
            for login_bonus in upsert["userLoginBonusList"]:
                await self.data.item.put_login_bonus(
                    user_id,
                    login_bonus["bonusId"],
                    login_bonus["point"],
                    login_bonus["isCurrent"],
                    login_bonus["isComplete"],
                )

        if "userMapList" in upsert and len(upsert["userMapList"]) > 0:
            for map in upsert["userMapList"]:
                await self.data.item.put_map(
                    user_id,
                    map["mapId"],
                    map["distance"],
                    map["isLock"],
                    map["isClear"],
                    map["isComplete"],
                )

        if "userMusicDetailList" in upsert and len(upsert["userMusicDetailList"]) > 0:
            for music in upsert["userMusicDetailList"]:
                await self.data.score.put_best_score(user_id, music)

        if "userCourseList" in upsert and len(upsert["userCourseList"]) > 0:
            for course in upsert["userCourseList"]:
                await self.data.score.put_course(user_id, course)

        if "userFavoriteList" in upsert and len(upsert["userFavoriteList"]) > 0:
            for fav in upsert["userFavoriteList"]:
                await self.data.item.put_favorite(user_id, fav["kind"], fav["itemIdList"])

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
                await self.data.item.put_friend_season_ranking(user_id, fsr)
        
        if "user2pPlaylog" in upsert:
            await self.data.score.put_playlog_2p(user_id, upsert["user2pPlaylog"])

        return {"returnCode": 1, "apiName": "UpsertUserAllApi"}

    async def handle_get_user_data_api_request(self, data: Dict) -> Dict:
        profile = await self.data.profile.get_profile_detail(data["userId"], self.version)
        if profile is None:
            return

        profile_dict = profile._asdict()
        profile_dict.pop("id")
        profile_dict.pop("user")
        profile_dict.pop("version")

        return {"userId": data["userId"], "userData": profile_dict}

    async def handle_get_user_extend_api_request(self, data: Dict) -> Dict:
        extend = await self.data.profile.get_profile_extend(data["userId"], self.version)
        if extend is None:
            return

        extend_dict = extend._asdict()
        extend_dict.pop("id")
        extend_dict.pop("user")
        extend_dict.pop("version")

        return {"userId": data["userId"], "userExtend": extend_dict}

    async def handle_get_user_option_api_request(self, data: Dict) -> Dict:
        options = await self.data.profile.get_profile_option(data["userId"], self.version)
        if options is None:
            return

        options_dict = options._asdict()
        options_dict.pop("id")
        options_dict.pop("user")
        options_dict.pop("version")

        return {"userId": data["userId"], "userOption": options_dict}

    async def handle_get_user_card_api_request(self, data: Dict) -> Dict:
        user_cards = await self.data.item.get_cards(data["userId"])
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

    async def handle_get_user_item_api_request(self, data: Dict) -> Dict:
        kind = int(data["nextIndex"] / 10000000000)
        next_idx = int(data["nextIndex"] % 10000000000)
        user_item_list = await self.data.item.get_items(data["userId"], kind)

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
        characters = await self.data.item.get_characters(data["userId"])

        chara_list = []
        for chara in characters:
            tmp = chara._asdict()
            tmp.pop("id")
            tmp.pop("user")
            chara_list.append(tmp)

        return {"userId": data["userId"], "userCharacterList": chara_list}

    async def handle_get_user_favorite_api_request(self, data: Dict) -> Dict:
        favorites = await self.data.item.get_favorites(data["userId"], data["itemKind"])
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
        ghost = await self.data.profile.get_profile_ghost(data["userId"], self.version)
        if ghost is None:
            return

        ghost_dict = ghost._asdict()
        ghost_dict.pop("user")
        ghost_dict.pop("id")
        ghost_dict.pop("version_int")

        return {"userId": data["userId"], "userGhost": ghost_dict}

    async def handle_get_user_rating_api_request(self, data: Dict) -> Dict:
        rating = await self.data.profile.get_profile_rating(data["userId"], self.version)
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
        playlist = await self.data.profile.get_profile_activity(data["userId"], 1)
        musiclist = await self.data.profile.get_profile_activity(data["userId"], 2)
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
        user_courses = await self.data.score.get_courses(data["userId"])
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
        friend_season_ranking = await self.data.item.get_friend_season_ranking(data["userId"])
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
        maps = await self.data.item.get_maps(data["userId"])
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
        login_bonuses = await self.data.item.get_login_bonuses(data["userId"])
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
        """
        class UserRegionList:
            regionId: int
            playCount: int
            created: str
        """
        return {"userId": data["userId"], "length": 0, "userRegionList": []}

    async def handle_get_user_rival_data_api_request(self, data: Dict) -> Dict:
        user_id = data["userId"]
        rival_id = data["rivalId"]

        """
        class UserRivalData:
            rivalId: int
            rivalName: str
        """
        return {"userId": user_id, "userRivalData": {}}

    async def handle_get_user_rival_music_api_request(self, data: Dict) -> Dict:
        user_id = data["userId"]
        rival_id = data["rivalId"]
        next_idx = data["nextIndex"]
        rival_music_levels = data["userRivalMusicLevelList"]

        """
        class UserRivalMusicList:
            class UserRivalMusicDetailList:
                level: int
                achievement: int
                deluxscoreMax: int

            musicId: int
            userRivalMusicDetailList: list[UserRivalMusicDetailList]
        """
        return {"userId": user_id, "nextIndex": 0, "userRivalMusicList": []}

    async def handle_get_user_music_api_request(self, data: Dict) -> Dict:
        user_id = data.get("userId", 0)        
        next_index = data.get("nextIndex", 0)
        max_ct = data.get("maxCount", 50)
        upper_lim = next_index + max_ct
        music_detail_list = []

        if user_id <= 0:
            self.logger.warning("handle_get_user_music_api_request: Could not find userid in data, or userId is 0")
            return {}
        
        songs = await self.data.score.get_best_scores(user_id)
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

    async def handle_user_login_api_request(self, data: Dict) -> Dict:
        ret = await super().handle_user_login_api_request(data)
        if ret is None or not ret:
            return ret
        ret['loginId'] = ret.get('loginCount', 0)
        return ret
