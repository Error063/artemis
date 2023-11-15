from typing import Tuple, List, Optional
import struct
import logging
from datetime import datetime

BIGINT_OFF = 16
LONG_OFF = 8
INT_OFF = 4
SHORT_OFF = 2
BYTE_OFF = 1

DT_FMT = "%Y%m%d%H%M%S"

def fmt_dt(d: Optional[datetime] = None) -> str:
    if d is None:
        d = datetime.fromtimestamp(0)
    return d.strftime(DT_FMT)

def prs_dt(s: Optional[str] = None) -> datetime:
    if not s:
        s = "19691231190000"
    return datetime.strptime(s, DT_FMT)

def decode_num(data: bytes, offset: int, size: int) -> int:
    try:
        return int.from_bytes(data[offset:offset + size], 'big')
    except:
        logging.getLogger('sao').error(f"Failed to parse {data[offset:offset + size]} as BE number of width {size}")
        return 0

def decode_byte(data: bytes, offset: int) -> int:
    return decode_num(data, offset, BYTE_OFF)

def decode_short(data: bytes, offset: int) -> int:
    return decode_num(data, offset, SHORT_OFF)

def decode_int(data: bytes, offset: int) -> int:
    return decode_num(data, offset, INT_OFF)

def decode_long(data: bytes, offset: int) -> int:
    return decode_num(data, offset, LONG_OFF)

def decode_bigint(data: bytes, offset: int) -> int:
    return decode_num(data, offset, BIGINT_OFF)

def decode_str(data: bytes, offset: int) -> Tuple[str, int]:
    try:
        str_len = decode_int(data, offset)
        num_bytes_decoded = INT_OFF + str_len
        str_out = data[offset + INT_OFF:offset + num_bytes_decoded].decode("utf-16-le", errors="replace")
        return (str_out, num_bytes_decoded)
    except:
        logging.getLogger('sao').error(f"Failed to parse {data[offset:]} as string!")
        return ("", 0)

def decode_arr_num(data: bytes, offset:int, element_size: int) -> Tuple[List[int], int]:
    size = 0
    num_obj = decode_int(data, offset + size)
    size += INT_OFF
    
    ret: List[int] = []
    for _ in range(num_obj):
        ret.append(decode_num(data, offset + size, element_size))
        size += element_size
    
    return (ret, size)

def decode_arr_str(data: bytes, offset: int) -> Tuple[List[str], int]:
    size = 0
    num_obj = decode_int(data, offset + size)
    size += INT_OFF
    
    ret: List[str] = []
    for _ in range(num_obj):
        tmp = decode_str(data, offset + size)
        ret.append(tmp[0])
        size += tmp[1]
    
    return (ret, size)

def encode_byte(data: int) -> bytes:
    return struct.pack("!b", data)

def encode_short(data: int) -> bytes:
    return struct.pack("!h", data)

def encode_int(data: int) -> bytes:
    return struct.pack("!i", data)

def encode_long(data: int) -> bytes:
    return struct.pack("!l", data)

def encode_bigint(data: int) -> bytes:
    return struct.pack("!q", data)

def encode_str(s: str) -> bytes:
    try:
        str_bytes = s.encode("utf-16-le", errors="replace")
        str_len_bytes = struct.pack("!I", len(str_bytes))
        return str_len_bytes + str_bytes
    except:
        logging.getLogger('sao').error(f"Failed to encode {s} as bytes!")
        return b""

def encode_arr_num(data: List[int], element_size: int) -> bytes:
    ret = encode_int(len(data))
        
    if element_size == BYTE_OFF:
        for x in data:
            ret += encode_byte(x)
    elif element_size == SHORT_OFF:
        for x in data:
            ret += encode_short(x)
    elif element_size == INT_OFF:
        for x in data:
            ret += encode_int(x)
    elif element_size == LONG_OFF:
        for x in data:
            ret += encode_long(x)
    elif element_size == BIGINT_OFF:
        for x in data:
            ret += encode_bigint(x)
    else:
        logging.getLogger('sao').error(f"Unknown element size {element_size}")
        return b"\x00" * INT_OFF

    return ret

class BaseHelper:
    def __init__(self, data: bytes, offset: int) -> None:
        self._sz = 0
        
    @classmethod
    def from_args(cls) -> "BaseHelper":
        return cls(b"", 0)
    
    def get_size(self) -> int:
        return self._sz
    
    def make(self) -> bytes:
        return b""

def decode_arr_cls(data: bytes, offset: int, cls: BaseHelper):
    size = 0
    num_cls = decode_int(data, offset + size)
    cls_type = type(cls)
    
    ret: List[cls_type] = []
    for _ in range(num_cls):
        tmp = cls(data, offset + size)
        size += tmp.get_size()
        ret.append(tmp)
    
    return (ret, size)

def encode_arr_cls(data: List[BaseHelper]) -> bytes:
    ret = encode_int(len(data))
    
    for x in data:
        ret += x.make()
    
    return ret

class MaterialCommonRewardUserData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        super().__init__(data, offset)
        self.common_reward_type = decode_short(data, offset + self._sz)
        self._sz += SHORT_OFF

        user_common_reward_id = decode_str(data, offset + self._sz)
        self.user_common_reward_id = user_common_reward_id[0]
        self._sz += user_common_reward_id[1]

class PartyTeamData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        sz = 0
        user_party_team_id = decode_str(data, offset + sz)
        self.user_party_team_id = user_party_team_id[0]
        sz += user_party_team_id[1]

        self.arrangement_num = decode_byte(data, offset + sz)
        sz += BYTE_OFF

        user_hero_log_id = decode_str(data, offset + sz)
        self.user_hero_log_id = user_hero_log_id[0]
        sz += user_hero_log_id[1]

        main_weapon_user_equipment_id = decode_str(data, offset + sz)
        self.main_weapon_user_equipment_id = main_weapon_user_equipment_id[0]
        sz += main_weapon_user_equipment_id[1]

        sub_equipment_user_equipment_id = decode_str(data, offset + sz)
        self.sub_equipment_user_equipment_id = sub_equipment_user_equipment_id[0]
        sz += sub_equipment_user_equipment_id[1]

        self.skill_slot1_skill_id = decode_int(data, offset + sz)
        sz += INT_OFF

        self.skill_slot2_skill_id = decode_int(data, offset + sz)
        sz += INT_OFF

        self.skill_slot3_skill_id = decode_int(data, offset + sz)
        sz += INT_OFF

        self.skill_slot4_skill_id = decode_int(data, offset + sz)
        sz += INT_OFF

        self.skill_slot5_skill_id = decode_int(data, offset + sz)
        sz += INT_OFF

        self._sz = sz

class PartyData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        sz = 0
        user_party_id = decode_str(data, offset + sz)
        self.user_party_id = user_party_id[0]
        sz += user_party_id[1]

        self.team_no = decode_byte(data, offset + sz)
        sz += BYTE_OFF

        self.party_team_data_count = decode_int(data, offset + sz)
        sz += INT_OFF

        self.party_team_data_list: List[PartyTeamData] = []
        for _ in range(self.party_team_data_count):
            tmp = PartyTeamData(data, offset + sz)
            self.party_team_data_list.append(tmp)
            sz += tmp.get_size()

        self._sz = sz

class PlayStartRequestData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        sz = 0
        user_party_id = decode_str(data, offset + sz)
        self.user_party_id = user_party_id[0]
        sz += user_party_id[1]

        appoint_leader_resource_card_code = decode_str(data, offset + sz)
        self.appoint_leader_resource_card_code = appoint_leader_resource_card_code[0]
        sz += appoint_leader_resource_card_code[1]

        use_profile_card_code = decode_str(data, offset + sz)
        self.use_profile_card_code = use_profile_card_code[0]
        sz += use_profile_card_code[1]

        self.quest_drop_boost_apply_flag = decode_byte(data, offset + sz)
        sz += BYTE_OFF

        self._sz = sz

class GetPlayerTraceData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        user_quest_scene_player_trace_id = decode_str(data, offset)
        self.user_quest_scene_player_trace_id = user_quest_scene_player_trace_id[0]
        self._sz = user_quest_scene_player_trace_id[1]

class BaseGetData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        self.get_hero_log_exp = decode_int(data, offset)
        offset += INT_OFF

        self.get_col = decode_int(data, offset)

        self._sz = INT_OFF + INT_OFF

class RareDropData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        self.quest_rare_drop_id = decode_int(data, offset)

        self._sz = INT_OFF

class UnanalyzedLogTmpRewardData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        self.unanalyzed_log_grade_id = decode_int(data, offset)

        self._sz = INT_OFF

class SpecialRareDropData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        self.quest_special_rare_drop_id = decode_int(data, offset)

        self._sz = INT_OFF

class EventItemData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        self.event_item_id = decode_int(data, offset)
        offset += INT_OFF
        self.get_num = decode_short(data, offset)

        self._sz = INT_OFF + SHORT_OFF

class DiscoveryEnemyData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        self.enemy_kind_id = decode_int(data, offset)
        offset += INT_OFF
        self.destroy_num = decode_short(data, offset)

        self._sz = INT_OFF + SHORT_OFF

class DestroyBossData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        self.boss_type = decode_byte(data, offset)
        offset += BYTE_OFF
        self.enemy_kind_id = decode_int(data, offset)
        offset += INT_OFF
        self.mission_difficulty_id = decode_short(data, offset)

        self._sz = INT_OFF + SHORT_OFF + BYTE_OFF

class MissionData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        self.mission_id = decode_int(data, offset)
        offset += INT_OFF
        self.clear_flag = decode_byte(data, offset)
        offset += BYTE_OFF
        self.destroy_num = decode_short(data, offset)

        self._sz = INT_OFF + SHORT_OFF + BYTE_OFF

class ScoreData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        super().__init__(data, offset)
        self.clear_time = decode_int(data, offset + self._sz)
        self._sz += INT_OFF

        self.combo_num = decode_int(data, offset + self._sz)
        self._sz += INT_OFF

        total_damage = decode_str(data, offset + self._sz)
        self.total_damage = total_damage[0]
        self._sz += total_damage[1]

        self.concurrent_destroying_num = decode_short(data, offset + self._sz)
        self._sz += SHORT_OFF

        self.reaching_skill_level = decode_short(data, offset + self._sz)
        self._sz += SHORT_OFF

        self.ko_chara_num = decode_byte(data, offset + self._sz)
        self._sz += BYTE_OFF

        self.acceleration_invocation_num = decode_short(data, offset + self._sz)
        self._sz += SHORT_OFF

        self.boss_destroying_num = decode_short(data, offset + self._sz)
        self._sz += SHORT_OFF

        self.synchro_skill_used_flag = decode_byte(data, offset + self._sz)
        self._sz += BYTE_OFF

        self.used_friend_skill_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF

        self.friend_skill_used_flag = decode_byte(data, offset + self._sz)
        self._sz += BYTE_OFF

        self.continue_cnt = decode_short(data, offset + self._sz)
        self._sz += SHORT_OFF

        self.total_loss_num = decode_short(data, offset + self._sz)
        self._sz += SHORT_OFF

class PlayEndRequestData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        sz = 0
        self.play_result_flag = decode_byte(data, offset + sz)
        sz += BYTE_OFF

        self.base_get_data_count = decode_int(data, offset + sz)
        sz += INT_OFF

        self.base_get_data_list: List[BaseGetData] = []
        for _ in range(self.base_get_data_count):
            tmp = BaseGetData(data, offset + sz)
            sz += tmp.get_size()
            self.base_get_data_list.append(tmp)

        self.get_player_trace_data_count = decode_int(data, offset + sz)
        sz += INT_OFF

        self.get_player_trace_data: List[GetPlayerTraceData] = []
        for _ in range(self.get_player_trace_data_count):
            tmp = GetPlayerTraceData(data, offset + sz)
            sz += tmp.get_size()
            self.get_player_trace_data.append(tmp)

        self.get_rare_drop_data_count = decode_int(data, offset + sz)
        sz += INT_OFF

        self.get_rare_drop_data_list: List[RareDropData] = []
        for _ in range(self.get_rare_drop_data_count):
            tmp = RareDropData(data, offset + sz)
            sz += tmp.get_size()
            self.get_rare_drop_data_list.append(tmp)

        self.get_special_rare_drop_data_count = decode_int(data, offset + sz)
        sz += INT_OFF

        self.get_special_rare_drop_data_list: List[SpecialRareDropData] = []
        for _ in range(self.get_special_rare_drop_data_count):
            tmp = SpecialRareDropData(data, offset + sz)
            sz += tmp.get_size()
            self.get_special_rare_drop_data_list.append(tmp)

        self.get_unanalyzed_log_tmp_reward_data_count = decode_int(data, offset + sz)
        sz += INT_OFF

        self.get_unanalyzed_log_tmp_reward_data_list: List[UnanalyzedLogTmpRewardData] = []
        for _ in range(self.get_unanalyzed_log_tmp_reward_data_count):
            tmp = UnanalyzedLogTmpRewardData(data, offset + sz)
            sz += tmp.get_size()
            self.get_unanalyzed_log_tmp_reward_data_list.append(tmp)

        self.get_event_item_data_count = decode_int(data, offset + sz)
        sz += INT_OFF

        self.get_event_item_data_list: List[EventItemData] = []
        for _ in range(self.get_event_item_data_count):
            tmp = EventItemData(data, offset + sz)
            sz += tmp.get_size()
            self.get_event_item_data_list.append(tmp)

        self.discovery_enemy_data_count = decode_int(data, offset + sz)
        sz += INT_OFF

        self.discovery_enemy_data_list: List[DiscoveryEnemyData] = []
        for _ in range(self.discovery_enemy_data_count):
            tmp = DiscoveryEnemyData(data, offset + sz)
            sz += tmp.get_size()
            self.discovery_enemy_data_list.append(tmp)

        self.destroy_boss_data_count = decode_int(data, offset + sz)
        sz += INT_OFF

        self.destroy_boss_data_list: List[DestroyBossData] = []
        for _ in range(self.destroy_boss_data_count):
            tmp = DestroyBossData(data, offset + sz)
            sz += tmp.get_size()
            self.destroy_boss_data_list.append(tmp)

        self.mission_data_count = decode_int(data, offset + sz)
        sz += INT_OFF

        self.mission_data_list: List[MissionData] = []
        for _ in range(self.mission_data_count):
            tmp = MissionData(data, offset + sz)
            sz += tmp.get_size()
            self.mission_data_list.append(tmp)

        self.score_data_count = decode_int(data, offset + sz)
        sz += INT_OFF

        self.score_data_list: List[ScoreData] = []
        for _ in range(self.score_data_count):
            tmp = ScoreData(data, offset + sz)
            sz += tmp.get_size()
            self.score_data_list.append(tmp)

        self._sz = sz

class EntryUserData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        super().__init__(data, offset)
        store_id = decode_str(data, offset + self._sz)
        self.store_id = store_id[0]
        self._sz += store_id[1]

        user_id = decode_str(data, offset + self._sz)
        self.user_id = user_id[0]
        self._sz += user_id[1]

        self.host_flag = decode_byte(data, offset + self._sz)
        self._sz += BYTE_OFF

class MultiPlayStartRequestData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        super().__init__(data, offset)
        room_id = decode_str(data, offset + self._sz)
        self.room_id = room_id[0]
        self._sz += room_id[1]

        self.matching_mode = decode_byte(data, offset + self._sz)
        self._sz += BYTE_OFF

        self.entry_user_data_count = decode_int(data, offset + self._sz)
        self._sz += INT_OFF

        self.entry_user_data_list: List[EntryUserData] = []
        for _ in range(self.entry_user_data_count):
            tmp = EntryUserData(data, offset + self._sz)
            self._sz += tmp.get_size()
            self.entry_user_data_list.append(tmp)

class MultiPlayEndRequestData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        super().__init__(data, offset)
        self.dummy_1 = decode_byte(data, offset + self._sz)
        self._sz += BYTE_OFF
        self.dummy_2 = decode_byte(data, offset + self._sz)
        self._sz += BYTE_OFF
        self.dummy_3 = decode_byte(data, offset + self._sz)
        self._sz += BYTE_OFF

class SalesResourceData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        super().__init__(data, offset)
        self.common_reward_type = decode_short(data, offset + self._sz)
        self._sz += SHORT_OFF
        self.common_reward_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        
        self.property1_property_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.property1_value1 = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.property1_value2 = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        
        self.property2_property_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.property2_value1 = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.property2_value2 = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        
        self.property3_property_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.property3_value1 = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.property3_value2 = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        
        self.property4_property_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.property4_value1 = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.property4_value2 = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
    
    @classmethod
    def from_args(cls, reward_type: int = 0, reward_id: int = 0) -> "SalesResourceData":
        ret = cls(b"\x00" * 54, 0)
        ret.common_reward_type = reward_type # short
        ret.common_reward_id = reward_id # int
        
        return ret

    def make(self) -> bytes:
        ret = b""
        ret += encode_short(self.common_reward_type)
        ret += encode_int(self.common_reward_id)
        
        ret += encode_int(self.property1_property_id)
        ret += encode_int(self.property1_value1)
        ret += encode_int(self.property1_value2)
        
        ret += encode_int(self.property2_property_id)
        ret += encode_int(self.property2_value1)
        ret += encode_int(self.property2_value2)
        
        ret += encode_int(self.property3_property_id)
        ret += encode_int(self.property3_value1)
        ret += encode_int(self.property3_value2)
        
        ret += encode_int(self.property4_property_id)
        ret += encode_int(self.property4_value1)
        ret += encode_int(self.property4_value2)

class ShopResourceSalesData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        super().__init__(data, offset)
        user_shop_resource_id = decode_str(data, offset + self._sz)
        self.user_shop_resource_id = user_shop_resource_id[0]
        self._sz = user_shop_resource_id[1]
        
        discharge_user_id = decode_str(data, offset + self._sz)
        self.discharge_user_id = discharge_user_id[0]
        self._sz = discharge_user_id[1]
        
        self.remaining_num = decode_short(data, offset + self._sz)
        self._sz += SHORT_OFF
        self.purchase_num = decode_short(data, offset + self._sz)
        self._sz += SHORT_OFF
        
        sales_start_date = decode_str(data, offset + self._sz)
        self.sales_start_date = prs_dt(sales_start_date[0])
        self._sz = sales_start_date[1]
        
        sales_resource_data_list = decode_arr_cls(data, offset + self._sz, SalesResourceData)
        self.sales_resource_data_list: List[SalesResourceData] = sales_resource_data_list[0]
        self._sz += sales_resource_data_list[1]

    @classmethod
    def from_args(cls, resource_id: str = "0", discharge_id: str = "0", remaining: int = 0, purchased: int = 0) -> "ShopResourceSalesData":
        ret = cls(b"\x00" * 20, 0)
        ret.user_shop_resource_id = resource_id
        ret.discharge_user_id = discharge_id
        ret.remaining_num = remaining # short
        ret.purchase_num = purchased # short
        ret.sales_start_date = prs_dt()
    
    def make(self) -> bytes:
        ret = encode_str(self.user_shop_resource_id)
        ret += encode_str(self.discharge_user_id)
        ret += encode_short(self.remaining_num)
        ret += encode_short(self.purchase_num)
        ret += encode_str(fmt_dt(self.sales_start_date))
        ret += encode_arr_cls(self.sales_resource_data_list)
        return ret

class YuiMedalShopUserData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        super().__init__(data, offset)
        self.yui_medal_shop_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        
        self.purchase_num = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        
        last_purchase_date = decode_str(data, offset + self._sz)
        self.last_purchase_date = last_purchase_date[0]
        self._sz += last_purchase_date[1]
    
    @classmethod
    def from_args(cls, yui_medal_shop_id: int = 0, purchase_num: int = 0, last_purchase_date: datetime = datetime.fromtimestamp(0)) -> "YuiMedalShopUserData":
        ret = cls(b"\x00" * 20, 0)
        ret.yui_medal_shop_id = yui_medal_shop_id
        ret.purchase_num = purchase_num
        ret.last_purchase_date = last_purchase_date
        return ret
    
    def make(self) -> bytes:
        ret = encode_int(self.yui_medal_shop_id)
        ret += encode_int(self.purchase_num)
        ret += encode_str(fmt_dt(self.last_purchase_date))
        return ret

class GashaMedalShopUserData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        super().__init__(data, offset)
        self.gasha_medal_shop_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        
        self.purchase_num = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
    
    @classmethod
    def from_args(cls, gasha_medal_shop_id: int = 0, purchase_num: int = 0) -> "GashaMedalShopUserData":
        ret = cls(b"\x00" * 20, 0)
        ret.gasha_medal_shop_id = gasha_medal_shop_id
        ret.purchase_num = purchase_num
        return ret
    
    def make(self) -> bytes:
        ret = encode_int(self.gasha_medal_shop_id)
        ret += encode_int(self.purchase_num)
        return ret

class YuiMedalShopData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        super().__init__(data, offset)
        self.yui_medal_shop_id = decode_int(data, offset + self._sz)
        
        name = decode_str(data, offset + self._sz)
        self.name = name[0]
        self._sz += name[1]

        description = decode_str(data, offset + self._sz)
        self.description = description[0]
        self._sz += description[1]
        
        self.selling_yui_medal = decode_short(data, offset + self._sz)
        self._sz += SHORT_OFF
        self.selling_col = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.selling_event_item_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.selling_event_item_num = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.selling_ticket_num = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.purchase_limit = decode_short(data, offset + self._sz)
        self._sz += SHORT_OFF
        self.pick_up_flag = decode_byte(data, offset + self._sz)
        self._sz += BYTE_OFF
        self.product_category = decode_byte(data, offset + self._sz)
        self._sz += BYTE_OFF
        self.sales_type = decode_byte(data, offset + self._sz)
        self._sz += BYTE_OFF
        self.target_days = decode_byte(data, offset + self._sz)
        self._sz += BYTE_OFF
        self.target_hour = decode_byte(data, offset + self._sz)
        self._sz += BYTE_OFF
        self.interval_hour = decode_byte(data, offset + self._sz)
        self._sz += BYTE_OFF
        
        sales_start_date = decode_str(data, offset + self._sz)
        self.sales_start_date = prs_dt(sales_start_date[0])
        self._sz += sales_start_date[1]
        
        sales_end_date = decode_str(data, offset + self._sz)
        self.sales_end_date = prs_dt(sales_end_date[0])
        self._sz += sales_end_date[1]
        
        self.sort = decode_byte(data, offset + self._sz)

    @classmethod
    def from_args(cls, shop_id: int = 0, name: str = "", desc: str = "") -> "YuiMedalShopData":
        ret = cls(b"\x00" * 43, 0)
        ret.yui_medal_shop_id = shop_id
        ret.name = name
        ret.description = desc
        return ret
    
    def make(self) -> bytes:
        ret = encode_int(self.yui_medal_shop_id)
        ret += encode_str(self.name)
        ret += encode_str(self.description)
        ret += encode_short(self.selling_yui_medal)
        ret += encode_int(self.selling_col)
        ret += encode_int(self.selling_event_item_id)
        ret += encode_int(self.selling_event_item_num)
        ret += encode_int(self.selling_ticket_num)
        ret += encode_short(self.purchase_limit)
        ret += encode_byte(self.pick_up_flag)
        ret += encode_byte(self.product_category)
        ret += encode_byte(self.sales_type)
        ret += encode_byte(self.target_days)
        ret += encode_byte(self.target_hour)
        ret += encode_byte(self.interval_hour)
        ret += encode_str(fmt_dt(self.sales_start_date))
        ret += encode_str(fmt_dt(self.sales_end_date))
        ret += encode_byte(self.sort)
        return ret

class YuiMedalShopItemData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        super().__init__(data, offset)
        self.yui_medal_shop_item_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.yui_medal_shop_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.common_reward_type = decode_byte(data, offset + self._sz)
        self._sz += BYTE_OFF
        self.common_reward_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.common_reward_num = decode_short(data, offset + self._sz)
        self._sz += SHORT_OFF
        self.strength = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        
        self.property1_property_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.property1_value1 = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.property1_value2 = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        
        self.property2_property_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.property2_value1 = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.property2_value2 = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        
        self.property3_property_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.property3_value1 = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.property3_value2 = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        
        self.property4_property_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.property4_value1 = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.property4_value2 = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
    
    @classmethod
    def from_args(cls, item_id: int = 0, shop_id: int = 0, reward_type: int = 0, reward_id: int = 0, reward_num: int = 0, strength: int = 0) -> "YuiMedalShopItemData":
        ret = cls(b"\x00" * 67, 0)
        ret.yui_medal_shop_item_id = item_id
        ret.yui_medal_shop_id = shop_id
        ret.common_reward_type = reward_type
        ret.common_reward_id = reward_id
        ret.common_reward_num = reward_num
        ret.strength = strength
        return ret
    
    def make(self) -> bytes:
        ret = encode_int(self.yui_medal_shop_item_id)
        ret += encode_int(self.yui_medal_shop_id)
        ret += encode_byte(self.common_reward_type)
        ret += encode_int(self.common_reward_id)
        ret += encode_short(self.common_reward_num)
        ret += encode_int(self.strength)
        
        ret += encode_int(self.property1_property_id)
        ret += encode_int(self.property1_value1)
        ret += encode_int(self.property1_value2)
        
        ret += encode_int(self.property2_property_id)
        ret += encode_int(self.property2_value1)
        ret += encode_int(self.property2_value2)
        
        ret += encode_int(self.property3_property_id)
        ret += encode_int(self.property3_value1)
        ret += encode_int(self.property3_value2)
        
        ret += encode_int(self.property4_property_id)
        ret += encode_int(self.property4_value1)
        ret += encode_int(self.property4_value2)
        return ret

class GashaMedalShop(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        super().__init__(data, offset)
        self.gasha_medal_shop_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF

        name = decode_str(data, offset + self._sz)
        self.name = name[0]
        self._sz += name[1]

        self.gasha_medal_id = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.use_gasha_medal_num = decode_int(data, offset + self._sz)
        self._sz += INT_OFF
        self.purchase_limit = decode_short(data, offset + self._sz)
        self._sz += SHORT_OFF

        sales_start_date = decode_str(data, offset + self._sz)
        self.sales_start_date = prs_dt(sales_start_date[0])
        self._sz += sales_start_date[1]
        
        sales_end_date = decode_str(data, offset + self._sz)
        self.sales_end_date = prs_dt(sales_end_date[0])
        self._sz += sales_end_date[1]
    
    @classmethod
    def from_args(cls, shop_id: int = 0, name: str = "", medal_id: int = 0, medal_num: int = 0, purchase_limit: int = 0) -> "GashaMedalShop":
        ret = cls(b"\x00" * 26, 0)
        ret.gasha_medal_shop_id = shop_id
        ret.name = name
        ret.gasha_medal_id = medal_id
        ret.use_gasha_medal_num = medal_num
        ret.purchase_limit = purchase_limit
        return ret
    
    def make(self) -> bytes:
        ret = encode_int(self.gasha_medal_shop_id)
        ret += encode_str(self.name)
        ret += encode_int(self.gasha_medal_id)
        ret += encode_int(self.use_gasha_medal_num)
        ret += encode_short(self.purchase_limit)
        ret += encode_str(fmt_dt(self.sales_start_date))
        ret += encode_str(fmt_dt(self.sales_end_date))
        return ret
