from datetime import datetime, date, timedelta
from typing import Dict
import logging

from core.config import CoreConfig
from titles.mai2.const import Mai2Constants
from titles.mai2.config import Mai2Config
from titles.mai2.database import Mai2Data

class Mai2Base():
    def __init__(self, cfg: CoreConfig, game_cfg: Mai2Config) -> None:
        self.core_config = cfg
        self.game_config = game_cfg
        self.game = Mai2Constants.GAME_CODE
        self.version = Mai2Constants.VER_MAIMAI_DX
        self.data = Mai2Data(cfg)
        self.logger = logging.getLogger("mai2")

    def handle_get_game_setting_api_request(self, data: Dict):
        reboot_start = date.strftime(datetime.now() + timedelta(hours=3), Mai2Constants.DATE_TIME_FORMAT)
        reboot_end = date.strftime(datetime.now() + timedelta(hours=4), Mai2Constants.DATE_TIME_FORMAT)
        return {
        "gameSetting": {
            "isMaintenance": "false",
            "requestInterval": 10,
            "rebootStartTime": reboot_start,
            "rebootEndTime": reboot_end,
            "movieUploadLimit": 10000,
            "movieStatus": 0,
            "movieServerUri": "",
            "deliverServerUri": "",
            "oldServerUri": "",
            "usbDlServerUri": "",
            "rebootInterval": 0        
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
        events_lst = []
        if events is None: return {"type": data["type"], "length": 0, "gameEventList": []}

        for event in events:
            events_lst.append({
                "type": event["type"], 
                "id": event["eventId"], 
                "startDate": "2017-12-05 07:00:00.0", 
                "endDate": "2099-12-31 00:00:00.0"
                })

        return {"type": data["type"], "length": len(events_lst), "gameEventList": events_lst}

    def handle_get_game_ng_music_id_api_request(self, data: Dict) -> Dict:
        return {"length": 0, "musicIdList": []}

    def handle_get_game_charge_api_request(self, data: Dict) -> Dict:
        game_charge_list = self.data.static.get_enabled_tickets(self.version, 1)
        if game_charge_list is None: return {"length": 0, "gameChargeList": []}

        charge_list = []
        for x in range(len(game_charge_list)):
            charge_list.append({
                "orderId": x,
                "chargeId": game_charge_list[x]["ticketId"],
                "price": game_charge_list[x]["price"],
                "startDate": "2017-12-05 07:00:00.0", 
                "endDate": "2099-12-31 00:00:00.0"
            })

        return {"length": len(charge_list), "gameChargeList": charge_list}

    def handle_upsert_client_setting_api_request(self, data: Dict) -> Dict:
        pass

    def handle_upsert_client_upload_api_request(self, data: Dict) -> Dict:
        pass

    def handle_upsert_client_bookkeeping_api_request(self, data: Dict) -> Dict:
        pass

    def handle_upsert_client_testmode_api_request(self, data: Dict) -> Dict:
        pass

    def handle_get_user_preview_api_request(self, data: Dict) -> Dict:
        p = self.data.profile.get_profile_detail(data["userId"], self.version)
        o = self.data.profile.get_profile_option(data["userId"], self.version)
        if p is None or o is None: return {} # Register
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
            "nameplateId": 0, # Unused
            "iconId": profile["iconId"],
            "trophyId": 0, # Unused
            "partnerId": profile["partnerId"],
            "frameId": profile["frameId"],
            "dispRate": option["dispRate"], # 0: all/begin, 1: disprate, 2: dispDan, 3: hide, 4: end
            "totalAwake": profile["totalAwake"],
            "isNetMember": profile["isNetMember"],
            "dailyBonusDate": profile["dailyBonusDate"],
            "headPhoneVolume": option["headPhoneVolume"],
            "isInherit": False, # Not sure what this is or does??
            "banState": profile["banState"] if profile["banState"] is not None else 0 # New with uni+
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
            "consecutiveLoginCount": 0, # We don't really have a way to track this...
            "loginId": loginCt # Used with the playlog!
        }
    
    def handle_upload_user_playlog_api_request(self, data: Dict) -> Dict:
        user_id = data["userId"]
        playlog = data["userPlaylog"]

        self.data.score.put_playlog(user_id, playlog)

    def handle_upsert_user_all_api_request(self, data: Dict) -> Dict:
        user_id = data["userId"]
        upsert = data["upsertUserAll"]

        if "userData" in upsert and len(upsert["userData"]) > 0:
            upsert["userData"][0]["isNetMember"] = 1
            upsert["userData"][0].pop("accessCode")
            self.data.profile.put_profile_detail(user_id, self.version, upsert["userData"][0])
        
        if "userExtend" in upsert and len(upsert["userExtend"]) > 0:
            self.data.profile.put_profile_extend(user_id, self.version, upsert["userExtend"][0])

        if "userGhost" in upsert:
            for ghost in upsert["userGhost"]:
                self.data.profile.put_profile_extend(user_id, self.version, ghost)
        
        if "userOption" in upsert and len(upsert["userOption"]) > 0:
            self.data.profile.put_profile_option(user_id, self.version, upsert["userOption"][0])

        if "userRatingList" in upsert and len(upsert["userRatingList"]) > 0:
            self.data.profile.put_profile_rating(user_id, self.version, upsert["userRatingList"][0])

        if "userActivityList" in upsert and len(upsert["userActivityList"]) > 0:
            for k,v in upsert["userActivityList"][0].items():
                for act in v:
                    self.data.profile.put_profile_activity(user_id, act)

        if upsert["isNewCharacterList"] and int(upsert["isNewCharacterList"]) > 0:
            for char in upsert["userCharacterList"]:
                self.data.item.put_character(user_id, char["characterId"], char["level"], char["awakening"], char["useCount"])

        if upsert["isNewItemList"] and int(upsert["isNewItemList"]) > 0:
            for item in upsert["userItemList"]:
                self.data.item.put_item(user_id, int(item["itemKind"]), item["itemId"], item["stock"], item["isValid"])

        if upsert["isNewLoginBonusList"] and int(upsert["isNewLoginBonusList"]) > 0:
            for login_bonus in upsert["userLoginBonusList"]:
                self.data.item.put_login_bonus(user_id, login_bonus["bonusId"], login_bonus["point"], login_bonus["isCurrent"], login_bonus["isComplete"])

        if upsert["isNewMapList"] and int(upsert["isNewMapList"]) > 0:
            for map in upsert["userMapList"]:
                self.data.item.put_map(user_id, map["mapId"], map["distance"], map["isLock"], map["isClear"], map["isComplete"])
        
        if upsert["isNewMusicDetailList"] and int(upsert["isNewMusicDetailList"]) > 0:
            for music in upsert["userMusicDetailList"]:
                self.data.score.put_best_score(user_id, music)
        
        if upsert["isNewCourseList"] and int(upsert["isNewCourseList"]) > 0:
            for course in upsert["userCourseList"]:
                self.data.score.put_course(user_id, course)
    
        if upsert["isNewFavoriteList"] and int(upsert["isNewFavoriteList"]) > 0:
            for fav in upsert["userFavoriteList"]:
                self.data.item.put_favorite(user_id, fav["kind"], fav["itemIdList"])

        if "isNewFriendSeasonRankingList" in upsert and int(upsert["isNewFriendSeasonRankingList"]) > 0:
            for fsr in upsert["userFriendSeasonRankingList"]:
                pass

    def handle_user_logout_api_request(self, data: Dict) -> Dict:
        pass

    def handle_get_user_data_api_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile_detail(data["userId"], self.version)
        if profile is None: return

        profile_dict = profile._asdict()
        profile_dict.pop("id")
        profile_dict.pop("user")
        profile_dict.pop("version")

        return {
            "userId": data["userId"],
            "userData": profile_dict
        }

    def handle_get_user_extend_api_request(self, data: Dict) -> Dict:
        extend = self.data.profile.get_profile_extend(data["userId"], self.version)
        if extend is None: return

        extend_dict = extend._asdict()
        extend_dict.pop("id")
        extend_dict.pop("user")
        extend_dict.pop("version")

        return {
            "userId": data["userId"],
            "userExtend": extend_dict
        }

    def handle_get_user_option_api_request(self, data: Dict) -> Dict:
        options = self.data.profile.get_profile_option(data["userId"], self.version)
        if options is None: return

        options_dict = options._asdict()
        options_dict.pop("id")
        options_dict.pop("user")
        options_dict.pop("version")

        return {
            "userId": data["userId"],
            "userOption": options_dict
        }

    def handle_get_user_card_api_request(self, data: Dict) -> Dict:
        return {"userId": data["userId"], "nextIndex": 0, "userCardList": []}

    def handle_get_user_charge_api_request(self, data: Dict) -> Dict:
        return {"userId": data["userId"], "length": 0, "userChargeList": []}

    def handle_get_user_item_api_request(self, data: Dict) -> Dict:
        kind = int(data["nextIndex"] / 10000000000)
        next_idx = int(data["nextIndex"] % 10000000000)
        user_items = self.data.item.get_items(data["userId"], kind)
        user_item_list = []
        next_idx = 0

        for x in range(next_idx, data["maxCount"]):
            try:
                user_item_list.append({"item_kind": user_items[x]["item_kind"], "item_id": user_items[x]["item_id"], 
                "stock": user_items[x]["stock"], "isValid": user_items[x]["is_valid"]})
            except: break
            
            if len(user_item_list) == data["maxCount"]:
                next_idx = data["nextIndex"] + data["maxCount"] + 1
                break

        return {"userId": data["userId"], "nextIndex": next_idx, "itemKind": kind, "userItemList": user_item_list}

    def handle_get_user_character_api_request(self, data: Dict) -> Dict:
        characters = self.data.item.get_characters(data["userId"])
        chara_list = []
        for chara in characters:
            chara_list.append({
                "characterId": chara["character_id"],
                "level": chara["level"],
                "awakening": chara["awakening"],
                "useCount": chara["use_count"],
            })

        return {"userId": data["userId"], "userCharacterList": chara_list}
    
    def handle_get_user_favorite_api_request(self, data: Dict) -> Dict:
        favorites = self.data.item.get_favorites(data["userId"], data["itemKind"])
        if favorites is None: return

        userFavs = []
        for fav in favorites:
            userFavs.append({
                "userId": data["userId"],
                "itemKind": fav["itemKind"],
                "itemIdList": fav["itemIdList"]
            })

        return {
            "userId": data["userId"],
            "userFavoriteData": userFavs
        }

    def handle_get_user_ghost_api_request(self, data: Dict) -> Dict:
        ghost = self.data.profile.get_profile_ghost(data["userId"], self.version)
        if ghost is None: return

        ghost_dict = ghost._asdict()
        ghost_dict.pop("user")
        ghost_dict.pop("id")
        ghost_dict.pop("version_int")

        return {
            "userId": data["userId"],
            "userGhost": ghost_dict
        }

    def handle_get_user_rating_api_request(self, data: Dict) -> Dict:
        rating = self.data.profile.get_profile_rating(data["userId"], self.version)
        if rating is None: return

        rating_dict = rating._asdict()
        rating_dict.pop("user")
        rating_dict.pop("id")
        rating_dict.pop("version")

        return {
            "userId": data["userId"],
            "userRating": rating_dict
        }

    def handle_get_user_activity_api_request(self, data: Dict) -> Dict:
        """
        kind 1 is playlist, kind 2 is music list
        """
        playlist = self.data.profile.get_profile_activity(data["userId"], 1)
        musiclist = self.data.profile.get_profile_activity(data["userId"], 2)
        if playlist is None or musiclist is None: return

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

        return { 
            "userActivity": {
                "playList": plst,
                "musicList": mlst
            } 
        }

    def handle_get_user_course_api_request(self, data: Dict) -> Dict:
        user_courses = self.data.score.get_courses(data["userId"])

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
        friend_season_ranking_list = []
        next_index = 0

        for x in range(data["nextIndex"], data["maxCount"] + data["nextIndex"]):
            try:
                friend_season_ranking_list.append({
                    "mapId": friend_season_ranking_list[x]["map_id"],
                    "distance": friend_season_ranking_list[x]["distance"],
                    "isLock": friend_season_ranking_list[x]["is_lock"],
                    "isClear": friend_season_ranking_list[x]["is_clear"],
                    "isComplete": friend_season_ranking_list[x]["is_complete"],
                })
            except:
                break

        # We're capped and still have some left to go
        if len(friend_season_ranking_list) == data["maxCount"] and len(friend_season_ranking) > data["maxCount"] + data["nextIndex"]:
            next_index = data["maxCount"] + data["nextIndex"]

        return {"userId": data["userId"], "nextIndex": next_index, "userFriendSeasonRankingList": friend_season_ranking_list}

    def handle_get_user_map_api_request(self, data: Dict) -> Dict:
        maps = self.data.item.get_maps(data["userId"])
        map_list = []
        next_index = 0

        for x in range(data["nextIndex"], data["maxCount"] + data["nextIndex"]):
            try:
                map_list.append({
                    "mapId": maps[x]["map_id"],
                    "distance": maps[x]["distance"],
                    "isLock": maps[x]["is_lock"],
                    "isClear": maps[x]["is_clear"],
                    "isComplete": maps[x]["is_complete"],
                })
            except:
                break

        # We're capped and still have some left to go
        if len(map_list) == data["maxCount"] and len(maps) > data["maxCount"] + data["nextIndex"]:
            next_index = data["maxCount"] + data["nextIndex"]

        return {"userId": data["userId"], "nextIndex": next_index, "userMapList": map_list}

    def handle_get_user_login_bonus_api_request(self, data: Dict) -> Dict:
        login_bonuses = self.data.item.get_login_bonuses(data["userId"])
        login_bonus_list = []
        next_index = 0

        for x in range(data["nextIndex"], data["maxCount"] + data["nextIndex"]):
            try:
                login_bonus_list.append({
                    "bonusId": login_bonuses[x]["bonus_id"],
                    "point": login_bonuses[x]["point"],
                    "isCurrent": login_bonuses[x]["is_current"],
                    "isComplete": login_bonuses[x]["is_complete"],
                })
            except:
                break

        # We're capped and still have some left to go
        if len(login_bonus_list) == data["maxCount"] and len(login_bonuses) > data["maxCount"] + data["nextIndex"]:
            next_index = data["maxCount"] + data["nextIndex"]

        return {"userId": data["userId"], "nextIndex": next_index, "userLoginBonusList": login_bonus_list}

    def handle_get_user_region_api_request(self, data: Dict) -> Dict:
        return {"userId": data["userId"], "length": 0, "userRegionList": []}

    def handle_get_user_music_api_request(self, data: Dict) -> Dict:
        songs = self.data.score.get_best_scores(data["userId"])
        music_detail_list = []
        next_index = 0

        if songs is not None:
            for song in songs:
                music_detail_list.append({
                    "musicId": song["song_id"],
                    "level": song["chart_id"],
                    "playCount": song["play_count"],
                    "achievement": song["achievement"],
                    "comboStatus": song["combo_status"],
                    "syncStatus": song["sync_status"],
                    "deluxscoreMax": song["dx_score"],
                    "scoreRank": song["score_rank"],
                    })
                if len(music_detail_list) == data["maxCount"]:
                    next_index = data["maxCount"] + data["nextIndex"]
                    break

        return {"userId": data["userId"], "nextIndex": next_index, "userMusicList": [{"userMusicDetailList": music_detail_list}]}
