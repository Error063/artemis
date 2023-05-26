from datetime import datetime, timedelta
import json, logging
from typing import Any, Dict
import random
import struct

from core.data import Data
from core import CoreConfig
from .config import SaoConfig
from .database import SaoData
from titles.sao.handlers.base import *

class SaoBase:
    def __init__(self, core_cfg: CoreConfig, game_cfg: SaoConfig) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.core_data = Data(core_cfg)
        self.game_data = SaoData(core_cfg)
        self.version = 0
        self.logger = logging.getLogger("sao")

    def handle_noop(self, request: Any) -> bytes:
        sao_request = request

        sao_id = int(sao_request[:4],16) + 1

        ret = struct.pack("!HHIIIIIIb", sao_id, 0, 0, 5, 1, 1, 5, 0x01000000, 0).hex()
        return bytes.fromhex(ret)

    def handle_c122(self, request: Any) -> bytes:
        #common/get_maintenance_info

        resp = SaoGetMaintResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c12e(self, request: Any) -> bytes:
        #common/ac_cabinet_boot_notification
        resp = SaoCommonAcCabinetBootNotificationResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c100(self, request: Any) -> bytes:
        #common/get_app_versions
        resp = SaoCommonGetAppVersionsRequest(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c102(self, request: Any) -> bytes:
        #common/master_data_version_check
        resp = SaoMasterDataVersionCheckResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c10a(self, request: Any) -> bytes:
        #common/paying_play_start
        resp = SaoCommonPayingPlayStartRequest(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_ca02(self, request: Any) -> bytes:
        #quest_multi_play_room/get_quest_scene_multi_play_photon_server
        resp = SaoGetQuestSceneMultiPlayPhotonServerResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c11e(self, request: Any) -> bytes:
        #common/get_auth_card_data

        #Check authentication
        access_code = bytes.fromhex(request[188:268]).decode("utf-16le")
        user_id = self.core_data.card.get_user_id_from_card( access_code )

        if not user_id:
            user_id = self.core_data.user.create_user() #works
            card_id = self.core_data.card.create_card(user_id, access_code)

            if card_id is None:
                user_id = -1
                self.logger.error("Failed to register card!")

            profile_id = self.game_data.profile.create_profile(user_id)

        self.logger.info(f"User Authenticated: { access_code } | { user_id }")

        #Grab values from profile
        profile_data = self.game_data.profile.get_profile(user_id)

        if user_id and not profile_data:
            profile_id = self.game_data.profile.create_profile(user_id)
            profile_data = self.game_data.profile.get_profile(user_id)

        resp = SaoGetAuthCardDataResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, profile_data)
        return resp.make()

    def handle_c40c(self, request: Any) -> bytes:
        #home/check_ac_login_bonus
        resp = SaoHomeCheckAcLoginBonusResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c104(self, request: Any) -> bytes:
        #common/login
        access_code = bytes.fromhex(request[228:308]).decode("utf-16le")
        user_id = self.core_data.card.get_user_id_from_card( access_code )
        profile_data = self.game_data.profile.get_profile(user_id)

        resp = SaoCommonLoginResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, profile_data)
        return resp.make()

    def handle_c404(self, request: Any) -> bytes:
        #home/check_comeback_event
        resp = SaoCheckComebackEventRequest(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c000(self, request: Any) -> bytes:
        #ticket/ticket
        resp = SaoTicketResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c500(self, request: Any) -> bytes:
        #user_info/get_user_basic_data
        user_id = bytes.fromhex(request[88:112]).decode("utf-16le")
        profile_data = self.game_data.profile.get_profile(user_id)

        resp = SaoGetUserBasicDataResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, profile_data)
        return resp.make()
        
    def handle_c600(self, request: Any) -> bytes:
        #have_object/get_hero_log_user_data_list
        heroIdsData = self.game_data.static.get_hero_ids(0, True)
        
        resp = SaoGetHeroLogUserDataListResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, heroIdsData)
        return resp.make()
    
    def handle_c602(self, request: Any) -> bytes:
        #have_object/get_equipment_user_data_list
        equipmentIdsData = self.game_data.static.get_equipment_ids(0, True)
        
        resp = SaoGetEquipmentUserDataListResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, equipmentIdsData)
        return resp.make()
        
    def handle_c604(self, request: Any) -> bytes:
        #have_object/get_item_user_data_list
        itemIdsData = self.game_data.static.get_item_ids(0, True)
        
        resp = SaoGetItemUserDataListResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, itemIdsData)
        return resp.make()
        
    def handle_c606(self, request: Any) -> bytes:
        #have_object/get_support_log_user_data_list
        supportIdsData = self.game_data.static.get_support_log_ids(0, True)
        
        resp = SaoGetSupportLogUserDataListResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, supportIdsData)
        return resp.make()
    
    def handle_c800(self, request: Any) -> bytes:
        #custom/get_title_user_data_list
        titleIdsData = self.game_data.static.get_title_ids(0, True)
        
        resp = SaoGetTitleUserDataListResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, titleIdsData)
        return resp.make()
        
    def handle_c608(self, request: Any) -> bytes:
        #have_object/get_episode_append_data_list
        user_id = bytes.fromhex(request[88:112]).decode("utf-16le")
        profile_data = self.game_data.profile.get_profile(user_id)

        resp = SaoGetEpisodeAppendDataListResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, profile_data)
        return resp.make()

    def handle_c804(self, request: Any) -> bytes:
        #custom/get_party_data_list
        resp = SaoGetPartyDataListResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c902(self, request: Any) -> bytes: # for whatever reason, having all entries empty or filled changes nothing
        #quest/get_quest_scene_prev_scan_profile_card
        resp = SaoGetQuestScenePrevScanProfileCardResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c124(self, request: Any) -> bytes:
        #common/get_resource_path_info
        resp = SaoGetResourcePathInfoResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c900(self, request: Any) -> bytes:
        #quest/get_quest_scene_user_data_list // QuestScene.csv
        questIdsData = self.game_data.static.get_quests_ids(0, True)
        resp = SaoGetQuestSceneUserDataListResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, questIdsData)
        return resp.make()

    def handle_c400(self, request: Any) -> bytes:
        #home/check_yui_medal_get_condition
        resp = SaoCheckYuiMedalGetConditionResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c402(self, request: Any) -> bytes:
        #home/get_yui_medal_bonus_user_data
        resp = SaoGetYuiMedalBonusUserDataResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c40a(self, request: Any) -> bytes:
        #home/check_profile_card_used_reward
        resp = SaoCheckProfileCardUsedRewardResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c904(self, request: Any) -> bytes:
        #quest/episode_play_start
        user_id = bytes.fromhex(request[100:124]).decode("utf-16le")
        profile_data = self.game_data.profile.get_profile(user_id)

        resp = SaoEpisodePlayStartResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, profile_data)
        return resp.make()

    def handle_c908(self, request: Any) -> bytes: # function not working yet, tired of this
        #quest/episode_play_end
        resp = SaoEpisodePlayEndResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c914(self, request: Any) -> bytes:
        #quest/trial_tower_play_start
        user_id = bytes.fromhex(request[100:124]).decode("utf-16le")
        floor_id = int(request[130:132], 16) # not required but nice to know
        profile_data = self.game_data.profile.get_profile(user_id)

        resp = SaoEpisodePlayStartResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, profile_data)
        return resp.make()

    def handle_c90a(self, request: Any) -> bytes: #should be tweaked for proper item unlock
        #quest/episode_play_end_unanalyzed_log_fixed
        resp = SaoEpisodePlayEndUnanalyzedLogFixedResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()
