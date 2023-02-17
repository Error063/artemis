import logging
import json
from datetime import datetime, timedelta
from time import strftime

import pytz
from typing import Dict, Any

from core.config import CoreConfig
from titles.chuni.const import ChuniConstants
from titles.chuni.database import ChuniData
from titles.chuni.config import ChuniConfig

class ChuniBase():
    def __init__(self, core_cfg: CoreConfig, game_cfg: ChuniConfig) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.data = ChuniData(core_cfg)
        self.date_time_format = "%Y-%m-%d %H:%M:%S"
        self.logger = logging.getLogger("chuni")
        self.game = ChuniConstants.GAME_CODE
        self.version = ChuniConstants.VER_CHUNITHM
    
    def handle_game_login_api_request(self, data: Dict) -> Dict:
        #self.data.base.log_event("chuni", "login", logging.INFO, {"version": self.version, "user": data["userId"]})
        return { "returnCode": 1 }
    
    def handle_game_logout_api_request(self, data: Dict) -> Dict:
        #self.data.base.log_event("chuni", "logout", logging.INFO, {"version": self.version, "user": data["userId"]})
        return { "returnCode": 1 }

    def handle_get_game_charge_api_request(self, data: Dict) -> Dict:
        game_charge_list = self.data.static.get_enabled_charges(self.version)

        charges = []
        for x in range(len(game_charge_list)):            
            charges.append({
                "orderId": x,
                "chargeId": game_charge_list[x]["chargeId"],
                "price": 1,
                "startDate": "2017-12-05 07:00:00.0", 
                "endDate": "2099-12-31 00:00:00.0", 
                "salePrice": 1, 
                "saleStartDate": "2017-12-05 07:00:00.0", 
                "saleEndDate": "2099-12-31 00:00:00.0"
            })
        return {
            "length": len(charges), 
            "gameChargeList": charges
        }

    def handle_get_game_event_api_request(self, data: Dict) -> Dict:
        game_events = self.data.static.get_enabled_events(self.version)

        event_list = []
        for evt_row in game_events:
            tmp = {}
            tmp["id"] = evt_row["eventId"]
            tmp["type"] = evt_row["type"]
            tmp["startDate"] = "2017-12-05 07:00:00.0"
            tmp["endDate"] = "2099-12-31 00:00:00.0"
            event_list.append(tmp)

        return {
            "type": data["type"], 
            "length": len(event_list), 
            "gameEventList": event_list
        }

    def handle_get_game_idlist_api_request(self, data: Dict) -> Dict:
        return { "type": data["type"], "length": 0, "gameIdlistList": [] }

    def handle_get_game_message_api_request(self, data: Dict) -> Dict:
        return { "type": data["type"], "length": "0", "gameMessageList": [] }

    def handle_get_game_ranking_api_request(self, data: Dict) -> Dict:
        return { "type": data["type"], "gameRankingList": [] }

    def handle_get_game_sale_api_request(self, data: Dict) -> Dict:
        return { "type": data["type"], "length": 0, "gameSaleList": [] }

    def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        reboot_start = datetime.strftime(datetime.now() - timedelta(hours=4), self.date_time_format)
        reboot_end = datetime.strftime(datetime.now() - timedelta(hours=3), self.date_time_format)
        return {
            "gameSetting": {
                "dataVersion": "1.00.00",
                "isMaintenance": "false",
                "requestInterval": 10,
                "rebootStartTime": reboot_start,
                "rebootEndTime": reboot_end,
                "isBackgroundDistribute": "false",
                "maxCountCharacter": 300,
                "maxCountItem": 300,
                "maxCountMusic": 300,
            },
                "isDumpUpload": "false",
                "isAou": "false",
        }

    def handle_get_user_activity_api_request(self, data: Dict) -> Dict:
        user_activity_list = self.data.profile.get_profile_activity(data["userId"], data["kind"])
        
        activity_list = []
        
        for activity in user_activity_list:
            tmp = activity._asdict()
            tmp.pop("user")
            tmp["id"] = tmp["activityId"]
            tmp.pop("activityId")
            activity_list.append(tmp)

        return {
          "userId": data["userId"], 
          "length": len(activity_list),
          "kind": data["kind"],
          "userActivityList": activity_list
        }

    def handle_get_user_character_api_request(self, data: Dict) -> Dict:
        characters = self.data.item.get_characters(data["userId"])
        if characters is None: return {}
        next_idx = -1

        characterList = []
        for x in range(int(data["nextIndex"]), len(characters)):
            tmp = characters[x]._asdict()
            tmp.pop("user")
            tmp.pop("id")
            characterList.append(tmp)

            if len(characterList) >= int(data["maxCount"]):
                break
        
        if len(characterList) >= int(data["maxCount"]) and len(characters) > int(data["maxCount"]) + int(data["nextIndex"]):
            next_idx = int(data["maxCount"]) + int(data["nextIndex"]) + 1
        
        return {
            "userId": data["userId"], 
            "length": len(characterList),
            "nextIndex": next_idx, 
            "userCharacterList": characterList
        }

    def handle_get_user_charge_api_request(self, data: Dict) -> Dict:
        user_charge_list = self.data.profile.get_profile_charge(data["userId"])

        charge_list = []
        for charge in user_charge_list:
            tmp = charge._asdict()
            tmp.pop("id")
            tmp.pop("user")
            charge_list.append(tmp)

        return {
            "userId": data["userId"], 
            "length": len(charge_list),
            "userChargeList": charge_list
        }

    def handle_get_user_course_api_request(self, data: Dict) -> Dict:
        user_course_list = self.data.score.get_courses(data["userId"])
        if user_course_list is None: 
            return {
                "userId": data["userId"], 
                "length": 0,
                "nextIndex": -1, 
                "userCourseList": []
            }
        
        course_list = []
        next_idx = int(data["nextIndex"])
        max_ct = int(data["maxCount"])

        for x in range(next_idx, len(user_course_list)):
            tmp = user_course_list[x]._asdict()
            tmp.pop("user")
            tmp.pop("id")
            course_list.append(tmp)

            if len(user_course_list) >= max_ct:
                break
        
        if len(user_course_list) >= max_ct:
            next_idx = next_idx + max_ct
        else:
            next_idx = -1
                
        return {
            "userId": data["userId"], 
            "length": len(course_list),
            "nextIndex": next_idx, 
            "userCourseList": course_list
        }

    def handle_get_user_data_api_request(self, data: Dict) -> Dict:
        p = self.data.profile.get_profile_data(data["userId"], self.version)
        if p is None: return {}

        profile = p._asdict()
        profile.pop("id")
        profile.pop("user")
        profile.pop("version")

        return {
            "userId": data["userId"], 
            "userData": profile
        }

    def handle_get_user_data_ex_api_request(self, data: Dict) -> Dict:
        p = self.data.profile.get_profile_data_ex(data["userId"], self.version)
        if p is None: return {}

        profile = p._asdict()
        profile.pop("id")
        profile.pop("user")
        profile.pop("version")

        return {
            "userId": data["userId"], 
            "userDataEx": profile
        }

    def handle_get_user_duel_api_request(self, data: Dict) -> Dict:
        user_duel_list = self.data.item.get_duels(data["userId"])
        if user_duel_list is None: return {}
        
        duel_list = []
        for duel in user_duel_list:
            tmp = duel._asdict()
            tmp.pop("id")
            tmp.pop("user")
            duel_list.append(tmp)

        return {
            "userId": data["userId"], 
            "length": len(duel_list),
            "userDuelList": duel_list
        }

    def handle_get_user_favorite_item_api_request(self, data: Dict) -> Dict:
        return {
            "userId": data["userId"], 
            "length": 0,
            "kind": data["kind"], 
            "nextIndex": -1, 
            "userFavoriteItemList": []
        }

    def handle_get_user_favorite_music_api_request(self, data: Dict) -> Dict:
        """
        This is handled via the webui, which we don't have right now
        """

        return {
            "userId": data["userId"], 
            "length": 0,
            "userFavoriteMusicList": []
        }

    def handle_get_user_item_api_request(self, data: Dict) -> Dict:
        kind = int(int(data["nextIndex"]) / 10000000000)
        next_idx = int(int(data["nextIndex"]) % 10000000000)
        user_item_list = self.data.item.get_items(data["userId"], kind)

        if user_item_list is None or len(user_item_list) == 0: 
            return {"userId": data["userId"], "nextIndex": -1, "itemKind": kind, "userItemList": []}

        items: list[Dict[str, Any]] = []
        for i in range(next_idx, len(user_item_list)):            
            tmp = user_item_list[i]._asdict()
            tmp.pop("user")
            tmp.pop("id")
            items.append(tmp)
            if len(items) >= int(data["maxCount"]):
                break

        xout = kind * 10000000000 + next_idx + len(items)

        if len(items) < int(data["maxCount"]): nextIndex = 0
        else: nextIndex = xout

        return {"userId": data["userId"], "nextIndex": nextIndex, "itemKind": kind, "length": len(items), "userItemList": items}

    def handle_get_user_login_bonus_api_request(self, data: Dict) -> Dict:
        """
        Unsure how to get this to trigger...
        """
        return {
            "userId": data["userId"], 
            "length": 2,
            "userLoginBonusList": [
                {
                "presetId": '10',
                "bonusCount": '0',
                "lastUpdateDate": "1970-01-01 09:00:00",
                "isWatched": "true"
                },
                {
                "presetId": '20',
                "bonusCount": '0',
                "lastUpdateDate": "1970-01-01 09:00:00",
                "isWatched": "true"
                },
            ]
        }

    def handle_get_user_map_api_request(self, data: Dict) -> Dict:
        user_map_list = self.data.item.get_maps(data["userId"])
        if user_map_list is None: return {}
        
        map_list = []
        for map in user_map_list:
            tmp = map._asdict()
            tmp.pop("id")
            tmp.pop("user")
            map_list.append(tmp)

        return {
            "userId": data["userId"], 
            "length": len(map_list),
            "userMapList": map_list
        }

    def handle_get_user_music_api_request(self, data: Dict) -> Dict:
        music_detail = self.data.score.get_scores(data["userId"])
        if music_detail is None: 
            return {
                "userId": data["userId"], 
                "length": 0, 
                "nextIndex": -1,
                "userMusicList": [] #240
            }
        song_list = []
        next_idx = int(data["nextIndex"])
        max_ct = int(data["maxCount"])

        for x in range(next_idx, len(music_detail)):
            found = False
            tmp = music_detail[x]._asdict()
            tmp.pop("user")
            tmp.pop("id")
            
            for song in song_list:
                if song["userMusicDetailList"][0]["musicId"] == tmp["musicId"]:
                    found = True
                    song["userMusicDetailList"].append(tmp)
                    song["length"] = len(song["userMusicDetailList"])
            
            if not found:
                song_list.append({
                    "length": 1,
                    "userMusicDetailList": [tmp]
                })
            
            if len(song_list) >= max_ct:
                break
        
        if len(song_list) >= max_ct:
            next_idx += max_ct
        else:
            next_idx = 0

        return {
            "userId": data["userId"], 
            "length": len(song_list), 
            "nextIndex": next_idx,
            "userMusicList": song_list #240
        }

    def handle_get_user_option_api_request(self, data: Dict) -> Dict:
        p = self.data.profile.get_profile_option(data["userId"])
        
        option = p._asdict()
        option.pop("id")
        option.pop("user")

        return {
            "userId": data["userId"], 
            "userGameOption": option
        }

    def handle_get_user_option_ex_api_request(self, data: Dict) -> Dict:
        p = self.data.profile.get_profile_option_ex(data["userId"])
        
        option = p._asdict()
        option.pop("id")
        option.pop("user")

        return {
            "userId": data["userId"], 
            "userGameOptionEx": option
        }

    def read_wtf8(self, src):
        return bytes([ord(c) for c in src]).decode("utf-8")

    def handle_get_user_preview_api_request(self, data: Dict) -> Dict:
        profile = self.data.profile.get_profile_preview(data["userId"], self.version)
        if profile is None: return None
        profile_character = self.data.item.get_character(data["userId"], profile["characterId"])
        
        if profile_character is None:
            chara = {}
        else:
            chara = profile_character._asdict()
            chara.pop("id")
            chara.pop("user")

        return {
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
            "trophyId": profile["trophyId"],  
            "nameplateId": profile["nameplateId"],
            # Current Selected Character
            "userCharacter": chara,
            # User Game Options
            "playerLevel": profile["playerLevel"], 
            "rating": profile["rating"], 
            "headphone": profile["headphone"],
            "chargeState": "1",
            "userNameEx": profile["userName"],
        }

    def handle_get_user_recent_rating_api_request(self, data: Dict) -> Dict:
        recet_rating_list = self.data.profile.get_profile_recent_rating(data["userId"])
        if recet_rating_list is None: 
            return {
                "userId": data["userId"],
                "length": 0,
                "userRecentRatingList": [],
            }

        return {
            "userId": data["userId"],
            "length": len(recet_rating_list["recentRating"]),
            "userRecentRatingList": recet_rating_list["recentRating"],
        }

    def handle_get_user_region_api_request(self, data: Dict) -> Dict:
        # TODO: Region
        return {
            "userId": data["userId"],
            "length": 0,
            "userRegionList": [],
        }

    def handle_get_user_team_api_request(self, data: Dict) -> Dict:
        # TODO: Team
        return {
            "userId": data["userId"],
            "teamId": 0
        }
    
    def handle_get_team_course_setting_api_request(self, data: Dict) -> Dict:
        return {
            "userId": data["userId"],
            "length": 0,
            "nextIndex": 0,
            "teamCourseSettingList": [],
        }

    def handle_get_team_course_rule_api_request(self, data: Dict) -> Dict:
        return {
            "userId": data["userId"],
            "length": 0,
            "nextIndex": 0,
            "teamCourseRuleList": [],
        }

    def handle_upsert_user_all_api_request(self, data: Dict) -> Dict:
        upsert = data["upsertUserAll"]
        user_id = data["userId"]

        if "userData" in upsert:
            try:
                upsert["userData"][0]["userName"] = self.read_wtf8(upsert["userData"][0]["userName"])
            except: pass

            self.data.profile.put_profile_data(user_id, self.version, upsert["userData"][0])
        if "userDataEx" in upsert:
            self.data.profile.put_profile_data_ex(user_id, self.version, upsert["userDataEx"][0])
        if "userGameOption" in upsert:
            self.data.profile.put_profile_option(user_id, upsert["userGameOption"][0])
        if "userGameOptionEx" in upsert:
            self.data.profile.put_profile_option_ex(user_id, upsert["userGameOptionEx"][0])
        if "userRecentRatingList" in upsert:
            self.data.profile.put_profile_recent_rating(user_id, upsert["userRecentRatingList"])
        
        if "userCharacterList" in upsert:
            for character in upsert["userCharacterList"]:
                self.data.item.put_character(user_id, character)

        if "userMapList" in upsert:
            for map in upsert["userMapList"]:
                self.data.item.put_map(user_id, map)

        if "userCourseList" in upsert:
            for course in upsert["userCourseList"]:
                self.data.score.put_course(user_id, course)

        if "userDuelList" in upsert:
            for duel in upsert["userDuelList"]:
                self.data.item.put_duel(user_id, duel)
        
        if "userItemList" in upsert:
            for item in upsert["userItemList"]:
                self.data.item.put_item(user_id, item)

        if "userActivityList" in upsert:
            for activity in upsert["userActivityList"]:
                self.data.profile.put_profile_activity(user_id, activity)
        
        if "userChargeList" in upsert:
            for charge in upsert["userChargeList"]:
                self.data.profile.put_profile_charge(user_id, charge)
        
        if "userMusicDetailList" in upsert:
            for song in upsert["userMusicDetailList"]:
                self.data.score.put_score(user_id, song)
        
        if "userPlaylogList" in upsert:
            for playlog in upsert["userPlaylogList"]:
                self.data.score.put_playlog(user_id, playlog)
        
        if "userTeamPoint" in upsert:
            # TODO: team stuff
            pass
        
        if "userMapAreaList" in upsert:
            for map_area in upsert["userMapAreaList"]:
                self.data.item.put_map_area(user_id, map_area)

        if "userOverPowerList" in upsert:
            for overpower in upsert["userOverPowerList"]:
                self.data.profile.put_profile_overpower(user_id, overpower)

        if "userEmoneyList" in upsert:
            for emoney in upsert["userEmoneyList"]:
                self.data.profile.put_profile_emoney(user_id, emoney)

        return { "returnCode": "1" }

    def handle_upsert_user_chargelog_api_request(self, data: Dict) -> Dict:
        return { "returnCode": "1" }

    def handle_upsert_client_bookkeeping_api_request(self, data: Dict) -> Dict:
        return { "returnCode": "1" }

    def handle_upsert_client_develop_api_request(self, data: Dict) -> Dict:
        return { "returnCode": "1" }

    def handle_upsert_client_error_api_request(self, data: Dict) -> Dict:
        return { "returnCode": "1" }

    def handle_upsert_client_setting_api_request(self, data: Dict) -> Dict:
        return { "returnCode": "1" }

    def handle_upsert_client_testmode_api_request(self, data: Dict) -> Dict:
        return { "returnCode": "1" }
