from typing import Tuple, List
import struct
import logging

BIGINT_OFF = 16
LONG_OFF = 8
INT_OFF = 4
SHORT_OFF = 2
BYTE_OFF = 1

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

def encode_byte(data: int) -> bytes:
    return struct.pack("!B", data)

def encode_short(data: int) -> bytes:
    return struct.pack("!H", data)

def encode_int(data: int) -> bytes:
    return struct.pack("!I", data)

def encode_long(data: int) -> bytes:
    return struct.pack("!L", data)

def encode_bigint(data: int) -> bytes:
    return struct.pack("!Q", data)

def encode_str(s: str) -> bytes:
    try:
        str_bytes = s.encode("utf-16-le", errors="replace")
        str_len_bytes = struct.pack("!I", len(str_bytes))
        return str_len_bytes + str_bytes
    except:
        logging.getLogger('sao').error(f"Failed to encode {s} as bytes!")
        return b""
    
class BaseHelper:
    def __init__(self, data: bytes, offset: int) -> None:
        self._sz = 0
    
    def get_size(self) -> int:
        return self._sz
    
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
