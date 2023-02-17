import logging
from datetime import datetime, timedelta

from typing import Dict

from core.config import CoreConfig
from titles.chuni.const import ChuniConstants
from titles.chuni.database import ChuniData
from titles.chuni.base import ChuniBase
from titles.chuni.config import ChuniConfig

class ChuniNew(ChuniBase):

    ITEM_TYPE = {
        "character": 20,
        "story": 21,
        "card": 22
    }

    def __init__(self, core_cfg: CoreConfig, game_cfg: ChuniConfig) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.data = ChuniData(core_cfg)
        self.date_time_format = "%Y-%m-%d %H:%M:%S"
        self.logger = logging.getLogger("chuni")
        self.game = ChuniConstants.GAME_CODE
        self.version = ChuniConstants.VER_CHUNITHM_NEW
    
    def handle_get_game_setting_api_request(self, data: Dict) -> Dict:
        match_start = datetime.strftime(datetime.now() - timedelta(hours=10), self.date_time_format)
        match_end = datetime.strftime(datetime.now() + timedelta(hours=10), self.date_time_format)
        reboot_start = datetime.strftime(datetime.now() - timedelta(hours=11), self.date_time_format)
        reboot_end = datetime.strftime(datetime.now() - timedelta(hours=10), self.date_time_format)
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
                "romVersion": "2.00.00",
                "dataVersion": "2.00.00",
                "matchingUri": f"http://{self.core_cfg.server.hostname}:{self.core_cfg.title.port}/SDHD/200/ChuniServlet/",
                "matchingUriX": f"http://{self.core_cfg.server.hostname}:{self.core_cfg.title.port}/SDHD/200/ChuniServlet/",
                "udpHolePunchUri": f"http://{self.core_cfg.server.hostname}:{self.core_cfg.title.port}/SDHD/200/ChuniServlet/",
                "reflectorUri": f"http://{self.core_cfg.server.hostname}:{self.core_cfg.title.port}/SDHD/200/ChuniServlet/",
            },
                "isDumpUpload": "false",
                "isAou": "false",
        }
        
    def handle_delete_token_api_request(self, data: Dict) -> Dict:
        return { "returnCode": "1" }
    
    def handle_create_token_api_request(self, data: Dict) -> Dict:
        return { "returnCode": "1" }
        
    def handle_get_user_map_area_api_request(self, data: Dict) -> Dict:
        user_map_areas = self.data.item.get_map_areas(data["userId"])

        map_areas = []
        for map_area in user_map_areas:
            tmp = map_area._asdict()
            tmp.pop("id")
            tmp.pop("user")
            map_areas.append(tmp)

        return {
            "userId": data["userId"], 
            "userMapAreaList": map_areas
        }
    
    def handle_get_user_symbol_chat_setting_api_request(self, data: Dict) -> Dict:
        return {
            "userId": data["userId"], 
            "symbolCharInfoList": []
        }

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
            "chargeState": 0,
            "userNameEx": "0",
            "banState": 0,
            "classEmblemMedal": profile["classEmblemMedal"],
            "classEmblemBase": profile["classEmblemBase"],
            "battleRankId": profile["battleRankId"],
        }
        return data1
