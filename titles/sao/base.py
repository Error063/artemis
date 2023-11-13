import logging
from csv import *
from random import choice

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

    def handle_noop(self, header: SaoRequestHeader, request: bytes) -> bytes:        
        self.logger.info(f"Using Generic handler")
        resp_thing = SaoNoopResponse(header.cmd + 1)
        return resp_thing.make()

    def handle_c122(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #common/get_maintenance_info
        resp = SaoGetMaintResponse(header.cmd +1)
        return resp.make()

    def handle_c12e(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #common/ac_cabinet_boot_notification
        resp = SaoCommonAcCabinetBootNotificationResponse(header.cmd +1)
        return resp.make()

    def handle_c100(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #common/get_app_versions
        resp = SaoCommonGetAppVersionsRequest(header.cmd +1)
        return resp.make()

    def handle_c102(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #common/master_data_version_check
        resp = SaoMasterDataVersionCheckResponse(header.cmd +1)
        return resp.make()

    def handle_c10a(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #common/paying_play_start
        resp = SaoCommonPayingPlayStartRequest(header.cmd +1)
        return resp.make()

    def handle_ca02(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #quest_multi_play_room/get_quest_scene_multi_play_photon_server
        resp = SaoGetQuestSceneMultiPlayPhotonServerResponse(header.cmd +1)
        return resp.make()

    def handle_c11e(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #common/get_auth_card_data
        req = SaoGetAuthCardDataRequest(header, request)

        #Check authentication
        user_id = self.core_data.card.get_user_id_from_card( req.access_code )

        if not user_id:
            user_id = self.core_data.user.create_user() #works
            card_id = self.core_data.card.create_card(user_id, req.access_code)

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
            

        self.logger.info(f"User Authenticated: { req.access_code } | { user_id }")

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

        resp = SaoGetAuthCardDataResponse(header.cmd +1, profile_data)
        return resp.make()

    def handle_c40c(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #home/check_ac_login_bonus
        resp = SaoHomeCheckAcLoginBonusResponse(header.cmd +1)
        return resp.make()

    def handle_c104(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #common/login
        req = SaoCommonLoginRequest(header, request)

        user_id = self.core_data.card.get_user_id_from_card( req.access_code )
        profile_data = self.game_data.profile.get_profile(user_id)

        resp = SaoCommonLoginResponse(header.cmd +1, profile_data)
        return resp.make()

    def handle_c404(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #home/check_comeback_event
        resp = SaoCheckComebackEventRequest(header.cmd +1)
        return resp.make()

    def handle_c000(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #ticket/ticket
        resp = SaoTicketResponse(header.cmd +1)
        return resp.make()

    def handle_c500(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #user_info/get_user_basic_data
        req = SaoGetUserBasicDataRequest(header, request)

        profile_data = self.game_data.profile.get_profile(req.user_id)

        resp = SaoGetUserBasicDataResponse(header.cmd +1, profile_data)
        return resp.make()
        
    def handle_c600(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #have_object/get_hero_log_user_data_list
        req = SaoGetHeroLogUserDataListRequest(header, request)

        hero_data = self.game_data.item.get_hero_logs(req.user_id)
        
        resp = SaoGetHeroLogUserDataListResponse(header.cmd +1, hero_data)
        return resp.make()
    
    def handle_c602(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #have_object/get_equipment_user_data_list
        req = SaoGetEquipmentUserDataListRequest(header, request)
    
        equipment_data = self.game_data.item.get_user_equipments(req.user_id)

        resp = SaoGetEquipmentUserDataListResponse(header.cmd +1, equipment_data)
        return resp.make()
        
    def handle_c604(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #have_object/get_item_user_data_list
        req = SaoGetItemUserDataListRequest(header, request)

        item_data = self.game_data.item.get_user_items(req.user_id)

        resp = SaoGetItemUserDataListResponse(header.cmd +1, item_data)
        return resp.make()
        
    def handle_c606(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #have_object/get_support_log_user_data_list
        supportIdsData = self.game_data.static.get_support_log_ids(0, True)
        
        resp = SaoGetSupportLogUserDataListResponse(header.cmd +1, supportIdsData)
        return resp.make()
    
    def handle_c800(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #custom/get_title_user_data_list
        titleIdsData = self.game_data.static.get_title_ids(0, True)
        
        resp = SaoGetTitleUserDataListResponse(header.cmd +1, titleIdsData)
        return resp.make()
        
    def handle_c608(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #have_object/get_episode_append_data_list
        req = SaoGetEpisodeAppendDataListRequest(header, request)

        profile_data = self.game_data.profile.get_profile(req.user_id)

        resp = SaoGetEpisodeAppendDataListResponse(header.cmd +1, profile_data)
        return resp.make()

    def handle_c804(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #custom/get_party_data_list
        req = SaoGetPartyDataListRequest(header, request)

        hero_party = self.game_data.item.get_hero_party(req.user_id, 0)
        hero1_data = self.game_data.item.get_hero_log(req.user_id, hero_party[3])
        hero2_data = self.game_data.item.get_hero_log(req.user_id, hero_party[4])
        hero3_data = self.game_data.item.get_hero_log(req.user_id, hero_party[5])

        resp = SaoGetPartyDataListResponse(header.cmd +1, hero1_data, hero2_data, hero3_data)
        return resp.make()

    def handle_c902(self, header: SaoRequestHeader, request: bytes) -> bytes: # for whatever reason, having all entries empty or filled changes nothing
        #quest/get_quest_scene_prev_scan_profile_card
        resp = SaoGetQuestScenePrevScanProfileCardResponse(header.cmd +1)
        return resp.make()

    def handle_c124(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #common/get_resource_path_info
        resp = SaoGetResourcePathInfoResponse(header.cmd +1)
        return resp.make()

    def handle_c900(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #quest/get_quest_scene_user_data_list // QuestScene.csv
        req = SaoGetQuestSceneUserDataListRequest(header, request)

        quest_data = self.game_data.item.get_quest_logs(req.user_id)

        resp = SaoGetQuestSceneUserDataListResponse(header.cmd +1, quest_data)
        return resp.make()

    def handle_c400(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #home/check_yui_medal_get_condition
        resp = SaoCheckYuiMedalGetConditionResponse(header.cmd +1)
        return resp.make()

    def handle_c402(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #home/get_yui_medal_bonus_user_data
        resp = SaoGetYuiMedalBonusUserDataResponse(header.cmd +1)
        return resp.make()

    def handle_c40a(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #home/check_profile_card_used_reward
        resp = SaoCheckProfileCardUsedRewardResponse(header.cmd +1)
        return resp.make()

    def handle_c814(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #custom/synthesize_enhancement_hero_log
        req = SaoSynthesizeEnhancementHeroLogRequest(header, request)

        synthesize_hero_log_data = self.game_data.item.get_hero_log(req.user_id, req.origin_user_hero_log_id)

        for x in req.material_common_reward_user_data_list:
            hero_exp = 0
            itemList = self.game_data.static.get_item_id(x.user_common_reward_id)
            heroList = self.game_data.static.get_hero_id(x.user_common_reward_id)
            equipmentList = self.game_data.static.get_equipment_id(x.user_common_reward_id)

            if itemList:
                hero_exp = 2000 + int(synthesize_hero_log_data["log_exp"])
                self.game_data.item.remove_item(req.user_id, x.user_common_reward_id)

            if equipmentList:
                equipment_data = self.game_data.item.get_user_equipment(req.user_id, x.user_common_reward_id)
                if equipment_data is None:
                    self.logger.error(f"Failed to find equipment {x.user_common_reward_id} for user {req.user_id}!")
                    continue
                
                hero_exp = int(equipment_data["enhancement_exp"]) + int(synthesize_hero_log_data["log_exp"])
                self.game_data.item.remove_equipment(req.user_id, x.user_common_reward_id)

            if heroList:
                hero_data = self.game_data.item.get_hero_log(req.user_id, x.user_common_reward_id)
                if hero_data is None:
                    self.logger.error(f"Failed to find hero {x.user_common_reward_id} for user {req.user_id}!")
                    continue
                
                hero_exp = int(hero_data["log_exp"]) + int(synthesize_hero_log_data["log_exp"])
                self.game_data.item.remove_hero_log(req.user_id, x.user_common_reward_id)
            
            if hero_exp == 0:
                self.logger.warn(f"Hero {x.user_common_reward_id} (type {x.common_reward_type}) not found!")

            self.game_data.item.put_hero_log(
                req.user_id, 
                int(req.origin_user_hero_log_id), 
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

            profile = self.game_data.profile.get_profile(req.user_id)
            new_col = int(profile["own_col"]) - 100

            # Update profile
            
            self.game_data.profile.put_profile(
                req.user_id,
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
        synthesize_hero_log_data = self.game_data.item.get_hero_log(req.user_id, req.origin_user_hero_log_id)

        resp = SaoSynthesizeEnhancementHeroLogResponse(header.cmd +1, synthesize_hero_log_data)
        return resp.make()

    def handle_c816(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #custom/synthesize_enhancement_equipment
        req_data = SaoSynthesizeEnhancementEquipmentRequest(header, request)
        synthesize_equipment_data = self.game_data.item.get_user_equipment(req_data.user_id, req_data.origin_user_equipment_id)

        for x in req_data.material_common_reward_user_data_list:
            equipment_exp = 0
            itemList = self.game_data.static.get_item_id(x.user_common_reward_id)
            heroList = self.game_data.static.get_hero_id(x.user_common_reward_id)
            equipmentList = self.game_data.static.get_equipment_id(x.user_common_reward_id)

            if itemList:
                equipment_exp = 2000 + int(synthesize_equipment_data["enhancement_exp"])
                self.game_data.item.remove_item(req_data.user_id, x.user_common_reward_id)

            if equipmentList:
                equipment_data = self.game_data.item.get_user_equipment(req_data.user_id, x.user_common_reward_id)
                if equipment_data is None:
                    self.logger.error(f"Failed to find equipment {x.user_common_reward_id} for user {req_data.user_id}!")
                    continue

                equipment_exp = int(equipment_data["enhancement_exp"]) + int(synthesize_equipment_data["enhancement_exp"])
                self.game_data.item.remove_equipment(req_data.user_id, x.user_common_reward_id)

            if heroList:
                hero_data = self.game_data.item.get_hero_log(req_data.user_id, x.user_common_reward_id)
                if hero_data is None:
                    self.logger.error(f"Failed to find hero {x.user_common_reward_id} for user {req_data.user_id}!")
                    continue

                equipment_exp = int(hero_data["log_exp"]) + int(synthesize_equipment_data["enhancement_exp"])
                self.game_data.item.remove_hero_log(req_data.user_id, x.user_common_reward_id)

            if equipment_exp == 0:
                self.logger.warn(f"Common reward {x.user_common_reward_id} (type {x.common_reward_type}) not found!")
                continue
            
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

        resp = SaoSynthesizeEnhancementEquipmentResponse(header.cmd +1, synthesize_equipment_data)
        return resp.make()

    def handle_c806(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #custom/change_party
        req_data = SaoChangePartyRequest(header, request)
        party_hero_list = []

        for party_team in req_data.party_data_list[0].party_team_data_list:
            hero_data = self.game_data.item.get_hero_log(req_data.user_id, party_team.user_hero_log_id)
            hero_level = 1
            hero_exp = 0

            if hero_data:
                hero_level = hero_data["log_level"]
                hero_exp = hero_data["log_exp"]

            self.game_data.item.put_hero_log(
                req_data.user_id,
                party_team.user_hero_log_id,
                hero_level,
                hero_exp,
                party_team.main_weapon_user_equipment_id,
                party_team.sub_equipment_user_equipment_id,
                party_team.skill_slot1_skill_id,
                party_team.skill_slot2_skill_id,
                party_team.skill_slot3_skill_id,
                party_team.skill_slot4_skill_id,
                party_team.skill_slot5_skill_id
            )

            party_hero_list.append(party_team.user_hero_log_id)

        self.game_data.item.put_hero_party(req_data.user_id, req_data.party_data_list[0].party_team_data_list[0].user_party_team_id, party_hero_list[0], party_hero_list[1], party_hero_list[2])

        resp = SaoNoopResponse(header.cmd +1)
        return resp.make()

    def handle_c904(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #quest/episode_play_start
        req_data = SaoEpisodePlayStartRequest(header, request)

        user_id = req_data.user_id
        profile_data = self.game_data.profile.get_profile(user_id)

        self.game_data.item.create_session(
            user_id, 
            int(req_data.play_start_request_data[0].user_party_id), 
            req_data.episode_id, 
            req_data.play_mode, 
            req_data.play_start_request_data[0].quest_drop_boost_apply_flag
            )

        resp = SaoEpisodePlayStartResponse(header.cmd +1, profile_data)
        return resp.make()

    def handle_c908(self, header: SaoRequestHeader, request: bytes) -> bytes: # Level calculation missing for the profile and heroes
        #quest/episode_play_end

        req_data = SaoEpisodePlayEndRequest(header, request)

        # Add stage progression to database
        user_id = req_data.user_id
        episode_id = req_data.episode_id
        quest_clear_flag = bool(req_data.play_end_request_data_list[0].score_data_list[0].boss_destroying_num)
        clear_time = req_data.play_end_request_data_list[0].score_data_list[0].clear_time
        combo_num = req_data.play_end_request_data_list[0].score_data_list[0].combo_num
        total_damage = req_data.play_end_request_data_list[0].score_data_list[0].total_damage
        concurrent_destroying_num = req_data.play_end_request_data_list[0].score_data_list[0].concurrent_destroying_num

        profile = self.game_data.profile.get_profile(user_id)
        vp = int(profile["own_vp"])
        exp = int(profile["rank_exp"]) + 100 #always 100 extra exp for some reason
        col = int(profile["own_col"]) + int(req_data.play_end_request_data_list[0].base_get_data_list[0].get_col)

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

            log_exp = int(hero_data["log_exp"]) + int(req_data.play_end_request_data_list[0].base_get_data_list[0].get_hero_log_exp)

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
        json_data = {"data": []}

        for r in range(0,req_data.play_end_request_data_list[0].get_rare_drop_data_count):
            rewardList = self.game_data.static.get_rare_drop_id(int(req_data.play_end_request_data_list[0].get_rare_drop_data_list[r].quest_rare_drop_id))
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
        for a in range(0,req_data.play_end_request_data_list[0].get_unanalyzed_log_tmp_reward_data_count):
            with open('titles/sao/data/RewardTable.csv', 'r') as f:
                keys_unanalyzed = next(f).strip().split(',')
                data_unanalyzed = list(DictReader(f, fieldnames=keys_unanalyzed))

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

            json_data["data"].append(randomized_unanalyzed_id['CommonRewardId'])
            
        # Send response

        self.game_data.item.create_end_session(user_id, episode_id, quest_clear_flag, json_data["data"])

        resp = SaoEpisodePlayEndResponse(header.cmd +1)
        return resp.make()

    def handle_c914(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #quest/trial_tower_play_start
        req_data = SaoTrialTowerPlayStartRequest(header, request)

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

        resp = SaoEpisodePlayStartResponse(header.cmd +1, profile_data)
        return resp.make()

    def handle_c918(self, header: SaoRequestHeader, request: bytes) -> bytes:
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

        json_data = {"data": []}
        
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

            json_data["data"].append(randomized_unanalyzed_id['CommonRewardId'])
            
        # Send response

        self.game_data.item.create_end_session(user_id, trial_tower_id, quest_clear_flag, json_data["data"])

        resp = SaoTrialTowerPlayEndResponse(header.cmd +1)
        return resp.make()

    def handle_c90a(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #quest/episode_play_end_unanalyzed_log_fixed

        req = SaoEpisodePlayEndUnanalyzedLogFixedRequest(header, request)

        end_session_data = self.game_data.item.get_end_session(req.user_id)

        resp = SaoEpisodePlayEndUnanalyzedLogFixedResponse(header.cmd +1, end_session_data[4])
        return resp.make()

    def handle_c91a(self, header: SaoRequestHeader, request: bytes) -> bytes: # handler is identical to the episode
        #quest/trial_tower_play_end_unanalyzed_log_fixed
        req = TrialTowerPlayEndUnanalyzedLogFixed(header, request)

        end_session_data = self.game_data.item.get_end_session(req.user_id)

        resp = SaoEpisodePlayEndUnanalyzedLogFixedResponse(header.cmd +1, end_session_data[4])
        return resp.make()

    def handle_cd00(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #defrag_match/get_defrag_match_basic_data
        resp = SaoGetDefragMatchBasicDataResponse(header.cmd +1)
        return resp.make()

    def handle_cd02(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #defrag_match/get_defrag_match_ranking_user_data
        resp = SaoGetDefragMatchRankingUserDataResponse(header.cmd +1)
        return resp.make()

    def handle_cd04(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #defrag_match/get_defrag_match_league_point_ranking_list
        resp = SaoGetDefragMatchLeaguePointRankingListResponse(header.cmd +1)
        return resp.make()

    def handle_cd06(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #defrag_match/get_defrag_match_league_score_ranking_list
        resp = SaoGetDefragMatchLeagueScoreRankingListResponse(header.cmd +1)
        return resp.make()

    def handle_d404(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #other/bnid_serial_code_check
        resp = SaoBnidSerialCodeCheckResponse(header.cmd +1)
        return resp.make()

    def handle_c306(self, header: SaoRequestHeader, request: bytes) -> bytes:
        #card/scan_qr_quest_profile_card
        resp = SaoScanQrQuestProfileCardResponse(header.cmd +1)
        return resp.make()