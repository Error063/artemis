from datetime import datetime, timedelta
import json, logging
from typing import Any, Dict
import random
import struct
from csv import *
from random import choice
import random as rand

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
        req = bytes.fromhex(request)[24:]

        req_struct = Struct(
            Padding(16),
            "cabinet_type" / Int8ub,  # cabinet_type is a byte
            "auth_type" / Int8ub,  # auth_type is a byte
            "store_id_size" / Rebuild(Int32ub, len_(this.store_id) * 2),  # calculates the length of the store_id
            "store_id" / PaddedString(this.store_id_size, "utf_16_le"),  # store_id is a (zero) padded string
            "serial_no_size" / Rebuild(Int32ub, len_(this.serial_no) * 2),  # calculates the length of the serial_no
            "serial_no" / PaddedString(this.serial_no_size, "utf_16_le"),  # serial_no is a (zero) padded string
            "access_code_size" / Rebuild(Int32ub, len_(this.access_code) * 2),  # calculates the length of the access_code
            "access_code" / PaddedString(this.access_code_size, "utf_16_le"),  # access_code is a (zero) padded string
            "chip_id_size" / Rebuild(Int32ub, len_(this.chip_id) * 2),  # calculates the length of the chip_id
            "chip_id" / PaddedString(this.chip_id_size, "utf_16_le"),  # chip_id is a (zero) padded string
        )

        req_data = req_struct.parse(req)
        access_code = req_data.access_code

        #Check authentication
        user_id = self.core_data.card.get_user_id_from_card( access_code )

        if not user_id:
            user_id = self.core_data.user.create_user() #works
            card_id = self.core_data.card.create_card(user_id, access_code)

            if card_id is None:
                user_id = -1
                self.logger.error("Failed to register card!")

            # Create profile with 3 basic heroes
            profile_id = self.game_data.profile.create_profile(user_id)
            self.game_data.item.put_hero_log(user_id, 101000010, 1, 0, 101000016, 0, 30086, 1001, 1002, 1003, 1005)
            self.game_data.item.put_hero_log(user_id, 102000010, 1, 0, 103000006, 0, 30086, 1001, 1002, 1003, 1005)
            self.game_data.item.put_hero_log(user_id, 103000010, 1, 0, 112000009, 0, 30086, 1001, 1002, 1003, 1005)
            self.game_data.item.put_hero_party(user_id, 0, 101000010, 102000010, 103000010)
            self.game_data.item.put_equipment_data(user_id, 101000016, 1, 200, 0, 0, 0)
            self.game_data.item.put_equipment_data(user_id, 103000006, 1, 200, 0, 0, 0)
            self.game_data.item.put_equipment_data(user_id, 112000009, 1, 200, 0, 0, 0)
            self.game_data.item.put_player_quest(user_id, 1001, True, 300, 0, 0, 1)

            # Force the tutorial stage to be completed due to potential crash in-game
            

        self.logger.info(f"User Authenticated: { access_code } | { user_id }")

        #Grab values from profile
        profile_data = self.game_data.profile.get_profile(user_id)

        if user_id and not profile_data:
            profile_id = self.game_data.profile.create_profile(user_id)
            self.game_data.item.put_hero_log(user_id, 101000010, 1, 0, 101000016, 0, 30086, 1001, 1002, 1003, 1005)
            self.game_data.item.put_hero_log(user_id, 102000010, 1, 0, 103000006, 0, 30086, 1001, 1002, 1003, 1005)
            self.game_data.item.put_hero_log(user_id, 103000010, 1, 0, 112000009, 0, 30086, 1001, 1002, 1003, 1005)
            self.game_data.item.put_hero_party(user_id, 0, 101000010, 102000010, 103000010)
            self.game_data.item.put_equipment_data(user_id, 101000016, 1, 200, 0, 0, 0)
            self.game_data.item.put_equipment_data(user_id, 103000006, 1, 200, 0, 0, 0)
            self.game_data.item.put_equipment_data(user_id, 112000009, 1, 200, 0, 0, 0)
            self.game_data.item.put_player_quest(user_id, 1001, True, 300, 0, 0, 1)

            # Force the tutorial stage to be completed due to potential crash in-game


            profile_data = self.game_data.profile.get_profile(user_id)

        resp = SaoGetAuthCardDataResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, profile_data)
        return resp.make()

    def handle_c40c(self, request: Any) -> bytes:
        #home/check_ac_login_bonus
        resp = SaoHomeCheckAcLoginBonusResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c104(self, request: Any) -> bytes:
        #common/login
        req = bytes.fromhex(request)[24:]

        req_struct = Struct(
            Padding(16),
            "cabinet_type" / Int8ub,  # cabinet_type is a byte
            "auth_type" / Int8ub,  # auth_type is a byte
            "store_id_size" / Rebuild(Int32ub, len_(this.store_id) * 2),  # calculates the length of the store_id
            "store_id" / PaddedString(this.store_id_size, "utf_16_le"),  # store_id is a (zero) padded string
            "store_name_size" / Rebuild(Int32ub, len_(this.store_name) * 2),  # calculates the length of the store_name
            "store_name" / PaddedString(this.store_name_size, "utf_16_le"),  # store_name is a (zero) padded string
            "serial_no_size" / Rebuild(Int32ub, len_(this.serial_no) * 2),  # calculates the length of the serial_no
            "serial_no" / PaddedString(this.serial_no_size, "utf_16_le"),  # serial_no is a (zero) padded string
            "access_code_size" / Rebuild(Int32ub, len_(this.access_code) * 2),  # calculates the length of the access_code
            "access_code" / PaddedString(this.access_code_size, "utf_16_le"),  # access_code is a (zero) padded string
            "chip_id_size" / Rebuild(Int32ub, len_(this.chip_id) * 2),  # calculates the length of the chip_id
            "chip_id" / PaddedString(this.chip_id_size, "utf_16_le"),  # chip_id is a (zero) padded string
            "free_ticket_distribution_target_flag" / Int8ub,  # free_ticket_distribution_target_flag is a byte
        )

        req_data = req_struct.parse(req)
        access_code = req_data.access_code

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
        req = bytes.fromhex(request)[24:]

        req_struct = Struct(
            Padding(16),
            "user_id_size" / Rebuild(Int32ub, len_(this.user_id) * 2),  # calculates the length of the user_id
            "user_id" / PaddedString(this.user_id_size, "utf_16_le"),  # user_id is a (zero) padded string
        )

        req_data = req_struct.parse(req)
        user_id = req_data.user_id

        profile_data = self.game_data.profile.get_profile(user_id)

        resp = SaoGetUserBasicDataResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, profile_data)
        return resp.make()
        
    def handle_c600(self, request: Any) -> bytes:
        #have_object/get_hero_log_user_data_list
        req = bytes.fromhex(request)[24:]
        
        req_struct = Struct(
            Padding(16),
            "user_id_size" / Rebuild(Int32ub, len_(this.user_id) * 2),  # calculates the length of the user_id
            "user_id" / PaddedString(this.user_id_size, "utf_16_le"),  # user_id is a (zero) padded string

        )
        req_data = req_struct.parse(req)
        user_id = req_data.user_id

        hero_data = self.game_data.item.get_hero_logs(user_id)
        
        resp = SaoGetHeroLogUserDataListResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, hero_data)
        return resp.make()
    
    def handle_c602(self, request: Any) -> bytes:
        #have_object/get_equipment_user_data_list
        req = bytes.fromhex(request)[24:]

        req_struct = Struct(
            Padding(16),
            "user_id_size" / Rebuild(Int32ub, len_(this.user_id) * 2),  # calculates the length of the user_id
            "user_id" / PaddedString(this.user_id_size, "utf_16_le"),  # user_id is a (zero) padded string

        )
        req_data = req_struct.parse(req)
        user_id = req_data.user_id
    
        equipment_data = self.game_data.item.get_user_equipments(user_id)

        resp = SaoGetEquipmentUserDataListResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, equipment_data)
        return resp.make()
        
    def handle_c604(self, request: Any) -> bytes:
        #have_object/get_item_user_data_list
        req = bytes.fromhex(request)[24:]

        req_struct = Struct(
            Padding(16),
            "user_id_size" / Rebuild(Int32ub, len_(this.user_id) * 2),  # calculates the length of the user_id
            "user_id" / PaddedString(this.user_id_size, "utf_16_le"),  # user_id is a (zero) padded string

        )
        req_data = req_struct.parse(req)
        user_id = req_data.user_id

        item_data = self.game_data.item.get_user_items(user_id)

        resp = SaoGetItemUserDataListResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, item_data)
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
        req = bytes.fromhex(request)[24:]

        req_struct = Struct(
            Padding(16),
            "user_id_size" / Rebuild(Int32ub, len_(this.user_id) * 2),  # calculates the length of the user_id
            "user_id" / PaddedString(this.user_id_size, "utf_16_le"),  # user_id is a (zero) padded string
        )

        req_data = req_struct.parse(req)
        user_id = req_data.user_id

        profile_data = self.game_data.profile.get_profile(user_id)

        resp = SaoGetEpisodeAppendDataListResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, profile_data)
        return resp.make()

    def handle_c804(self, request: Any) -> bytes:
        #custom/get_party_data_list
        req = bytes.fromhex(request)[24:]

        req_struct = Struct(
            Padding(16),
            "user_id_size" / Rebuild(Int32ub, len_(this.user_id) * 2),  # calculates the length of the user_id
            "user_id" / PaddedString(this.user_id_size, "utf_16_le"),  # user_id is a (zero) padded string

        )
        req_data = req_struct.parse(req)
        user_id = req_data.user_id

        hero_party = self.game_data.item.get_hero_party(user_id, 0)
        hero1_data = self.game_data.item.get_hero_log(user_id, hero_party[3])
        hero2_data = self.game_data.item.get_hero_log(user_id, hero_party[4])
        hero3_data = self.game_data.item.get_hero_log(user_id, hero_party[5])

        resp = SaoGetPartyDataListResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, hero1_data, hero2_data, hero3_data)
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
        req = bytes.fromhex(request)[24:]

        req_struct = Struct(
            Padding(16),
            "user_id_size" / Rebuild(Int32ub, len_(this.user_id) * 2),  # calculates the length of the user_id
            "user_id" / PaddedString(this.user_id_size, "utf_16_le"),  # user_id is a (zero) padded string

        )
        req_data = req_struct.parse(req)
        user_id = req_data.user_id

        quest_data = self.game_data.item.get_quest_logs(user_id)

        resp = SaoGetQuestSceneUserDataListResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, quest_data)
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

    def handle_c814(self, request: Any) -> bytes:
        #custom/synthesize_enhancement_hero_log
        req = bytes.fromhex(request)[24:]

        req_struct = Struct(
            Padding(20),
            "ticket_id" / Bytes(1),  # needs to be parsed as an int
            Padding(1),
            "user_id_size" / Rebuild(Int32ub, len_(this.user_id) * 2),  # calculates the length of the user_id
            "user_id" / PaddedString(this.user_id_size, "utf_16_le"),  # user_id is a (zero) padded string
            "origin_user_hero_log_id_size" / Rebuild(Int32ub, len_(this.origin_user_hero_log_id) * 2),  # calculates the length of the origin_user_hero_log_id
            "origin_user_hero_log_id" / PaddedString(this.origin_user_hero_log_id_size, "utf_16_le"),  # origin_user_hero_log_id is a (zero) padded string
            Padding(3),
            "material_common_reward_user_data_list_length" / Rebuild(Int8ub, len_(this.material_common_reward_user_data_list)),  # material_common_reward_user_data_list is a byte,
            "material_common_reward_user_data_list" / Array(this.material_common_reward_user_data_list_length, Struct(
                "common_reward_type" / Int16ub,  # team_no is a byte
                "user_common_reward_id_size" / Rebuild(Int32ub, len_(this.user_common_reward_id) * 2),  # calculates the length of the user_common_reward_id
                "user_common_reward_id" / PaddedString(this.user_common_reward_id_size, "utf_16_le"),  # user_common_reward_id is a (zero) padded string
            )),
        )

        req_data = req_struct.parse(req)
        user_id = req_data.user_id
        synthesize_hero_log_data = self.game_data.item.get_hero_log(req_data.user_id, req_data.origin_user_hero_log_id)

        for i in range(0,req_data.material_common_reward_user_data_list_length):

            itemList = self.game_data.static.get_item_id(req_data.material_common_reward_user_data_list[i].user_common_reward_id)
            heroList = self.game_data.static.get_hero_id(req_data.material_common_reward_user_data_list[i].user_common_reward_id)
            equipmentList = self.game_data.static.get_equipment_id(req_data.material_common_reward_user_data_list[i].user_common_reward_id)

            if itemList:
                hero_exp = 2000 + int(synthesize_hero_log_data["log_exp"])
                self.game_data.item.remove_item(req_data.user_id, req_data.material_common_reward_user_data_list[i].user_common_reward_id)

            if equipmentList:
                equipment_data = self.game_data.item.get_user_equipment(req_data.user_id, req_data.material_common_reward_user_data_list[i].user_common_reward_id)
                hero_exp = int(equipment_data["enhancement_exp"]) + int(synthesize_hero_log_data["log_exp"])
                self.game_data.item.remove_equipment(req_data.user_id, req_data.material_common_reward_user_data_list[i].user_common_reward_id)

            if heroList:
                hero_data = self.game_data.item.get_hero_log(req_data.user_id, req_data.material_common_reward_user_data_list[i].user_common_reward_id)
                hero_exp = int(hero_data["log_exp"]) + int(synthesize_hero_log_data["log_exp"])
                self.game_data.item.remove_hero_log(req_data.user_id, req_data.material_common_reward_user_data_list[i].user_common_reward_id)

            self.game_data.item.put_hero_log(
                user_id, 
                int(req_data.origin_user_hero_log_id), 
                synthesize_hero_log_data["log_level"], 
                hero_exp, 
                synthesize_hero_log_data["main_weapon"], 
                synthesize_hero_log_data["sub_equipment"], 
                synthesize_hero_log_data["skill_slot1_skill_id"], 
                synthesize_hero_log_data["skill_slot2_skill_id"], 
                synthesize_hero_log_data["skill_slot3_skill_id"], 
                synthesize_hero_log_data["skill_slot4_skill_id"], 
                synthesize_hero_log_data["skill_slot5_skill_id"]
            )

            profile = self.game_data.profile.get_profile(req_data.user_id)
            new_col = int(profile["own_col"]) - 100

            # Update profile
            
            self.game_data.profile.put_profile(
                req_data.user_id,
                profile["user_type"], 
                profile["nick_name"], 
                profile["rank_num"],
                profile["rank_exp"],
                new_col,
                profile["own_vp"], 
                profile["own_yui_medal"], 
                profile["setting_title_id"]
            )

        # Load the item again to push to the response handler  
        synthesize_hero_log_data = self.game_data.item.get_hero_log(req_data.user_id, req_data.origin_user_hero_log_id)

        resp = SaoSynthesizeEnhancementHeroLogResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, synthesize_hero_log_data)
        return resp.make()

    def handle_c816(self, request: Any) -> bytes:
        #custom/synthesize_enhancement_equipment
        req = bytes.fromhex(request)[24:]

        req_struct = Struct(
            Padding(20),
            "ticket_id" / Bytes(1),  # needs to be parsed as an int
            Padding(1),
            "user_id_size" / Rebuild(Int32ub, len_(this.user_id) * 2),  # calculates the length of the user_id
            "user_id" / PaddedString(this.user_id_size, "utf_16_le"),  # user_id is a (zero) padded string
            "origin_user_equipment_id_size" / Rebuild(Int32ub, len_(this.origin_user_equipment_id) * 2),  # calculates the length of the origin_user_equipment_id
            "origin_user_equipment_id" / PaddedString(this.origin_user_equipment_id_size, "utf_16_le"),  # origin_user_equipment_id is a (zero) padded string
            Padding(3),
            "material_common_reward_user_data_list_length" / Rebuild(Int8ub, len_(this.material_common_reward_user_data_list)),  # material_common_reward_user_data_list is a byte,
            "material_common_reward_user_data_list" / Array(this.material_common_reward_user_data_list_length, Struct(
                "common_reward_type" / Int16ub,  # team_no is a byte
                "user_common_reward_id_size" / Rebuild(Int32ub, len_(this.user_common_reward_id) * 2),  # calculates the length of the user_common_reward_id
                "user_common_reward_id" / PaddedString(this.user_common_reward_id_size, "utf_16_le"),  # user_common_reward_id is a (zero) padded string
            )),
        )

        req_data = req_struct.parse(req)

        user_id = req_data.user_id
        synthesize_equipment_data = self.game_data.item.get_user_equipment(req_data.user_id, req_data.origin_user_equipment_id)

        for i in range(0,req_data.material_common_reward_user_data_list_length):

            itemList = self.game_data.static.get_item_id(req_data.material_common_reward_user_data_list[i].user_common_reward_id)
            heroList = self.game_data.static.get_hero_id(req_data.material_common_reward_user_data_list[i].user_common_reward_id)
            equipmentList = self.game_data.static.get_equipment_id(req_data.material_common_reward_user_data_list[i].user_common_reward_id)

            if itemList:
                equipment_exp = 2000 + int(synthesize_equipment_data["enhancement_exp"])
                self.game_data.item.remove_item(req_data.user_id, req_data.material_common_reward_user_data_list[i].user_common_reward_id)

            if equipmentList:
                equipment_data = self.game_data.item.get_user_equipment(req_data.user_id, req_data.material_common_reward_user_data_list[i].user_common_reward_id)
                equipment_exp = int(equipment_data["enhancement_exp"]) + int(synthesize_equipment_data["enhancement_exp"])
                self.game_data.item.remove_equipment(req_data.user_id, req_data.material_common_reward_user_data_list[i].user_common_reward_id)

            if heroList:
                hero_data = self.game_data.item.get_hero_log(req_data.user_id, req_data.material_common_reward_user_data_list[i].user_common_reward_id)
                equipment_exp = int(hero_data["log_exp"]) + int(synthesize_equipment_data["enhancement_exp"])
                self.game_data.item.remove_hero_log(req_data.user_id, req_data.material_common_reward_user_data_list[i].user_common_reward_id)

            self.game_data.item.put_equipment_data(req_data.user_id, int(req_data.origin_user_equipment_id), synthesize_equipment_data["enhancement_value"], equipment_exp, 0, 0, 0)

            profile = self.game_data.profile.get_profile(req_data.user_id)
            new_col = int(profile["own_col"]) - 100

            # Update profile
            
            self.game_data.profile.put_profile(
                req_data.user_id,
                profile["user_type"], 
                profile["nick_name"], 
                profile["rank_num"],
                profile["rank_exp"],
                new_col,
                profile["own_vp"], 
                profile["own_yui_medal"], 
                profile["setting_title_id"]
                )

        # Load the item again to push to the response handler  
        synthesize_equipment_data = self.game_data.item.get_user_equipment(req_data.user_id, req_data.origin_user_equipment_id)

        resp = SaoSynthesizeEnhancementEquipmentResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, synthesize_equipment_data)
        return resp.make()

    def handle_c806(self, request: Any) -> bytes:
        #custom/change_party
        req = bytes.fromhex(request)[24:]

        req_struct = Struct(
            Padding(20),
            "ticket_id" / Bytes(1),  # needs to be parsed as an int
            Padding(1),
            "user_id_size" / Rebuild(Int32ub, len_(this.user_id) * 2),  # calculates the length of the user_id
            "user_id" / PaddedString(this.user_id_size, "utf_16_le"),  # user_id is a (zero) padded string
            "act_type" / Int8ub,  # play_mode is a byte
            Padding(3),
            "party_data_list_length" / Rebuild(Int8ub, len_(this.party_data_list)),  # party_data_list is a byte,
            "party_data_list" / Array(this.party_data_list_length, Struct(
                "user_party_id_size" / Rebuild(Int32ub, len_(this.user_party_id) * 2),  # calculates the length of the user_party_id
                "user_party_id" / PaddedString(this.user_party_id_size, "utf_16_le"),  # user_party_id is a (zero) padded string
                "team_no" / Int8ub,  # team_no is a byte
            Padding(3),
            "party_team_data_list_length" / Rebuild(Int8ub, len_(this.party_team_data_list)),  # party_team_data_list is a byte
            "party_team_data_list" / Array(this.party_team_data_list_length, Struct(
                "user_party_team_id_size" / Rebuild(Int32ub, len_(this.user_party_team_id) * 2),  # calculates the length of the user_party_team_id
                "user_party_team_id" / PaddedString(this.user_party_team_id_size, "utf_16_le"),  # user_party_team_id is a (zero) padded string
                "arrangement_num" / Int8ub,  # arrangement_num is a byte
                "user_hero_log_id_size" / Rebuild(Int32ub, len_(this.user_hero_log_id) * 2),  # calculates the length of the user_hero_log_id
                "user_hero_log_id" / PaddedString(this.user_hero_log_id_size, "utf_16_le"),  # user_hero_log_id is a (zero) padded string
                "main_weapon_user_equipment_id_size" / Rebuild(Int32ub, len_(this.main_weapon_user_equipment_id) * 2),  # calculates the length of the main_weapon_user_equipment_id
                "main_weapon_user_equipment_id" / PaddedString(this.main_weapon_user_equipment_id_size, "utf_16_le"),  # main_weapon_user_equipment_id is a (zero) padded string
                "sub_equipment_user_equipment_id_size" / Rebuild(Int32ub, len_(this.sub_equipment_user_equipment_id) * 2),  # calculates the length of the sub_equipment_user_equipment_id
                "sub_equipment_user_equipment_id" / PaddedString(this.sub_equipment_user_equipment_id_size, "utf_16_le"),  # sub_equipment_user_equipment_id is a (zero) padded string
                "skill_slot1_skill_id" / Int32ub,  # skill_slot1_skill_id is a int,
                "skill_slot2_skill_id" / Int32ub,  # skill_slot1_skill_id is a int,
                "skill_slot3_skill_id" / Int32ub,  # skill_slot1_skill_id is a int,
                "skill_slot4_skill_id" / Int32ub,  # skill_slot1_skill_id is a int,
                "skill_slot5_skill_id" / Int32ub,  # skill_slot1_skill_id is a int,
            )),
            )),

        )

        req_data = req_struct.parse(req)
        user_id = req_data.user_id
        party_hero_list = []

        for party_team in req_data.party_data_list[0].party_team_data_list:
            hero_data = self.game_data.item.get_hero_log(user_id, party_team["user_hero_log_id"])
            hero_level = 1
            hero_exp = 0

            if hero_data:
                hero_level = hero_data["log_level"]
                hero_exp = hero_data["log_exp"]

            self.game_data.item.put_hero_log(
                user_id,
                party_team["user_hero_log_id"],
                hero_level,
                hero_exp,
                party_team["main_weapon_user_equipment_id"],
                party_team["sub_equipment_user_equipment_id"],
                party_team["skill_slot1_skill_id"],
                party_team["skill_slot2_skill_id"],
                party_team["skill_slot3_skill_id"],
                party_team["skill_slot4_skill_id"],
                party_team["skill_slot5_skill_id"]
            )

            party_hero_list.append(party_team["user_hero_log_id"])

        self.game_data.item.put_hero_party(user_id, req_data.party_data_list[0].party_team_data_list[0].user_party_team_id, party_hero_list[0], party_hero_list[1], party_hero_list[2])

        resp = SaoNoopResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c904(self, request: Any) -> bytes:
        #quest/episode_play_start
        req = bytes.fromhex(request)[24:]

        req_struct = Struct(
            Padding(20),
            "ticket_id" / Bytes(1),  # needs to be parsed as an int
            Padding(1),
            "user_id_size" / Rebuild(Int32ub, len_(this.user_id) * 2),  # calculates the length of the user_id
            "user_id" / PaddedString(this.user_id_size, "utf_16_le"),  # user_id is a (zero) padded string
            "episode_id" / Int32ub,  # episode_id is a int,
            "play_mode" / Int8ub,  # play_mode is a byte
            Padding(3),
            "play_start_request_data_length" / Rebuild(Int8ub, len_(this.play_start_request_data)),  # play_start_request_data_length is a byte,
            "play_start_request_data" / Array(this.play_start_request_data_length, Struct(
                "user_party_id_size" / Rebuild(Int32ub, len_(this.user_party_id) * 2),  # calculates the length of the user_party_id
                "user_party_id" / PaddedString(this.user_party_id_size, "utf_16_le"),  # user_party_id is a (zero) padded string
                "appoint_leader_resource_card_code_size" / Rebuild(Int32ub, len_(this.appoint_leader_resource_card_code) * 2),  # calculates the length of the total_damage
                "appoint_leader_resource_card_code" / PaddedString(this.appoint_leader_resource_card_code_size, "utf_16_le"),  # total_damage is a (zero) padded string
                "use_profile_card_code_size" / Rebuild(Int32ub, len_(this.use_profile_card_code) * 2),  # calculates the length of the total_damage
                "use_profile_card_code" / PaddedString(this.use_profile_card_code_size, "utf_16_le"),  # use_profile_card_code is a (zero) padded string
                "quest_drop_boost_apply_flag" / Int8ub,  # quest_drop_boost_apply_flag is a byte
            )),

        )

        req_data = req_struct.parse(req)

        user_id = req_data.user_id
        profile_data = self.game_data.profile.get_profile(user_id)

        self.game_data.item.create_session(
            user_id, 
            int(req_data.play_start_request_data[0].user_party_id), 
            req_data.episode_id, 
            req_data.play_mode, 
            req_data.play_start_request_data[0].quest_drop_boost_apply_flag
            )

        resp = SaoEpisodePlayStartResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, profile_data)
        return resp.make()

    def handle_c908(self, request: Any) -> bytes: # Level calculation missing for the profile and heroes
        #quest/episode_play_end

        req = bytes.fromhex(request)[24:]

        req_struct = Struct(
            Padding(20),
            "ticket_id" / Bytes(1),  # needs to be parsed as an int
            Padding(1),
            "user_id_size" / Rebuild(Int32ub, len_(this.user_id) * 2),  # calculates the length of the user_id
            "user_id" / PaddedString(this.user_id_size, "utf_16_le"),  # user_id is a (zero) padded string
            Padding(2),
            "episode_id" / Int16ub,  # episode_id is a short,
            Padding(3),
            "play_end_request_data" / Int8ub,  # play_end_request_data is a byte
            Padding(1),
            "play_result_flag" / Int8ub,  # play_result_flag is a byte
            Padding(2),
            "base_get_data_length" / Rebuild(Int8ub, len_(this.base_get_data)),  # base_get_data_length is a byte,
            "base_get_data" / Array(this.base_get_data_length, Struct(
                "get_hero_log_exp" / Int32ub,  # get_hero_log_exp is an int
                "get_col" / Int32ub,  # get_num is a short
            )),
            Padding(3),
            "get_player_trace_data_list_length" / Rebuild(Int8ub, len_(this.get_player_trace_data_list)),  # get_player_trace_data_list_length is a byte
            "get_player_trace_data_list" / Array(this.get_player_trace_data_list_length, Struct(
                "user_quest_scene_player_trace_id" / Int32ub,  # user_quest_scene_player_trace_id is an int
            )),
            Padding(3),
            "get_rare_drop_data_list_length" / Rebuild(Int8ub, len_(this.get_rare_drop_data_list)),  # get_rare_drop_data_list_length is a byte
            "get_rare_drop_data_list" / Array(this.get_rare_drop_data_list_length, Struct(
                "quest_rare_drop_id" / Int32ub,  # quest_rare_drop_id is an int
            )),
            Padding(3),
            "get_special_rare_drop_data_list_length" / Rebuild(Int8ub, len_(this.get_special_rare_drop_data_list)),  # get_special_rare_drop_data_list_length is a byte
            "get_special_rare_drop_data_list" / Array(this.get_special_rare_drop_data_list_length, Struct(
                "quest_special_rare_drop_id" / Int32ub,  # quest_special_rare_drop_id is an int
            )),
            Padding(3),
            "get_unanalyzed_log_tmp_reward_data_list_length" / Rebuild(Int8ub, len_(this.get_unanalyzed_log_tmp_reward_data_list)),  # get_unanalyzed_log_tmp_reward_data_list_length is a byte
            "get_unanalyzed_log_tmp_reward_data_list" / Array(this.get_unanalyzed_log_tmp_reward_data_list_length, Struct(
                "unanalyzed_log_grade_id" / Int32ub,  # unanalyzed_log_grade_id is an int,
            )),
            Padding(3),
            "get_event_item_data_list_length" / Rebuild(Int8ub, len_(this.get_event_item_data_list)),  # get_event_item_data_list_length is a byte,
            "get_event_item_data_list" / Array(this.get_event_item_data_list_length, Struct(
                "event_item_id" / Int32ub,  # event_item_id is an int
                "get_num" / Int16ub,  # get_num is a short
            )),
            Padding(3),
            "discovery_enemy_data_list_length" / Rebuild(Int8ub, len_(this.discovery_enemy_data_list)),  # discovery_enemy_data_list_length is a byte
            "discovery_enemy_data_list" / Array(this.discovery_enemy_data_list_length, Struct(
                "enemy_kind_id" / Int32ub,  # enemy_kind_id is an int
                "destroy_num" / Int16ub,  # destroy_num is a short
            )),
            Padding(3),
            "destroy_boss_data_list_length" / Rebuild(Int8ub, len_(this.destroy_boss_data_list)),  # destroy_boss_data_list_length is a byte
            "destroy_boss_data_list" / Array(this.destroy_boss_data_list_length, Struct(
                "boss_type" / Int8ub,  # boss_type is a byte
                "enemy_kind_id" / Int32ub,  # enemy_kind_id is an int
                "destroy_num" / Int16ub,  # destroy_num is a short
            )),
            Padding(3),
            "mission_data_list_length" / Rebuild(Int8ub, len_(this.mission_data_list)),  # mission_data_list_length is a byte
            "mission_data_list" / Array(this.mission_data_list_length, Struct(
                "mission_id" / Int32ub,  # enemy_kind_id is an int
                "clear_flag" / Int8ub,  # boss_type is a byte
                "mission_difficulty_id" / Int16ub,  # destroy_num is a short
            )),
            Padding(3),
            "score_data_length" / Rebuild(Int8ub, len_(this.score_data)),  # score_data_length is a byte
            "score_data" / Array(this.score_data_length, Struct(
                "clear_time" / Int32ub,  # clear_time is an int
                "combo_num" / Int32ub,  # boss_type is a int
                "total_damage_size" / Rebuild(Int32ub, len_(this.total_damage) * 2),  # calculates the length of the total_damage
                "total_damage" / PaddedString(this.total_damage_size, "utf_16_le"),  # total_damage is a (zero) padded string
                "concurrent_destroying_num" / Int16ub, # concurrent_destroying_num is a short
                "reaching_skill_level" / Int16ub, # reaching_skill_level is a short
                "ko_chara_num" / Int8ub,  # ko_chara_num is a byte
                "acceleration_invocation_num" / Int16ub, # acceleration_invocation_num is a short
                "boss_destroying_num" / Int16ub, # boss_destroying_num is a short
                "synchro_skill_used_flag" / Int8ub,  # synchro_skill_used_flag is a byte
                "used_friend_skill_id" / Int32ub,  # used_friend_skill_id is an int
                "friend_skill_used_flag" / Int8ub,  # friend_skill_used_flag is a byte
                "continue_cnt" / Int16ub, # continue_cnt is a short
                "total_loss_num" / Int16ub, # total_loss_num is a short
            )),

        )

        req_data = req_struct.parse(req)

        # Add stage progression to database
        user_id = req_data.user_id
        episode_id = req_data.episode_id
        quest_clear_flag = bool(req_data.score_data[0].boss_destroying_num)
        clear_time = req_data.score_data[0].clear_time
        combo_num = req_data.score_data[0].combo_num
        total_damage = req_data.score_data[0].total_damage
        concurrent_destroying_num = req_data.score_data[0].concurrent_destroying_num

        profile = self.game_data.profile.get_profile(user_id)
        vp = int(profile["own_vp"])
        exp = int(profile["rank_exp"]) + 100 #always 100 extra exp for some reason
        col = int(profile["own_col"]) + int(req_data.base_get_data[0].get_col)

        if quest_clear_flag is True:
            # Save stage progression - to be revised to avoid saving worse score

            # Reference Episode.csv but Chapter 2,3,4 and 5 reports id -1, match using /10 + last digits
            if episode_id > 10000 and episode_id < 11000:
                # Starts at 1001
                episode_id = episode_id - 9000
            elif episode_id > 20000:
                # Starts at 2001
                stage_id = str(episode_id)[-2:]
                episode_id = episode_id / 10
                episode_id = int(episode_id) + int(stage_id)

                # Match episode_id with the questSceneId saved in the DB through sortNo
                questId = self.game_data.static.get_quests_id(episode_id)
                episode_id = questId[2]

            self.game_data.item.put_player_quest(user_id, episode_id, quest_clear_flag, clear_time, combo_num, total_damage, concurrent_destroying_num)

            vp = int(profile["own_vp"]) + 10 #always 10 VP per cleared stage


        # Calculate level based off experience and the CSV list
        with open(r'titles/sao/data/PlayerRank.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            data = []
            rowf = False
            for row in csv_reader:
                if rowf==False:
                    rowf=True
                else:
                    data.append(row)           
            
        for i in range(0,len(data)):
            if exp>=int(data[i][1]) and exp<int(data[i+1][1]):
                player_level = int(data[i][0])
                break

        # Update profile
        updated_profile = self.game_data.profile.put_profile(
            user_id,
            profile["user_type"], 
            profile["nick_name"], 
            player_level,
            exp,
            col,
            vp, 
            profile["own_yui_medal"], 
            profile["setting_title_id"]
            )

        # Update heroes from the used party
        play_session = self.game_data.item.get_session(user_id)
        session_party = self.game_data.item.get_hero_party(user_id, play_session["user_party_team_id"])

        hero_list = []
        hero_list.append(session_party["user_hero_log_id_1"])
        hero_list.append(session_party["user_hero_log_id_2"])
        hero_list.append(session_party["user_hero_log_id_3"])

        for i in range(0,len(hero_list)):
            hero_data = self.game_data.item.get_hero_log(user_id, hero_list[i])

            log_exp = int(hero_data["log_exp"]) + int(req_data.base_get_data[0].get_hero_log_exp)

            # Calculate hero level based off experience and the CSV list
            with open(r'titles/sao/data/HeroLogLevel.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                data = []
                rowf = False
                for row in csv_reader:
                    if rowf==False:
                        rowf=True
                    else:
                        data.append(row)
                
            for e in range(0,len(data)):
                if log_exp>=int(data[e][1]) and log_exp<int(data[e+1][1]):
                    hero_level = int(data[e][0])
                    break

            self.game_data.item.put_hero_log(
                user_id,
                hero_data["user_hero_log_id"],
                hero_level,
                log_exp,
                hero_data["main_weapon"],
                hero_data["sub_equipment"],
                hero_data["skill_slot1_skill_id"],
                hero_data["skill_slot2_skill_id"],
                hero_data["skill_slot3_skill_id"],
                hero_data["skill_slot4_skill_id"],
                hero_data["skill_slot5_skill_id"]
            )

        # Grab the rare loot from the table, match it with the right item and then push to the player profile
        for r in range(0,req_data.get_rare_drop_data_list_length):
            rewardList = self.game_data.static.get_rare_drop_id(int(req_data.get_rare_drop_data_list[r].quest_rare_drop_id))
            commonRewardId = rewardList["commonRewardId"]

            heroList = self.game_data.static.get_hero_id(commonRewardId)
            equipmentList = self.game_data.static.get_equipment_id(commonRewardId)
            itemList = self.game_data.static.get_item_id(commonRewardId)

            if heroList:
                self.game_data.item.put_hero_log(user_id, commonRewardId, 1, 0, 101000016, 0, 30086, 1001, 1002, 0, 0)
            if equipmentList:
                self.game_data.item.put_equipment_data(user_id, commonRewardId, 1, 200, 0, 0, 0)
            if itemList:
                self.game_data.item.put_item(user_id, commonRewardId)
        
        # Generate random hero(es) based off the response    
        for a in range(0,req_data.get_unanalyzed_log_tmp_reward_data_list_length):
            
            with open('titles/sao/data/RewardTable.csv', 'r') as f:
                keys_unanalyzed = next(f).strip().split(',')
                data_unanalyzed = list(DictReader(f, fieldnames=keys_unanalyzed))

            randomized_unanalyzed_id = choice(data_unanalyzed)
            while int(randomized_unanalyzed_id['UnanalyzedLogGradeId']) != req_data.get_unanalyzed_log_tmp_reward_data_list[a].unanalyzed_log_grade_id:
                randomized_unanalyzed_id = choice(data_unanalyzed)
            
            heroList = self.game_data.static.get_hero_id(randomized_unanalyzed_id['CommonRewardId'])
            equipmentList = self.game_data.static.get_equipment_id(randomized_unanalyzed_id['CommonRewardId'])
            itemList = self.game_data.static.get_item_id(randomized_unanalyzed_id['CommonRewardId'])
            if heroList:
                self.game_data.item.put_hero_log(user_id, randomized_unanalyzed_id['CommonRewardId'], 1, 0, 101000016, 0, 30086, 1001, 1002, 0, 0)
            if equipmentList:
                self.game_data.item.put_equipment_data(user_id, randomized_unanalyzed_id['CommonRewardId'], 1, 200, 0, 0, 0)
            if itemList:
                self.game_data.item.put_item(user_id, randomized_unanalyzed_id['CommonRewardId'])
            
        # Send response

        resp = SaoEpisodePlayEndResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c914(self, request: Any) -> bytes:
        #quest/trial_tower_play_start
        req = bytes.fromhex(request)[24:]

        req_struct = Struct(
            Padding(16),
            "ticket_id_size" / Rebuild(Int32ub, len_(this.ticket_id) * 2),  # calculates the length of the ticket_id
            "ticket_id" / PaddedString(this.ticket_id_size, "utf_16_le"),  # ticket_id is a (zero) padded string
            "user_id_size" / Rebuild(Int32ub, len_(this.user_id) * 2),  # calculates the length of the user_id
            "user_id" / PaddedString(this.user_id_size, "utf_16_le"),  # user_id is a (zero) padded string
            "trial_tower_id" / Int32ub,  # trial_tower_id is an int
            "play_mode" / Int8ub,  # play_mode is a byte
            Padding(3),
            "play_start_request_data_length" / Rebuild(Int8ub, len_(this.play_start_request_data)),  # play_start_request_data_length is a byte,
            "play_start_request_data" / Array(this.play_start_request_data_length, Struct(
                "user_party_id_size" / Rebuild(Int32ub, len_(this.user_party_id) * 2),  # calculates the length of the user_party_id
                "user_party_id" / PaddedString(this.user_party_id_size, "utf_16_le"),  # user_party_id is a (zero) padded string
                "appoint_leader_resource_card_code_size" / Rebuild(Int32ub, len_(this.appoint_leader_resource_card_code) * 2),  # calculates the length of the total_damage
                "appoint_leader_resource_card_code" / PaddedString(this.appoint_leader_resource_card_code_size, "utf_16_le"),  # total_damage is a (zero) padded string
                "use_profile_card_code_size" / Rebuild(Int32ub, len_(this.use_profile_card_code) * 2),  # calculates the length of the total_damage
                "use_profile_card_code" / PaddedString(this.use_profile_card_code_size, "utf_16_le"),  # use_profile_card_code is a (zero) padded string
                "quest_drop_boost_apply_flag" / Int8ub,  # quest_drop_boost_apply_flag is a byte
            )),
        )

        req_data = req_struct.parse(req)

        user_id = req_data.user_id
        floor_id = req_data.trial_tower_id
        profile_data = self.game_data.profile.get_profile(user_id)

        self.game_data.item.create_session(
            user_id, 
            int(req_data.play_start_request_data[0].user_party_id), 
            req_data.trial_tower_id, 
            req_data.play_mode, 
            req_data.play_start_request_data[0].quest_drop_boost_apply_flag
            )

        resp = SaoEpisodePlayStartResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1, profile_data)
        return resp.make()

    def handle_c918(self, request: Any) -> bytes:
        #quest/trial_tower_play_end
        req = bytes.fromhex(request)[24:]

        req_struct = Struct(
            Padding(20),
            "ticket_id" / Bytes(1),  # needs to be parsed as an int
            Padding(1),
            "user_id_size" / Rebuild(Int32ub, len_(this.user_id) * 2),  # calculates the length of the user_id
            "user_id" / PaddedString(this.user_id_size, "utf_16_le"),  # user_id is a (zero) padded string
            Padding(2),
            "trial_tower_id" / Int16ub,  # trial_tower_id is a short,
            Padding(3),
            "play_end_request_data" / Int8ub,  # play_end_request_data is a byte
            Padding(1),
            "play_result_flag" / Int8ub,  # play_result_flag is a byte
            Padding(2),
            "base_get_data_length" / Rebuild(Int8ub, len_(this.base_get_data)),  # base_get_data_length is a byte,
            "base_get_data" / Array(this.base_get_data_length, Struct(
                "get_hero_log_exp" / Int32ub,  # get_hero_log_exp is an int
                "get_col" / Int32ub,  # get_num is a short
            )),
            Padding(3),
            "get_player_trace_data_list_length" / Rebuild(Int8ub, len_(this.get_player_trace_data_list)),  # get_player_trace_data_list_length is a byte
            "get_player_trace_data_list" / Array(this.get_player_trace_data_list_length, Struct(
                "user_quest_scene_player_trace_id" / Int32ub,  # user_quest_scene_player_trace_id is an int
            )),
            Padding(3),
            "get_rare_drop_data_list_length" / Rebuild(Int8ub, len_(this.get_rare_drop_data_list)),  # get_rare_drop_data_list_length is a byte
            "get_rare_drop_data_list" / Array(this.get_rare_drop_data_list_length, Struct(
                "quest_rare_drop_id" / Int32ub,  # quest_rare_drop_id is an int
            )),
            Padding(3),
            "get_special_rare_drop_data_list_length" / Rebuild(Int8ub, len_(this.get_special_rare_drop_data_list)),  # get_special_rare_drop_data_list_length is a byte
            "get_special_rare_drop_data_list" / Array(this.get_special_rare_drop_data_list_length, Struct(
                "quest_special_rare_drop_id" / Int32ub,  # quest_special_rare_drop_id is an int
            )),
            Padding(3),
            "get_unanalyzed_log_tmp_reward_data_list_length" / Rebuild(Int8ub, len_(this.get_unanalyzed_log_tmp_reward_data_list)),  # get_unanalyzed_log_tmp_reward_data_list_length is a byte
            "get_unanalyzed_log_tmp_reward_data_list" / Array(this.get_unanalyzed_log_tmp_reward_data_list_length, Struct(
                "unanalyzed_log_grade_id" / Int32ub,  # unanalyzed_log_grade_id is an int,
            )),
            Padding(3),
            "get_event_item_data_list_length" / Rebuild(Int8ub, len_(this.get_event_item_data_list)),  # get_event_item_data_list_length is a byte,
            "get_event_item_data_list" / Array(this.get_event_item_data_list_length, Struct(
                "event_item_id" / Int32ub,  # event_item_id is an int
                "get_num" / Int16ub,  # get_num is a short
            )),
            Padding(3),
            "discovery_enemy_data_list_length" / Rebuild(Int8ub, len_(this.discovery_enemy_data_list)),  # discovery_enemy_data_list_length is a byte
            "discovery_enemy_data_list" / Array(this.discovery_enemy_data_list_length, Struct(
                "enemy_kind_id" / Int32ub,  # enemy_kind_id is an int
                "destroy_num" / Int16ub,  # destroy_num is a short
            )),
            Padding(3),
            "destroy_boss_data_list_length" / Rebuild(Int8ub, len_(this.destroy_boss_data_list)),  # destroy_boss_data_list_length is a byte
            "destroy_boss_data_list" / Array(this.destroy_boss_data_list_length, Struct(
                "boss_type" / Int8ub,  # boss_type is a byte
                "enemy_kind_id" / Int32ub,  # enemy_kind_id is an int
                "destroy_num" / Int16ub,  # destroy_num is a short
            )),
            Padding(3),
            "mission_data_list_length" / Rebuild(Int8ub, len_(this.mission_data_list)),  # mission_data_list_length is a byte
            "mission_data_list" / Array(this.mission_data_list_length, Struct(
                "mission_id" / Int32ub,  # enemy_kind_id is an int
                "clear_flag" / Int8ub,  # boss_type is a byte
                "mission_difficulty_id" / Int16ub,  # destroy_num is a short
            )),
            Padding(3),
            "score_data_length" / Rebuild(Int8ub, len_(this.score_data)),  # score_data_length is a byte
            "score_data" / Array(this.score_data_length, Struct(
                "clear_time" / Int32ub,  # clear_time is an int
                "combo_num" / Int32ub,  # boss_type is a int
                "total_damage_size" / Rebuild(Int32ub, len_(this.total_damage) * 2),  # calculates the length of the total_damage
                "total_damage" / PaddedString(this.total_damage_size, "utf_16_le"),  # total_damage is a (zero) padded string
                "concurrent_destroying_num" / Int16ub, # concurrent_destroying_num is a short
                "reaching_skill_level" / Int16ub, # reaching_skill_level is a short
                "ko_chara_num" / Int8ub,  # ko_chara_num is a byte
                "acceleration_invocation_num" / Int16ub, # acceleration_invocation_num is a short
                "boss_destroying_num" / Int16ub, # boss_destroying_num is a short
                "synchro_skill_used_flag" / Int8ub,  # synchro_skill_used_flag is a byte
                "used_friend_skill_id" / Int32ub,  # used_friend_skill_id is an int
                "friend_skill_used_flag" / Int8ub,  # friend_skill_used_flag is a byte
                "continue_cnt" / Int16ub, # continue_cnt is a short
                "total_loss_num" / Int16ub, # total_loss_num is a short
            )),

        )

        req_data = req_struct.parse(req)

        # Add tower progression to database
        user_id = req_data.user_id
        trial_tower_id = req_data.trial_tower_id
        next_tower_id = 0
        quest_clear_flag = bool(req_data.score_data[0].boss_destroying_num)
        clear_time = req_data.score_data[0].clear_time
        combo_num = req_data.score_data[0].combo_num
        total_damage = req_data.score_data[0].total_damage
        concurrent_destroying_num = req_data.score_data[0].concurrent_destroying_num

        if quest_clear_flag is True:
            # Save tower progression - to be revised to avoid saving worse score
            if trial_tower_id == 9: 
                next_tower_id = 10001
            elif trial_tower_id == 10: 
                trial_tower_id = 10001
                next_tower_id = 3011
            elif trial_tower_id == 19: 
                next_tower_id = 10002
            elif trial_tower_id == 20:
                trial_tower_id = 10002
                next_tower_id = 3021
            elif trial_tower_id == 29: 
                next_tower_id = 10003
            elif trial_tower_id == 30:
                trial_tower_id = 10003
                next_tower_id = 3031
            elif trial_tower_id == 39: 
                next_tower_id = 10004
            elif trial_tower_id == 40:
                trial_tower_id = 10004
                next_tower_id = 3041
            elif trial_tower_id == 49: 
                next_tower_id = 10005
            elif trial_tower_id == 50:
                trial_tower_id = 10005
                next_tower_id = 3051
            else:
                trial_tower_id = trial_tower_id + 3000
                next_tower_id = trial_tower_id + 1

            self.game_data.item.put_player_quest(user_id, trial_tower_id, quest_clear_flag, clear_time, combo_num, total_damage, concurrent_destroying_num)

            # Check if next stage is already done
            checkQuest = self.game_data.item.get_quest_log(user_id, next_tower_id)
            if not checkQuest:
                if next_tower_id != 3101:
                    self.game_data.item.put_player_quest(user_id, next_tower_id, 0, 0, 0, 0, 0)

        # Update the profile 
        profile = self.game_data.profile.get_profile(user_id)
        
        exp = int(profile["rank_exp"]) + 100 #always 100 extra exp for some reason
        col = int(profile["own_col"]) + int(req_data.base_get_data[0].get_col)

        # Calculate level based off experience and the CSV list
        with open(r'titles/sao/data/PlayerRank.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            data = []
            rowf = False
            for row in csv_reader:
                if rowf==False:
                    rowf=True
                else:
                    data.append(row)           
            
        for i in range(0,len(data)):
            if exp>=int(data[i][1]) and exp<int(data[i+1][1]):
                player_level = int(data[i][0])
                break

        updated_profile = self.game_data.profile.put_profile(
            user_id,
            profile["user_type"], 
            profile["nick_name"], 
            player_level,
            exp,
            col,
            profile["own_vp"], 
            profile["own_yui_medal"], 
            profile["setting_title_id"]
            )

        # Update heroes from the used party
        play_session = self.game_data.item.get_session(user_id)
        session_party = self.game_data.item.get_hero_party(user_id, play_session["user_party_team_id"])

        hero_list = []
        hero_list.append(session_party["user_hero_log_id_1"])
        hero_list.append(session_party["user_hero_log_id_2"])
        hero_list.append(session_party["user_hero_log_id_3"])

        for i in range(0,len(hero_list)):
            hero_data = self.game_data.item.get_hero_log(user_id, hero_list[i])

            log_exp = int(hero_data["log_exp"]) + int(req_data.base_get_data[0].get_hero_log_exp)

            # Calculate hero level based off experience and the CSV list
            with open(r'titles/sao/data/HeroLogLevel.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                data = []
                rowf = False
                for row in csv_reader:
                    if rowf==False:
                        rowf=True
                    else:
                        data.append(row)
                
            for e in range(0,len(data)):
                if log_exp>=int(data[e][1]) and log_exp<int(data[e+1][1]):
                    hero_level = int(data[e][0])
                    break

            self.game_data.item.put_hero_log(
                user_id,
                hero_data["user_hero_log_id"],
                hero_level,
                log_exp,
                hero_data["main_weapon"],
                hero_data["sub_equipment"],
                hero_data["skill_slot1_skill_id"],
                hero_data["skill_slot2_skill_id"],
                hero_data["skill_slot3_skill_id"],
                hero_data["skill_slot4_skill_id"],
                hero_data["skill_slot5_skill_id"]
            )
        
        # Grab the rare loot from the table, match it with the right item and then push to the player profile
        for r in range(0,req_data.get_rare_drop_data_list_length):
            rewardList = self.game_data.static.get_rare_drop_id(int(req_data.get_rare_drop_data_list[r].quest_rare_drop_id))
            commonRewardId = rewardList["commonRewardId"]

            heroList = self.game_data.static.get_hero_id(commonRewardId)
            equipmentList = self.game_data.static.get_equipment_id(commonRewardId)
            itemList = self.game_data.static.get_item_id(commonRewardId)

            if heroList:
                self.game_data.item.put_hero_log(user_id, commonRewardId, 1, 0, 101000016, 0, 30086, 1001, 1002, 0, 0)
            if equipmentList:
                self.game_data.item.put_equipment_data(user_id, commonRewardId, 1, 200, 0, 0, 0)
            if itemList:
                self.game_data.item.put_item(user_id, commonRewardId)

        # Generate random hero(es) based off the response    
        for a in range(0,req_data.get_unanalyzed_log_tmp_reward_data_list_length):
            
            with open('titles/sao/data/RewardTable.csv', 'r') as f:
                keys_unanalyzed = next(f).strip().split(',')
                data_unanalyzed = list(DictReader(f, fieldnames=keys_unanalyzed))

            randomized_unanalyzed_id = choice(data_unanalyzed)
            while int(randomized_unanalyzed_id['UnanalyzedLogGradeId']) != req_data.get_unanalyzed_log_tmp_reward_data_list[a].unanalyzed_log_grade_id:
                randomized_unanalyzed_id = choice(data_unanalyzed)
            
            heroList = self.game_data.static.get_hero_id(randomized_unanalyzed_id['CommonRewardId'])
            equipmentList = self.game_data.static.get_equipment_id(randomized_unanalyzed_id['CommonRewardId'])
            itemList = self.game_data.static.get_item_id(randomized_unanalyzed_id['CommonRewardId'])
            if heroList:
                self.game_data.item.put_hero_log(user_id, randomized_unanalyzed_id['CommonRewardId'], 1, 0, 101000016, 0, 30086, 1001, 1002, 0, 0)
            if equipmentList:
                self.game_data.item.put_equipment_data(user_id, randomized_unanalyzed_id['CommonRewardId'], 1, 200, 0, 0, 0)
            if itemList:
                self.game_data.item.put_item(user_id, randomized_unanalyzed_id['CommonRewardId'])
            
        # Send response

        resp = SaoTrialTowerPlayEndResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c90a(self, request: Any) -> bytes: #should be tweaked for proper item unlock
        #quest/episode_play_end_unanalyzed_log_fixed
        resp = SaoEpisodePlayEndUnanalyzedLogFixedResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c91a(self, request: Any) -> bytes: # handler is identical to the episode
        #quest/trial_tower_play_end_unanalyzed_log_fixed
        resp = SaoEpisodePlayEndUnanalyzedLogFixedResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_cd00(self, request: Any) -> bytes:
        #defrag_match/get_defrag_match_basic_data
        resp = SaoGetDefragMatchBasicDataResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_cd02(self, request: Any) -> bytes:
        #defrag_match/get_defrag_match_ranking_user_data
        resp = SaoGetDefragMatchRankingUserDataResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_cd04(self, request: Any) -> bytes:
        #defrag_match/get_defrag_match_league_point_ranking_list
        resp = SaoGetDefragMatchLeaguePointRankingListResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_cd06(self, request: Any) -> bytes:
        #defrag_match/get_defrag_match_league_score_ranking_list
        resp = SaoGetDefragMatchLeagueScoreRankingListResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()
    
    def handle_d404(self, request: Any) -> bytes:
        #other/bnid_serial_code_check
        resp = SaoBnidSerialCodeCheckResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()

    def handle_c306(self, request: Any) -> bytes:
        #card/scan_qr_quest_profile_card
        resp = SaoScanQrQuestProfileCardResponse(int.from_bytes(bytes.fromhex(request[:4]), "big")+1)
        return resp.make()