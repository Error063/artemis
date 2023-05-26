import struct
from datetime import datetime
from construct import *
import sys

class SaoBaseRequest:
    def __init__(self, data: bytes) -> None:
        self.cmd = struct.unpack_from("!H", bytes)[0]
        # TODO: The rest of the request header

class SaoBaseResponse:
    def __init__(self, cmd_id: int) -> None:
        self.cmd = cmd_id
        self.err_status = 0
        self.error_type = 0
        self.vendor_id = 5
        self.game_id = 1
        self.version_id = 1
        self.length = 1
    
    def make(self) -> bytes:
        return struct.pack("!HHIIIII", self.cmd, self.err_status, self.error_type, self.vendor_id, self.game_id, self.version_id, self.length)

class SaoNoopResponse(SaoBaseResponse):
    def __init__(self, cmd: int) -> None:
        super().__init__(cmd)      
        self.result = 1
        self.length = 5

    def make(self) -> bytes:
        return super().make() + struct.pack("!bI", self.result, 0)
        
class SaoGetMaintRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)
        # TODO: The rest of the mait info request

class SaoGetMaintResponse(SaoBaseResponse):
    def __init__(self, cmd) -> None:
        super().__init__(cmd)
        self.result = 1
        self.maint_begin = datetime.fromtimestamp(0)
        self.maint_begin_int_ct = 6
        self.maint_end = datetime.fromtimestamp(0)
        self.maint_end_int_ct = 6
        self.dt_format = "%Y%m%d%H%M%S"
    
    def make(self) -> bytes:
        maint_begin_list = [x for x in datetime.strftime(self.maint_begin, self.dt_format)]
        maint_end_list = [x for x in datetime.strftime(self.maint_end, self.dt_format)]
        self.maint_begin_int_ct = len(maint_begin_list) * 2
        self.maint_end_int_ct = len(maint_end_list) * 2

        maint_begin_bytes = b""
        maint_end_bytes = b""
        
        for x in maint_begin_list:
            maint_begin_bytes += struct.pack("<H", ord(x))

        for x in maint_end_list:
            maint_end_bytes += struct.pack("<H", ord(x))
        
        resp_data = struct.pack("!bI", self.result, self.maint_begin_int_ct) + maint_begin_bytes + struct.pack("!I", self.maint_end_int_ct) + maint_end_bytes
        
        self.length = len(resp_data)
        return super().make() + resp_data

class SaoCommonAcCabinetBootNotificationRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoCommonAcCabinetBootNotificationResponse(SaoBaseResponse):
    def __init__(self, cmd) -> None:
        super().__init__(cmd)
        self.result = 1
    
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
        )

        resp_data = resp_struct.build(dict(
            result=self.result,
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoMasterDataVersionCheckRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoMasterDataVersionCheckResponse(SaoBaseResponse):
    def __init__(self, cmd) -> None:
        super().__init__(cmd)
        self.result = 1
        self.update_flag = 0
        self.data_version = 100
    
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "update_flag" / Int8ul,  # result is either 0 or 1
            "data_version" / Int32ub,
        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            update_flag=self.update_flag,
            data_version=self.data_version,
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoCommonGetAppVersionsRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoCommonGetAppVersionsRequest(SaoBaseResponse):
    def __init__(self, cmd) -> None:
        super().__init__(cmd)
        self.result = 1
        self.data_list_size = 1 # Number of arrays

        self.version_app_id = 1
        self.applying_start_date = "20230520193000"
    
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "data_list_size" / Int32ub,

            "version_app_id" / Int32ub,
            "applying_start_date_size" / Int32ub, # big endian
            "applying_start_date" / Int16ul[len(self.applying_start_date)],
        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            data_list_size=self.data_list_size,

            version_app_id=self.version_app_id,
            applying_start_date_size=len(self.applying_start_date) * 2,
            applying_start_date=[ord(x) for x in self.applying_start_date],
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoCommonPayingPlayStartRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoCommonPayingPlayStartRequest(SaoBaseResponse):
    def __init__(self, cmd) -> None:
        super().__init__(cmd)
        self.result = 1
        self.paying_session_id = "1"
    
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "paying_session_id_size" / Int32ub, # big endian
            "paying_session_id" / Int16ul[len(self.paying_session_id)],
        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            paying_session_id_size=len(self.paying_session_id) * 2,
            paying_session_id=[ord(x) for x in self.paying_session_id],
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoGetAuthCardDataRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoGetAuthCardDataResponse(SaoBaseResponse): #GssSite.dll / GssSiteSystem / GameConnectProt / public class get_auth_card_data_R : GameConnect.GssProtocolBase
    def __init__(self, cmd, profile_data) -> None:
        super().__init__(cmd)

        self.result = 1
        self.unused_card_flag = ""
        self.first_play_flag = 0
        self.tutorial_complete_flag = 1
        self.nick_name = profile_data['nick_name'] # nick_name field #4
        self.personal_id = str(profile_data['user'])
    
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "unused_card_flag_size" / Int32ub,  # big endian
            "unused_card_flag" / Int16ul[len(self.unused_card_flag)],
            "first_play_flag" / Int8ul,  # result is either 0 or 1
            "tutorial_complete_flag" / Int8ul,  # result is either 0 or 1
            "nick_name_size" / Int32ub,  # big endian
            "nick_name" / Int16ul[len(self.nick_name)],
            "personal_id_size" / Int32ub,  # big endian
            "personal_id" / Int16ul[len(self.personal_id)]
        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            unused_card_flag_size=len(self.unused_card_flag) * 2,
            unused_card_flag=[ord(x) for x in self.unused_card_flag],
            first_play_flag=self.first_play_flag,
            tutorial_complete_flag=self.tutorial_complete_flag,
            nick_name_size=len(self.nick_name) * 2,
            nick_name=[ord(x) for x in self.nick_name],
            personal_id_size=len(self.personal_id) * 2,
            personal_id=[ord(x) for x in self.personal_id]
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoHomeCheckAcLoginBonusRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoHomeCheckAcLoginBonusResponse(SaoBaseResponse):
    def __init__(self, cmd) -> None:
        super().__init__(cmd)
        self.result = 1
        self.reward_get_flag = 1
        self.get_ac_login_bonus_id_list_size = 2 # Array

        self.get_ac_login_bonus_id_1 = 1 # "2020年7月9日～（アニメ＆リコリス記念）"
        self.get_ac_login_bonus_id_2 = 2 # "2020年10月6日～（秋のデビュー＆カムバックCP）"
    
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "reward_get_flag" / Int8ul,  # result is either 0 or 1
            "get_ac_login_bonus_id_list_size" / Int32ub,

            "get_ac_login_bonus_id_1" / Int32ub,
            "get_ac_login_bonus_id_2" / Int32ub,
        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            reward_get_flag=self.reward_get_flag,
            get_ac_login_bonus_id_list_size=self.get_ac_login_bonus_id_list_size,

            get_ac_login_bonus_id_1=self.get_ac_login_bonus_id_1,
            get_ac_login_bonus_id_2=self.get_ac_login_bonus_id_2,
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoGetQuestSceneMultiPlayPhotonServerRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoGetQuestSceneMultiPlayPhotonServerResponse(SaoBaseResponse):
    def __init__(self, cmd) -> None:
        super().__init__(cmd)
        self.result = 1
        self.application_id = "7df3a2f6-d69d-4073-aafe-810ee61e1cea"
    
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "application_id_size" / Int32ub,  # big endian
            "application_id" / Int16ul[len(self.application_id)],
        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            application_id_size=len(self.application_id) * 2,
            application_id=[ord(x) for x in self.application_id],
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoTicketRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoTicketResponse(SaoBaseResponse):
    def __init__(self, cmd) -> None:
        super().__init__(cmd)
        self.result = "1"
        self.ticket_id = "9" #up to 18
    
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result_size" / Int32ub,  # big endian
            "result" / Int16ul[len(self.result)],
            "ticket_id_size" / Int32ub,  # big endian
            "ticket_id" / Int16ul[len(self.result)],
        )

        resp_data = resp_struct.build(dict(
            result_size=len(self.result) * 2,
            result=[ord(x) for x in self.result],
            ticket_id_size=len(self.ticket_id) * 2,
            ticket_id=[ord(x) for x in self.ticket_id],
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoCommonLoginRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoCommonLoginResponse(SaoBaseResponse):
    def __init__(self, cmd, profile_data) -> None:
        super().__init__(cmd)
        self.result = 1
        self.user_id = str(profile_data['user'])
        self.first_play_flag = 0
        self.grantable_free_ticket_flag = 1
        self.login_reward_vp = 99
        self.today_paying_flag = 1
    
    def make(self) -> bytes:
        # create a resp struct
        '''
        bool = Int8ul
        short = Int16ub
        int = Int32ub
        '''
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "user_id_size" / Int32ub, # big endian
            "user_id" / Int16ul[len(self.user_id)],
            "first_play_flag" / Int8ul,  # result is either 0 or 1
            "grantable_free_ticket_flag" / Int8ul,  # result is either 0 or 1
            "login_reward_vp" / Int16ub,
            "today_paying_flag" / Int8ul,  # result is either 0 or 1
        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            user_id_size=len(self.user_id) * 2,
            user_id=[ord(x) for x in self.user_id],
            first_play_flag=self.first_play_flag,
            grantable_free_ticket_flag=self.grantable_free_ticket_flag,
            login_reward_vp=self.login_reward_vp,
            today_paying_flag=self.today_paying_flag,
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoCheckComebackEventRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoCheckComebackEventRequest(SaoBaseResponse):
    def __init__(self, cmd) -> None:
        super().__init__(cmd)
        self.result = 1
        self.get_flag_ = 1
        self.get_comeback_event_id_list = "" # Array of events apparently
    
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "get_flag_" / Int8ul,  # result is either 0 or 1
            "get_comeback_event_id_list_size" / Int32ub, # big endian
            "get_comeback_event_id_list" / Int16ul[len(self.get_comeback_event_id_list)],
        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            get_flag_=self.get_flag_,
            get_comeback_event_id_list_size=len(self.get_comeback_event_id_list) * 2,
            get_comeback_event_id_list=[ord(x) for x in self.get_comeback_event_id_list],
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoGetUserBasicDataRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoGetUserBasicDataResponse(SaoBaseResponse):
    def __init__(self, cmd, profile_data) -> None:
        super().__init__(cmd)
        self.result = 1
        self.user_basic_data_size = 1 # Number of arrays
        self.user_type = profile_data['user_type']
        self.nick_name = profile_data['nick_name']
        self.rank_num = profile_data['rank_num']
        self.rank_exp = profile_data['rank_exp']
        self.own_col = profile_data['own_col']
        self.own_vp = profile_data['own_vp']
        self.own_yui_medal = profile_data['own_yui_medal']
        self.setting_title_id = profile_data['setting_title_id']
        self.favorite_user_hero_log_id = ""
        self.favorite_user_support_log_id = ""
        self.my_store_id = "1"
        self.my_store_name = "ARTEMiS"
        self.user_reg_date = "20230101120000"
    
    def make(self) -> bytes:
        # create a resp struct
        '''
        bool = Int8ul
        short = Int16ub
        int = Int32ub
        '''
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "user_basic_data_size" / Int32ub,

            "user_type" / Int16ub,
            "nick_name_size" / Int32ub,  # big endian
            "nick_name" / Int16ul[len(self.nick_name)],
            "rank_num" / Int16ub,
            "rank_exp" / Int32ub,
            "own_col" / Int32ub,
            "own_vp" / Int32ub,
            "own_yui_medal" / Int32ub,
            "setting_title_id" / Int32ub,
            "favorite_user_hero_log_id_size" / Int32ub,  # big endian
            "favorite_user_hero_log_id" / Int16ul[len(str(self.favorite_user_hero_log_id))],
            "favorite_user_support_log_id_size" / Int32ub,  # big endian
            "favorite_user_support_log_id" / Int16ul[len(str(self.favorite_user_support_log_id))],
            "my_store_id_size" / Int32ub,  # big endian
            "my_store_id" / Int16ul[len(str(self.my_store_id))],
            "my_store_name_size" / Int32ub,  # big endian
            "my_store_name" / Int16ul[len(str(self.my_store_name))],         
            "user_reg_date_size" / Int32ub,  # big endian
            "user_reg_date" / Int16ul[len(self.user_reg_date)]

        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            user_basic_data_size=self.user_basic_data_size,

            user_type=self.user_type,
            nick_name_size=len(self.nick_name) * 2,
            nick_name=[ord(x) for x in self.nick_name],
            rank_num=self.rank_num,
            rank_exp=self.rank_exp,
            own_col=self.own_col,
            own_vp=self.own_vp,
            own_yui_medal=self.own_yui_medal,
            setting_title_id=self.setting_title_id,
            favorite_user_hero_log_id_size=len(self.favorite_user_hero_log_id) * 2,
            favorite_user_hero_log_id=[ord(x) for x in str(self.favorite_user_hero_log_id)],
            favorite_user_support_log_id_size=len(self.favorite_user_support_log_id) * 2,
            favorite_user_support_log_id=[ord(x) for x in str(self.favorite_user_support_log_id)],
            my_store_id_size=len(self.my_store_id) * 2,
            my_store_id=[ord(x) for x in str(self.my_store_id)],
            my_store_name_size=len(self.my_store_name) * 2,
            my_store_name=[ord(x) for x in str(self.my_store_name)],
            user_reg_date_size=len(self.user_reg_date) * 2,
            user_reg_date=[ord(x) for x in self.user_reg_date],
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoGetHeroLogUserDataListRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoGetHeroLogUserDataListResponse(SaoBaseResponse):
    def __init__(self, cmd, heroIdsData) -> None:
        super().__init__(cmd)
        self.result = 1
        
        #print(heroIdsData)
        #print(list(map(str,heroIdsData)))

        # hero_log_user_data_list
        self.user_hero_log_id = list(map(str,heroIdsData)) #str
        self.hero_log_id = heroIdsData #int
        self.log_level = 10 #short
        self.max_log_level_extended_num = 10 #short
        self.log_exp = 1000 #int
        self.possible_awakening_flag = 0 #byte
        self.awakening_stage = 0 #short
        self.awakening_exp = 0 #int
        self.skill_slot_correction_value = 0 #byte
        self.last_set_skill_slot1_skill_id = 0 #short
        self.last_set_skill_slot2_skill_id = 0 #short
        self.last_set_skill_slot3_skill_id = 0 #short
        self.last_set_skill_slot4_skill_id = 0 #short
        self.last_set_skill_slot5_skill_id = 0 #short
        self.property1_property_id = 0 #int
        self.property1_value1 = 0 #int
        self.property1_value2 = 0 #int
        self.property2_property_id = 0 #int
        self.property2_value1 = 0 #int
        self.property2_value2 = 0 #int
        self.property3_property_id = 0 #int
        self.property3_value1 = 0 #int
        self.property3_value2 = 0 #int
        self.property4_property_id = 0 #int
        self.property4_value1 = 0 #int
        self.property4_value2 = 0 #int
        self.converted_card_num = 0 #short
        self.shop_purchase_flag = 1 #byte
        self.protect_flag = 0 #byte
        self.get_date = "20230101120000" #str
    
    def make(self) -> bytes:
        #new stuff

        hero_log_user_data_list_struct = Struct(
            "user_hero_log_id_size" / Int32ub,  # big endian
            "user_hero_log_id" / Int16ul[9], #string
            "hero_log_id" / Int32ub, #int
            "log_level" / Int16ub, #short
            "max_log_level_extended_num" / Int16ub, #short
            "log_exp" / Int32ub, #int
            "possible_awakening_flag" / Int8ul,  # result is either 0 or 1
            "awakening_stage" / Int16ub, #short
            "awakening_exp" / Int32ub, #int
            "skill_slot_correction_value" / Int8ul,  # result is either 0 or 1
            "last_set_skill_slot1_skill_id" / Int16ub, #short
            "last_set_skill_slot2_skill_id" / Int16ub, #short
            "last_set_skill_slot3_skill_id" / Int16ub, #short
            "last_set_skill_slot4_skill_id" / Int16ub, #short
            "last_set_skill_slot5_skill_id" / Int16ub, #short
            "property1_property_id" / Int32ub,
            "property1_value1" / Int32ub,
            "property1_value2" / Int32ub,
            "property2_property_id" / Int32ub,
            "property2_value1" / Int32ub,
            "property2_value2" / Int32ub,
            "property3_property_id" / Int32ub,
            "property3_value1" / Int32ub,
            "property3_value2" / Int32ub,
            "property4_property_id" / Int32ub,
            "property4_value1" / Int32ub,
            "property4_value2" / Int32ub,
            "converted_card_num" / Int16ub,
            "shop_purchase_flag" / Int8ul,  # result is either 0 or 1
            "protect_flag" / Int8ul,  # result is either 0 or 1
            "get_date_size" / Int32ub,  # big endian
            "get_date" / Int16ul[len(self.get_date)],
        )

        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "hero_log_user_data_list_size" / Rebuild(Int32ub, len_(this.hero_log_user_data_list)),  # big endian
            "hero_log_user_data_list" / Array(this.hero_log_user_data_list_size, hero_log_user_data_list_struct),
        )

        resp_data = resp_struct.parse(resp_struct.build(dict(
            result=self.result,
            hero_log_user_data_list_size=0,
            hero_log_user_data_list=[],
        )))

        for i in range(len(self.hero_log_id)):
            hero_data = dict(
                user_hero_log_id_size=len(self.user_hero_log_id[i]) * 2,
                user_hero_log_id=[ord(x) for x in self.user_hero_log_id[i]],
                hero_log_id=self.hero_log_id[i],
                log_level=self.log_level,
                max_log_level_extended_num=self.max_log_level_extended_num,
                log_exp=self.log_exp,
                possible_awakening_flag=self.possible_awakening_flag,
                awakening_stage=self.awakening_stage,
                awakening_exp=self.awakening_exp,
                skill_slot_correction_value=self.skill_slot_correction_value,
                last_set_skill_slot1_skill_id=self.last_set_skill_slot1_skill_id,
                last_set_skill_slot2_skill_id=self.last_set_skill_slot2_skill_id,
                last_set_skill_slot3_skill_id=self.last_set_skill_slot3_skill_id,
                last_set_skill_slot4_skill_id=self.last_set_skill_slot4_skill_id,
                last_set_skill_slot5_skill_id=self.last_set_skill_slot5_skill_id,
                property1_property_id=self.property1_property_id,
                property1_value1=self.property1_value1,
                property1_value2=self.property1_value2,
                property2_property_id=self.property2_property_id,
                property2_value1=self.property2_value1,
                property2_value2=self.property2_value2,
                property3_property_id=self.property3_property_id,
                property3_value1=self.property3_value1,
                property3_value2=self.property3_value2,
                property4_property_id=self.property4_property_id,
                property4_value1=self.property4_value1,
                property4_value2=self.property4_value2,
                converted_card_num=self.converted_card_num,
                shop_purchase_flag=self.shop_purchase_flag,
                protect_flag=self.protect_flag,
                get_date_size=len(self.get_date) * 2,
                get_date=[ord(x) for x in self.get_date],

            )
            
            resp_data.hero_log_user_data_list.append(hero_data)

        # finally, rebuild the resp_data
        resp_data = resp_struct.build(resp_data)

        self.length = len(resp_data)
        return super().make() + resp_data
    
class SaoGetEquipmentUserDataListRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoGetEquipmentUserDataListResponse(SaoBaseResponse):
    def __init__(self, cmd, equipmentIdsData) -> None:
        super().__init__(cmd)
        self.result = 1

        # equipment_user_data_list
        self.user_equipment_id = list(map(str,equipmentIdsData)) #str
        self.equipment_id = equipmentIdsData #int
        self.enhancement_value = 10 #short
        self.max_enhancement_value_extended_num = 10 #short
        self.enhancement_exp = 1000 #int
        self.possible_awakening_flag = 0 #byte
        self.awakening_stage = 0 #short
        self.awakening_exp = 0 #int
        self.property1_property_id = 0 #int
        self.property1_value1 = 0 #int
        self.property1_value2 = 0 #int
        self.property2_property_id = 0 #int
        self.property2_value1 = 0 #int
        self.property2_value2 = 0 #int
        self.property3_property_id = 0 #int
        self.property3_value1 = 0 #int
        self.property3_value2 = 0 #int
        self.property4_property_id = 0 #int
        self.property4_value1 = 0 #int
        self.property4_value2 = 0 #int
        self.converted_card_num = 1 #short
        self.shop_purchase_flag = 1 #byte
        self.protect_flag = 0 #byte
        self.get_date = "20230101120000" #str
    
    def make(self) -> bytes:

        equipment_user_data_list_struct = Struct(
            "user_equipment_id_size" / Int32ub,  # big endian
            "user_equipment_id" / Int16ul[9], #string
            "equipment_id" / Int32ub, #int
            "enhancement_value" / Int16ub, #short
            "max_enhancement_value_extended_num" / Int16ub, #short
            "enhancement_exp" / Int32ub, #int
            "possible_awakening_flag" / Int8ul,  # result is either 0 or 1
            "awakening_stage" / Int16ub, #short
            "awakening_exp" / Int32ub, #int
            "property1_property_id" / Int32ub,
            "property1_value1" / Int32ub,
            "property1_value2" / Int32ub,
            "property2_property_id" / Int32ub,
            "property2_value1" / Int32ub,
            "property2_value2" / Int32ub,
            "property3_property_id" / Int32ub,
            "property3_value1" / Int32ub,
            "property3_value2" / Int32ub,
            "property4_property_id" / Int32ub,
            "property4_value1" / Int32ub,
            "property4_value2" / Int32ub,
            "converted_card_num" / Int16ub,
            "shop_purchase_flag" / Int8ul,  # result is either 0 or 1
            "protect_flag" / Int8ul,  # result is either 0 or 1
            "get_date_size" / Int32ub,  # big endian
            "get_date" / Int16ul[len(self.get_date)],
        )

        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "equipment_user_data_list_size" / Rebuild(Int32ub, len_(this.equipment_user_data_list)),  # big endian
            "equipment_user_data_list" / Array(this.equipment_user_data_list_size, equipment_user_data_list_struct),
        )

        resp_data = resp_struct.parse(resp_struct.build(dict(
            result=self.result,
            equipment_user_data_list_size=0,
            equipment_user_data_list=[],
        )))

        for i in range(len(self.equipment_id)):
            equipment_data = dict(
                user_equipment_id_size=len(self.user_equipment_id[i]) * 2,
                user_equipment_id=[ord(x) for x in self.user_equipment_id[i]],
                equipment_id=self.equipment_id[i],
                enhancement_value=self.enhancement_value,
                max_enhancement_value_extended_num=self.max_enhancement_value_extended_num,
                enhancement_exp=self.enhancement_exp,
                possible_awakening_flag=self.possible_awakening_flag,
                awakening_stage=self.awakening_stage,
                awakening_exp=self.awakening_exp,
                property1_property_id=self.property1_property_id,
                property1_value1=self.property1_value1,
                property1_value2=self.property1_value2,
                property2_property_id=self.property2_property_id,
                property2_value1=self.property2_value1,
                property2_value2=self.property2_value2,
                property3_property_id=self.property3_property_id,
                property3_value1=self.property3_value1,
                property3_value2=self.property3_value2,
                property4_property_id=self.property4_property_id,
                property4_value1=self.property4_value1,
                property4_value2=self.property4_value2,
                converted_card_num=self.converted_card_num,
                shop_purchase_flag=self.shop_purchase_flag,
                protect_flag=self.protect_flag,
                get_date_size=len(self.get_date) * 2,
                get_date=[ord(x) for x in self.get_date],

            )
            
            resp_data.equipment_user_data_list.append(equipment_data)

        # finally, rebuild the resp_data
        resp_data = resp_struct.build(resp_data)

        self.length = len(resp_data)
        return super().make() + resp_data
    
class SaoGetItemUserDataListRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoGetItemUserDataListResponse(SaoBaseResponse):
    def __init__(self, cmd, itemIdsData) -> None:
        super().__init__(cmd)
        self.result = 1

        # item_user_data_list
        self.user_item_id = list(map(str,itemIdsData)) #str
        self.item_id = itemIdsData #int
        self.protect_flag = 0 #byte
        self.get_date = "20230101120000" #str
    
    def make(self) -> bytes:
        #new stuff

        item_user_data_list_struct = Struct(
            "user_item_id_size" / Int32ub,  # big endian
            "user_item_id" / Int16ul[6], #string but this will not work with 10000 IDs... only with 6 digits
            "item_id" / Int32ub, #int
            "protect_flag" / Int8ul,  # result is either 0 or 1
            "get_date_size" / Int32ub,  # big endian
            "get_date" / Int16ul[len(self.get_date)],
        )

        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "item_user_data_list_size" / Rebuild(Int32ub, len_(this.item_user_data_list)),  # big endian
            "item_user_data_list" / Array(this.item_user_data_list_size, item_user_data_list_struct),
        )

        resp_data = resp_struct.parse(resp_struct.build(dict(
            result=self.result,
            item_user_data_list_size=0,
            item_user_data_list=[],
        )))

        for i in range(len(self.item_id)):
            item_data = dict(
                user_item_id_size=len(self.user_item_id[i]) * 2,
                user_item_id=[ord(x) for x in self.user_item_id[i]],
                item_id=self.item_id[i],
                protect_flag=self.protect_flag,
                get_date_size=len(self.get_date) * 2,
                get_date=[ord(x) for x in self.get_date],

            )
            
            resp_data.item_user_data_list.append(item_data)

        # finally, rebuild the resp_data
        resp_data = resp_struct.build(resp_data)

        self.length = len(resp_data)
        return super().make() + resp_data
    
class SaoGetSupportLogUserDataListRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoGetSupportLogUserDataListResponse(SaoBaseResponse):
    def __init__(self, cmd, supportIdsData) -> None:
        super().__init__(cmd)
        self.result = 1

        # support_log_user_data_list
        self.user_support_log_id = list(map(str,supportIdsData)) #str
        self.support_log_id = supportIdsData #int
        self.possible_awakening_flag = 0
        self.awakening_stage = 0
        self.awakening_exp = 0
        self.converted_card_num = 0
        self.shop_purchase_flag = 0
        self.protect_flag = 0 #byte
        self.get_date = "20230101120000" #str
    
    def make(self) -> bytes:
        support_log_user_data_list_struct = Struct(
            "user_support_log_id_size" / Int32ub,  # big endian
            "user_support_log_id" / Int16ul[9],
            "support_log_id" / Int32ub, #int
            "possible_awakening_flag" / Int8ul,  # result is either 0 or 1
            "awakening_stage" / Int16ub, #short
            "awakening_exp" / Int32ub, # int
            "converted_card_num" / Int16ub, #short
            "shop_purchase_flag" / Int8ul,  # result is either 0 or 1
            "protect_flag" / Int8ul,  # result is either 0 or 1
            "get_date_size" / Int32ub,  # big endian
            "get_date" / Int16ul[len(self.get_date)],
        )

        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "support_log_user_data_list_size" / Rebuild(Int32ub, len_(this.support_log_user_data_list)),  # big endian
            "support_log_user_data_list" / Array(this.support_log_user_data_list_size, support_log_user_data_list_struct),
        )

        resp_data = resp_struct.parse(resp_struct.build(dict(
            result=self.result,
            support_log_user_data_list_size=0,
            support_log_user_data_list=[],
        )))

        for i in range(len(self.support_log_id)):
            support_data = dict(
                user_support_log_id_size=len(self.user_support_log_id[i]) * 2,
                user_support_log_id=[ord(x) for x in self.user_support_log_id[i]],
                support_log_id=self.support_log_id[i],
                possible_awakening_flag=self.possible_awakening_flag,
                awakening_stage=self.awakening_stage,
                awakening_exp=self.awakening_exp,
                converted_card_num=self.converted_card_num,
                shop_purchase_flag=self.shop_purchase_flag,
                protect_flag=self.protect_flag,
                get_date_size=len(self.get_date) * 2,
                get_date=[ord(x) for x in self.get_date],

            )
            
            resp_data.support_log_user_data_list.append(support_data)

        resp_data = resp_struct.build(resp_data)

        self.length = len(resp_data)
        return super().make() + resp_data
    
class SaoGetTitleUserDataListRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoGetTitleUserDataListResponse(SaoBaseResponse):
    def __init__(self, cmd, titleIdsData) -> None:
        super().__init__(cmd)
        self.result = 1

        # title_user_data_list
        self.user_title_id = list(map(str,titleIdsData)) #str
        self.title_id = titleIdsData #int
    
    def make(self) -> bytes:
        title_user_data_list_struct = Struct(
            "user_title_id_size" / Int32ub,  # big endian
            "user_title_id" / Int16ul[6], #string
            "title_id" / Int32ub, #int
        )

        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "title_user_data_list_size" / Rebuild(Int32ub, len_(this.title_user_data_list)),  # big endian
            "title_user_data_list" / Array(this.title_user_data_list_size, title_user_data_list_struct),
        )

        resp_data = resp_struct.parse(resp_struct.build(dict(
            result=self.result,
            title_user_data_list_size=0,
            title_user_data_list=[],
        )))

        for i in range(len(self.title_id)):
            title_data = dict(
                user_title_id_size=len(self.user_title_id[i]) * 2,
                user_title_id=[ord(x) for x in self.user_title_id[i]],
                title_id=self.title_id[i],
            )
            
            resp_data.title_user_data_list.append(title_data)

        # finally, rebuild the resp_data
        resp_data = resp_struct.build(resp_data)

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoGetEpisodeAppendDataListRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoGetEpisodeAppendDataListResponse(SaoBaseResponse):
    def __init__(self, cmd, profile_data) -> None:
        super().__init__(cmd)
        self.length = None
        self.result = 1

        self.user_episode_append_id_list = ["10001", "10002", "10003", "10004", "10005"]
        self.user_id_list = [str(profile_data["user"]), str(profile_data["user"]), str(profile_data["user"]), str(profile_data["user"]), str(profile_data["user"])]
        self.episode_append_id_list = [10001, 10002, 10003, 10004, 10005]
        self.own_num_list = [3, 3, 3, 3 ,3]
    
    def make(self) -> bytes:
        episode_data_struct = Struct(
            "user_episode_append_id_size" / Int32ub,  # big endian
            "user_episode_append_id" / Int16ul[5], #forced to match the user_episode_append_id_list index which is always 5 chars for the episode ids
            "user_id_size" / Int32ub,  # big endian
            "user_id" / Int16ul[6], # has to be exactly 6 chars in the user field... MANDATORY
            "episode_append_id" / Int32ub,
            "own_num" / Int32ub,
        )

        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "episode_append_data_list_size" / Rebuild(Int32ub, len_(this.episode_append_data_list)),  # big endian
            "episode_append_data_list" / Array(this.episode_append_data_list_size, episode_data_struct),
        )

        # really dump to parse the build resp, but that creates a new object
        # and is nicer to twork with
        resp_data = resp_struct.parse(resp_struct.build(dict(
            result=self.result,
            episode_append_data_list_size=0,
            episode_append_data_list=[],
        )))

        if len(self.user_episode_append_id_list) != len(self.user_id_list) != len(self.episode_append_id_list) != len(self.own_num_list):
            raise ValueError("all lists must be of the same length")

        for i in range(len(self.user_id_list)):
            # add the episode_data_struct to the resp_struct.episode_append_data_list
            resp_data.episode_append_data_list.append(dict(
                user_episode_append_id_size=len(self.user_episode_append_id_list[i]) * 2,
                user_episode_append_id=[ord(x) for x in self.user_episode_append_id_list[i]],
                user_id_size=len(self.user_id_list[i]) * 2,
                user_id=[ord(x) for x in self.user_id_list[i]],
                episode_append_id=self.episode_append_id_list[i],
                own_num=self.own_num_list[i],
            ))

        # finally, rebuild the resp_data
        resp_data = resp_struct.build(resp_data)

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoGetPartyDataListRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoGetPartyDataListResponse(SaoBaseResponse): # Default party 
    def __init__(self, cmd) -> None:
        super().__init__(cmd)
        self.result = 1
        self.party_data_list_size = 1 # Number of arrays

        self.user_party_id = "0"
        self.team_no = 0
        self.party_team_data_list_size = 3 # Number of arrays

        self.user_party_team_id_1 = "0"
        self.arrangement_num_1 = 0
        self.user_hero_log_id_1 = "101000010"
        self.main_weapon_user_equipment_id_1 = "101000016"
        self.sub_equipment_user_equipment_id_1 = "0"
        self.skill_slot1_skill_id_1 = 30086
        self.skill_slot2_skill_id_1 = 1001
        self.skill_slot3_skill_id_1 = 1002
        self.skill_slot4_skill_id_1 = 1003
        self.skill_slot5_skill_id_1 = 1005

        self.user_party_team_id_2 = "0"
        self.arrangement_num_2 = 0
        self.user_hero_log_id_2 = "102000010"
        self.main_weapon_user_equipment_id_2 = "103000006"
        self.sub_equipment_user_equipment_id_2 = "0"
        self.skill_slot1_skill_id_2 = 30086
        self.skill_slot2_skill_id_2 = 1001
        self.skill_slot3_skill_id_2 = 1002
        self.skill_slot4_skill_id_2 = 1003
        self.skill_slot5_skill_id_2 = 1005

        self.user_party_team_id_3 = "0"
        self.arrangement_num_3 = 0
        self.user_hero_log_id_3 = "103000010"
        self.main_weapon_user_equipment_id_3 = "112000009"
        self.sub_equipment_user_equipment_id_3 = "0"
        self.skill_slot1_skill_id_3 = 30086
        self.skill_slot2_skill_id_3 = 1001
        self.skill_slot3_skill_id_3 = 1002
        self.skill_slot4_skill_id_3 = 1003
        self.skill_slot5_skill_id_3 = 1005
    
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul, # result is either 0 or 1
            "party_data_list_size" / Int32ub, # big endian

            "user_party_id_size" / Int32ub, # big endian
            "user_party_id" / Int16ul[len(self.user_party_id)],
            "team_no" / Int8ul, # result is either 0 or 1
            "party_team_data_list_size" / Int32ub, # big endian

            "user_party_team_id_1_size" / Int32ub, # big endian
            "user_party_team_id_1" / Int16ul[len(self.user_party_team_id_1)],
            "arrangement_num_1" / Int8ul, # big endian
            "user_hero_log_id_1_size" / Int32ub, # big endian
            "user_hero_log_id_1" / Int16ul[len(self.user_hero_log_id_1)],
            "main_weapon_user_equipment_id_1_size" / Int32ub, # big endian
            "main_weapon_user_equipment_id_1" / Int16ul[len(self.main_weapon_user_equipment_id_1)],
            "sub_equipment_user_equipment_id_1_size" / Int32ub, # big endian
            "sub_equipment_user_equipment_id_1" / Int16ul[len(self.sub_equipment_user_equipment_id_1)],
            "skill_slot1_skill_id_1" / Int32ub,
            "skill_slot2_skill_id_1" / Int32ub,
            "skill_slot3_skill_id_1" / Int32ub,
            "skill_slot4_skill_id_1" / Int32ub,
            "skill_slot5_skill_id_1" / Int32ub,

            "user_party_team_id_2_size" / Int32ub, # big endian
            "user_party_team_id_2" / Int16ul[len(self.user_party_team_id_2)],
            "arrangement_num_2" / Int8ul, # result is either 0 or 1
            "user_hero_log_id_2_size" / Int32ub, # big endian
            "user_hero_log_id_2" / Int16ul[len(self.user_hero_log_id_2)],
            "main_weapon_user_equipment_id_2_size" / Int32ub, # big endian
            "main_weapon_user_equipment_id_2" / Int16ul[len(self.main_weapon_user_equipment_id_2)],
            "sub_equipment_user_equipment_id_2_size" / Int32ub, # big endian
            "sub_equipment_user_equipment_id_2" / Int16ul[len(self.sub_equipment_user_equipment_id_2)],
            "skill_slot1_skill_id_2" / Int32ub,
            "skill_slot2_skill_id_2" / Int32ub,
            "skill_slot3_skill_id_2" / Int32ub,
            "skill_slot4_skill_id_2" / Int32ub,
            "skill_slot5_skill_id_2" / Int32ub,

            "user_party_team_id_3_size" / Int32ub, # big endian
            "user_party_team_id_3" / Int16ul[len(self.user_party_team_id_3)],
            "arrangement_num_3" / Int8ul, # result is either 0 or 1
            "user_hero_log_id_3_size" / Int32ub, # big endian
            "user_hero_log_id_3" / Int16ul[len(self.user_hero_log_id_3)],
            "main_weapon_user_equipment_id_3_size" / Int32ub, # big endian
            "main_weapon_user_equipment_id_3" / Int16ul[len(self.main_weapon_user_equipment_id_3)],
            "sub_equipment_user_equipment_id_3_size" / Int32ub, # big endian
            "sub_equipment_user_equipment_id_3" / Int16ul[len(self.sub_equipment_user_equipment_id_3)],
            "skill_slot1_skill_id_3" / Int32ub,
            "skill_slot2_skill_id_3" / Int32ub,
            "skill_slot3_skill_id_3" / Int32ub,
            "skill_slot4_skill_id_3" / Int32ub,
            "skill_slot5_skill_id_3" / Int32ub,

        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            party_data_list_size=self.party_data_list_size,

            user_party_id_size=len(self.user_party_id) * 2,
            user_party_id=[ord(x) for x in self.user_party_id],
            team_no=self.team_no,
            party_team_data_list_size=self.party_team_data_list_size,

            user_party_team_id_1_size=len(self.user_party_team_id_1) * 2,
            user_party_team_id_1=[ord(x) for x in self.user_party_team_id_1],
            arrangement_num_1=self.arrangement_num_1,
            user_hero_log_id_1_size=len(self.user_hero_log_id_1) * 2,
            user_hero_log_id_1=[ord(x) for x in self.user_hero_log_id_1],
            main_weapon_user_equipment_id_1_size=len(self.main_weapon_user_equipment_id_1) * 2,
            main_weapon_user_equipment_id_1=[ord(x) for x in self.main_weapon_user_equipment_id_1],
            sub_equipment_user_equipment_id_1_size=len(self.sub_equipment_user_equipment_id_1) * 2,
            sub_equipment_user_equipment_id_1=[ord(x) for x in self.sub_equipment_user_equipment_id_1],
            skill_slot1_skill_id_1=self.skill_slot1_skill_id_1,
            skill_slot2_skill_id_1=self.skill_slot2_skill_id_1,
            skill_slot3_skill_id_1=self.skill_slot3_skill_id_1,
            skill_slot4_skill_id_1=self.skill_slot4_skill_id_1,
            skill_slot5_skill_id_1=self.skill_slot5_skill_id_1,

            user_party_team_id_2_size=len(self.user_party_team_id_2) * 2,
            user_party_team_id_2=[ord(x) for x in self.user_party_team_id_2],
            arrangement_num_2=self.arrangement_num_2,
            user_hero_log_id_2_size=len(self.user_hero_log_id_2) * 2,
            user_hero_log_id_2=[ord(x) for x in self.user_hero_log_id_2],
            main_weapon_user_equipment_id_2_size=len(self.main_weapon_user_equipment_id_2) * 2,
            main_weapon_user_equipment_id_2=[ord(x) for x in self.main_weapon_user_equipment_id_2],
            sub_equipment_user_equipment_id_2_size=len(self.sub_equipment_user_equipment_id_2) * 2,
            sub_equipment_user_equipment_id_2=[ord(x) for x in self.sub_equipment_user_equipment_id_2],
            skill_slot1_skill_id_2=self.skill_slot1_skill_id_2,
            skill_slot2_skill_id_2=self.skill_slot2_skill_id_2,
            skill_slot3_skill_id_2=self.skill_slot3_skill_id_2,
            skill_slot4_skill_id_2=self.skill_slot4_skill_id_2,
            skill_slot5_skill_id_2=self.skill_slot5_skill_id_2,

            user_party_team_id_3_size=len(self.user_party_team_id_3) * 2,
            user_party_team_id_3=[ord(x) for x in self.user_party_team_id_3],
            arrangement_num_3=self.arrangement_num_3,
            user_hero_log_id_3_size=len(self.user_hero_log_id_3) * 2,
            user_hero_log_id_3=[ord(x) for x in self.user_hero_log_id_3],
            main_weapon_user_equipment_id_3_size=len(self.main_weapon_user_equipment_id_3) * 2,
            main_weapon_user_equipment_id_3=[ord(x) for x in self.main_weapon_user_equipment_id_3],
            sub_equipment_user_equipment_id_3_size=len(self.sub_equipment_user_equipment_id_3) * 2,
            sub_equipment_user_equipment_id_3=[ord(x) for x in self.sub_equipment_user_equipment_id_3],
            skill_slot1_skill_id_3=self.skill_slot1_skill_id_3,
            skill_slot2_skill_id_3=self.skill_slot2_skill_id_3,
            skill_slot3_skill_id_3=self.skill_slot3_skill_id_3,
            skill_slot4_skill_id_3=self.skill_slot4_skill_id_3,
            skill_slot5_skill_id_3=self.skill_slot5_skill_id_3,
        ))

        self.length = len(resp_data)
        return super().make() + resp_data
    
class SaoGetQuestScenePrevScanProfileCardRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoGetQuestScenePrevScanProfileCardResponse(SaoBaseResponse):
    def __init__(self, cmd) -> None:
        super().__init__(cmd)
        self.result = 1
        self.profile_card_data = 1 # number of arrays 
        
        self.profile_card_code = ""
        self.nick_name = ""
    
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul, # result is either 0 or 1
            "profile_card_data" / Int32ub, # big endian

            "profile_card_code_size" / Int32ub, # big endian
            "profile_card_code" / Int16ul[len(self.profile_card_code)],
            "nick_name_size" / Int32ub, # big endian
            "nick_name" / Int16ul[len(self.nick_name)],
            "rank_num" / Int16ub, #short
            "setting_title_id" / Int32ub, # int
            "skill_id" / Int16ub, # short
            "hero_log_hero_log_id" / Int32ub, # int
            "hero_log_log_level" / Int16ub, # short
            "hero_log_awakening_stage" / Int16ub, # short
            "hero_log_property1_property_id" / Int32ub, # int
            "hero_log_property1_value1" / Int32ub, # int
            "hero_log_property1_value2" / Int32ub, # int
            "hero_log_property2_property_id" / Int32ub, # int
            "hero_log_property2_value1" / Int32ub, # int
            "hero_log_property2_value2" / Int32ub, # int
            "hero_log_property3_property_id" / Int32ub, # int
            "hero_log_property3_value1" / Int32ub, # int
            "hero_log_property3_value2" / Int32ub, # int
            "hero_log_property4_property_id" / Int32ub, # int
            "hero_log_property4_value1" / Int32ub, # int
            "hero_log_property4_value2" / Int32ub, # int
            "main_weapon_equipment_id" / Int32ub, # int
            "main_weapon_enhancement_value" / Int16ub, # short
            "main_weapon_awakening_stage" / Int16ub, # short       
            "main_weapon_property1_property_id" / Int32ub, # int
            "main_weapon_property1_value1" / Int32ub, # int
            "main_weapon_property1_value2" / Int32ub, # int
            "main_weapon_property2_property_id" / Int32ub, # int
            "main_weapon_property2_value1" / Int32ub, # int
            "main_weapon_property2_value2" / Int32ub, # int
            "main_weapon_property3_property_id" / Int32ub, # int
            "main_weapon_property3_value1" / Int32ub, # int
            "main_weapon_property3_value2" / Int32ub, # int
            "main_weapon_property4_property_id" / Int32ub, # int
            "main_weapon_property4_value1" / Int32ub, # int
            "main_weapon_property4_value2" / Int32ub, # int
            "sub_equipment_equipment_id" / Int32ub, # int
            "sub_equipment_enhancement_value" / Int16ub, # short
            "sub_equipment_awakening_stage" / Int16ub, # short
            "sub_equipment_property1_property_id" / Int32ub, # int
            "sub_equipment_property1_value1" / Int32ub, # int
            "sub_equipment_property1_value2" / Int32ub, # int
            "sub_equipment_property2_property_id" / Int32ub, # int
            "sub_equipment_property2_value1" / Int32ub, # int
            "sub_equipment_property2_value2" / Int32ub, # int
            "sub_equipment_property3_property_id" / Int32ub, # int
            "sub_equipment_property3_value1" / Int32ub, # int
            "sub_equipment_property3_value2" / Int32ub, # int
            "sub_equipment_property4_property_id" / Int32ub, # int
            "sub_equipment_property4_value1" / Int32ub, # int
            "sub_equipment_property4_value2" / Int32ub, # int
            "holographic_flag" / Int8ul, # result is either 0 or 1
        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            profile_card_data=self.profile_card_data,
            
            profile_card_code_size=len(self.profile_card_code) * 2,
            profile_card_code=[ord(x) for x in self.profile_card_code],
            nick_name_size=len(self.nick_name) * 2,
            nick_name=[ord(x) for x in self.nick_name],
            rank_num=0,
            setting_title_id=0,
            skill_id=0,
            hero_log_hero_log_id=0,
            hero_log_log_level=0,
            hero_log_awakening_stage=0,
            hero_log_property1_property_id=0,
            hero_log_property1_value1=0,
            hero_log_property1_value2=0,
            hero_log_property2_property_id=0,
            hero_log_property2_value1=0,
            hero_log_property2_value2=0,
            hero_log_property3_property_id=0,
            hero_log_property3_value1=0,
            hero_log_property3_value2=0,
            hero_log_property4_property_id=0,
            hero_log_property4_value1=0,
            hero_log_property4_value2=0,
            main_weapon_equipment_id=0,
            main_weapon_enhancement_value=0,
            main_weapon_awakening_stage=0,
            main_weapon_property1_property_id=0,
            main_weapon_property1_value1=0,
            main_weapon_property1_value2=0,
            main_weapon_property2_property_id=0,
            main_weapon_property2_value1=0,
            main_weapon_property2_value2=0,
            main_weapon_property3_property_id=0,
            main_weapon_property3_value1=0,
            main_weapon_property3_value2=0,
            main_weapon_property4_property_id=0,
            main_weapon_property4_value1=0,
            main_weapon_property4_value2=0,
            sub_equipment_equipment_id=0,
            sub_equipment_enhancement_value=0,
            sub_equipment_awakening_stage=0,
            sub_equipment_property1_property_id=0,
            sub_equipment_property1_value1=0,
            sub_equipment_property1_value2=0,
            sub_equipment_property2_property_id=0,
            sub_equipment_property2_value1=0,
            sub_equipment_property2_value2=0,
            sub_equipment_property3_property_id=0,
            sub_equipment_property3_value1=0,
            sub_equipment_property3_value2=0,
            sub_equipment_property4_property_id=0,
            sub_equipment_property4_value1=0,
            sub_equipment_property4_value2=0,
            holographic_flag=0,
            
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoGetResourcePathInfoRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoGetResourcePathInfoResponse(SaoBaseResponse):
    def __init__(self, cmd) -> None:
        super().__init__(cmd)
        self.result = 1
        self.resource_base_url = "http://localhost:9000/SDEW/100/"
        self.gasha_base_dir = "a"
        self.ad_base_dir = "b"
        self.event_base_dir = "c"
    
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "resource_base_url_size" / Int32ub,  # big endian
            "resource_base_url" / Int16ul[len(self.resource_base_url)],
            "gasha_base_dir_size" / Int32ub,  # big endian
            "gasha_base_dir" / Int16ul[len(self.gasha_base_dir)],
            "ad_base_dir_size" / Int32ub,  # big endian
            "ad_base_dir" / Int16ul[len(self.ad_base_dir)],
            "event_base_dir_size" / Int32ub,  # big endian
            "event_base_dir" / Int16ul[len(self.event_base_dir)],
        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            resource_base_url_size=len(self.resource_base_url) * 2,
            resource_base_url=[ord(x) for x in self.resource_base_url],
            gasha_base_dir_size=len(self.gasha_base_dir) * 2,
            gasha_base_dir=[ord(x) for x in self.gasha_base_dir],
            ad_base_dir_size=len(self.ad_base_dir) * 2,
            ad_base_dir=[ord(x) for x in self.ad_base_dir],
            event_base_dir_size=len(self.event_base_dir) * 2,
            event_base_dir=[ord(x) for x in self.event_base_dir],
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoEpisodePlayStartRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoEpisodePlayStartResponse(SaoBaseResponse):
    def __init__(self, cmd, profile_data) -> None:
        super().__init__(cmd)
        self.result = 1
        self.play_start_response_data_size = 1 # Number of arrays (minimum 1 mandatory)
        self.multi_play_start_response_data_size = 0 # Number of arrays (set 0 due to single play)

        self.appearance_player_trace_data_list_size = 1

        self.user_quest_scene_player_trace_id = "1003"
        self.nick_name = profile_data["nick_name"]
    
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "play_start_response_data_size" / Int32ub,
            "multi_play_start_response_data_size" / Int32ub,

            "appearance_player_trace_data_list_size" / Int32ub,

            "user_quest_scene_player_trace_id_size" / Int32ub, # big endian
            "user_quest_scene_player_trace_id" / Int16ul[len(self.user_quest_scene_player_trace_id)],
            "nick_name_size" / Int32ub, # big endian
            "nick_name" / Int16ul[len(self.nick_name)],
        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            play_start_response_data_size=self.play_start_response_data_size,
            multi_play_start_response_data_size=self.multi_play_start_response_data_size,

            appearance_player_trace_data_list_size=self.appearance_player_trace_data_list_size,

            user_quest_scene_player_trace_id_size=len(self.user_quest_scene_player_trace_id) * 2,
            user_quest_scene_player_trace_id=[ord(x) for x in self.user_quest_scene_player_trace_id],
            nick_name_size=len(self.nick_name) * 2,
            nick_name=[ord(x) for x in self.nick_name],
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoEpisodePlayEndRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoEpisodePlayEndResponse(SaoBaseResponse):
    def __init__(self, cmd) -> None:
        super().__init__(cmd)
        self.result = 1
        self.play_end_response_data_size = 1  # Number of arrays
        self.multi_play_end_response_data_size = 1  # Unused on solo play

        self.dummy_1 = 0
        self.dummy_2 = 0
        self.dummy_3 = 0

        self.rarity_up_occurrence_flag = 0
        self.adventure_ex_area_occurrences_flag = 0
        self.ex_bonus_data_list_size = 1  # Number of arrays
        self.play_end_player_trace_reward_data_list_size = 0  # Number of arrays

        self.ex_bonus_table_id = 0  # ExBonusTable.csv values, dont care for now
        self.achievement_status = 1

        self.common_reward_data_size = 1  # Number of arrays

        self.common_reward_type = 0  # dummy values from 2,101000000,1 from RewardTable.csv
        self.common_reward_id = 0
        self.common_reward_num = 0
        
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "play_end_response_data_size" / Int32ub,  # big endian

            "rarity_up_occurrence_flag" / Int8ul,  # result is either 0 or 1
            "adventure_ex_area_occurrences_flag" / Int8ul,  # result is either 0 or 1
            "ex_bonus_data_list_size" / Int32ub,  # big endian
            "play_end_player_trace_reward_data_list_size" / Int32ub,  # big endian

            # ex_bonus_data_list
            "ex_bonus_table_id" / Int32ub,
            "achievement_status" / Int8ul,  # result is either 0 or 1

            # play_end_player_trace_reward_data_list
            "common_reward_data_size" / Int32ub,

            # common_reward_data
            "common_reward_type" / Int16ub,  # short
            "common_reward_id" / Int32ub,
            "common_reward_num" / Int32ub,

            "multi_play_end_response_data_size" / Int32ub,  # big endian

            # multi_play_end_response_data
            "dummy_1" / Int8ul,  # result is either 0 or 1
            "dummy_2" / Int8ul,  # result is either 0 or 1
            "dummy_3" / Int8ul,  # result is either 0 or 1
        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            play_end_response_data_size=self.play_end_response_data_size,

            rarity_up_occurrence_flag=self.rarity_up_occurrence_flag,
            adventure_ex_area_occurrences_flag=self.adventure_ex_area_occurrences_flag,
            ex_bonus_data_list_size=self.ex_bonus_data_list_size,
            play_end_player_trace_reward_data_list_size=self.play_end_player_trace_reward_data_list_size,
            
            ex_bonus_table_id=self.ex_bonus_table_id,
            achievement_status=self.achievement_status,
            
            common_reward_data_size=self.common_reward_data_size,
            
            common_reward_type=self.common_reward_type,
            common_reward_id=self.common_reward_id,
            common_reward_num=self.common_reward_num,
            
            multi_play_end_response_data_size=self.multi_play_end_response_data_size,
            
            dummy_1=self.dummy_1,
            dummy_2=self.dummy_2,
            dummy_3=self.dummy_3,
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoEpisodePlayEndUnanalyzedLogFixedRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoEpisodePlayEndUnanalyzedLogFixedResponse(SaoBaseResponse):
    def __init__(self, cmd) -> None:
        super().__init__(cmd)
        self.result = 1
        self.play_end_unanalyzed_log_reward_data_list_size = 1 # Number of arrays

        self.unanalyzed_log_grade_id = 3 # RewardTable.csv
        self.common_reward_data_size = 1

        self.common_reward_type_1 = 1
        self.common_reward_id_1 = 102000070
        self.common_reward_num_1 = 1
    
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "play_end_unanalyzed_log_reward_data_list_size" / Int32ub,  # big endian

            "unanalyzed_log_grade_id" / Int32ub,
            "common_reward_data_size" / Int32ub,

            "common_reward_type_1" / Int16ub,
            "common_reward_id_1" / Int32ub,
            "common_reward_num_1" / Int32ub,
        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            play_end_unanalyzed_log_reward_data_list_size=self.play_end_unanalyzed_log_reward_data_list_size,
            
            unanalyzed_log_grade_id=self.unanalyzed_log_grade_id,
            common_reward_data_size=self.common_reward_data_size,

            common_reward_type_1=self.common_reward_type_1,
            common_reward_id_1=self.common_reward_id_1,
            common_reward_num_1=self.common_reward_num_1,
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoGetQuestSceneUserDataListRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoGetQuestSceneUserDataListResponse(SaoBaseResponse):
    def __init__(self, cmd, questIdsData) -> None:
        super().__init__(cmd)
        self.result = 1

        # quest_scene_user_data_list_size
        self.quest_type = [1] * len(questIdsData)
        self.quest_scene_id = questIdsData
        self.clear_flag = [1] * len(questIdsData)

        # quest_scene_best_score_user_data
        self.clear_time = 300
        self.combo_num = 0
        self.total_damage = "0"
        self.concurrent_destroying_num = 1

        # quest_scene_ex_bonus_user_data_list
        self.achievement_flag = [[1, 1, 1],[1, 1, 1]]
        self.ex_bonus_table_id = [[1, 2, 3],[4, 5, 6]]
    
    def make(self) -> bytes:
        #new stuff
        quest_scene_ex_bonus_user_data_list_struct = Struct(
            "achievement_flag" / Int32ub,  # big endian
            "ex_bonus_table_id" / Int32ub,  # big endian
        )

        quest_scene_best_score_user_data_struct = Struct(
            "clear_time" / Int32ub,  # big endian
            "combo_num" / Int32ub,  # big endian
            "total_damage_size" / Int32ub, # big endian
            "total_damage" / Int16ul[len(self.total_damage)],
            "concurrent_destroying_num" / Int16ub,
        )

        quest_scene_user_data_list_struct = Struct(
            "quest_type" / Int8ul, # result is either 0 or 1
            "quest_scene_id" / Int16ub, #short
            "clear_flag" / Int8ul, # result is either 0 or 1
            "quest_scene_best_score_user_data_size" / Rebuild(Int32ub, len_(this.quest_scene_best_score_user_data)),  # big endian
            "quest_scene_best_score_user_data" / Array(this.quest_scene_best_score_user_data_size, quest_scene_best_score_user_data_struct),
            "quest_scene_ex_bonus_user_data_list_size" / Rebuild(Int32ub, len_(this.quest_scene_ex_bonus_user_data_list)),  # big endian
            "quest_scene_ex_bonus_user_data_list" / Array(this.quest_scene_ex_bonus_user_data_list_size, quest_scene_ex_bonus_user_data_list_struct),
        )

        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul,  # result is either 0 or 1
            "quest_scene_user_data_list_size" / Rebuild(Int32ub, len_(this.quest_scene_user_data_list)),  # big endian
            "quest_scene_user_data_list" / Array(this.quest_scene_user_data_list_size, quest_scene_user_data_list_struct),
        )

        resp_data = resp_struct.parse(resp_struct.build(dict(
            result=self.result,
            quest_scene_user_data_list_size=0,
            quest_scene_user_data_list=[],
        )))

        for i in range(len(self.quest_scene_id)):
            quest_data = dict(
                quest_type=self.quest_type[i],
                quest_scene_id=self.quest_scene_id[i],
                clear_flag=self.clear_flag[i],

                quest_scene_best_score_user_data_size=0,
                quest_scene_best_score_user_data=[],
                quest_scene_ex_bonus_user_data_list_size=0,
                quest_scene_ex_bonus_user_data_list=[],
            )

            quest_data["quest_scene_best_score_user_data"].append(dict(
                clear_time=self.clear_time,
                combo_num=self.combo_num,
                total_damage_size=len(self.total_damage) * 2,
                total_damage=[ord(x) for x in self.total_damage],
                concurrent_destroying_num=self.concurrent_destroying_num,
            ))

            '''
            quest_data["quest_scene_ex_bonus_user_data_list"].append(dict(
                ex_bonus_table_id=self.ex_bonus_table_id[i],
                achievement_flag=self.achievement_flag[i],
            ))
            '''
            
            resp_data.quest_scene_user_data_list.append(quest_data)

        # finally, rebuild the resp_data
        resp_data = resp_struct.build(resp_data)

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoCheckYuiMedalGetConditionRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoCheckYuiMedalGetConditionResponse(SaoBaseResponse):
    def __init__(self, cmd) -> None:
        super().__init__(cmd)
        self.result = 1
        self.get_flag = 1
        self.elapsed_days = 1
        self.get_yui_medal_num = 1
    
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul, # result is either 0 or 1
            "get_flag" / Int8ul, # result is either 0 or 1
            "elapsed_days" / Int16ub, #short
            "get_yui_medal_num" / Int16ub, #short
        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            get_flag=self.get_flag,
            elapsed_days=self.elapsed_days,
            get_yui_medal_num=self.get_yui_medal_num,
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoGetYuiMedalBonusUserDataRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoGetYuiMedalBonusUserDataResponse(SaoBaseResponse):
    def __init__(self, cmd) -> None:
        super().__init__(cmd)
        self.result = 1
        self.data_size = 1 # number of arrays

        self.elapsed_days = 1
        self.loop_num = 1
        self.last_check_date = "20230520193000"
        self.last_get_date = "20230520193000"
    
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul, # result is either 0 or 1
            "data_size" / Int32ub, # big endian

            "elapsed_days" / Int32ub, # big endian
            "loop_num" / Int32ub, # big endian
            "last_check_date_size" / Int32ub, # big endian
            "last_check_date" / Int16ul[len(self.last_check_date)],
            "last_get_date_size" / Int32ub, # big endian
            "last_get_date" / Int16ul[len(self.last_get_date)],
        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            data_size=self.data_size,

            elapsed_days=self.elapsed_days,
            loop_num=self.loop_num,
            last_check_date_size=len(self.last_check_date) * 2,
            last_check_date=[ord(x) for x in self.last_check_date],
            last_get_date_size=len(self.last_get_date) * 2,
            last_get_date=[ord(x) for x in self.last_get_date],
            
        ))

        self.length = len(resp_data)
        return super().make() + resp_data

class SaoCheckProfileCardUsedRewardRequest(SaoBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)

class SaoCheckProfileCardUsedRewardResponse(SaoBaseResponse):
    def __init__(self, cmd) -> None:
        super().__init__(cmd)
        self.result = 1
        self.get_flag = 1
        self.used_num = 0
        self.get_vp = 1
    
    def make(self) -> bytes:
        # create a resp struct
        resp_struct = Struct(
            "result" / Int8ul, # result is either 0 or 1
            "get_flag" / Int8ul, # result is either 0 or 1
            "used_num" / Int32ub, # big endian
            "get_vp" / Int32ub, # big endian
        )

        resp_data = resp_struct.build(dict(
            result=self.result,
            get_flag=self.get_flag,
            used_num=self.used_num,
            get_vp=self.get_vp,
            
        ))

        self.length = len(resp_data)
        return super().make() + resp_data