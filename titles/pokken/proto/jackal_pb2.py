# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: jackal.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0cjackal.proto\x12\x0fjackal.protobuf"\xae\x0b\n\x07Request\x12*\n\x04type\x18\x01 \x02(\x0e\x32\x1c.jackal.protobuf.MessageType\x12.\n\x04noop\x18\x02 \x01(\x0b\x32 .jackal.protobuf.NoopRequestData\x12.\n\x04ping\x18\x03 \x01(\x0b\x32 .jackal.protobuf.PingRequestData\x12=\n\x0cregister_pcb\x18\x04 \x01(\x0b\x32\'.jackal.protobuf.RegisterPcbRequestData\x12\x35\n\x08save_ads\x18\x05 \x01(\x0b\x32#.jackal.protobuf.SaveAdsRequestData\x12\x46\n\x11\x63heck_access_code\x18\x06 \x01(\x0b\x32+.jackal.protobuf.CheckAccessCodeRequestData\x12\x46\n\x11set_bnpassid_lock\x18\x07 \x01(\x0b\x32+.jackal.protobuf.SetBnpassIdLockRequestData\x12\x37\n\tload_user\x18\x08 \x01(\x0b\x32$.jackal.protobuf.LoadUserRequestData\x12\x37\n\tsave_user\x18\n \x01(\x0b\x32$.jackal.protobuf.SaveUserRequestData\x12\x43\n\x0f\x63heck_diagnosis\x18\x0b \x01(\x0b\x32*.jackal.protobuf.CheckDiagnosisRequestData\x12\x42\n\x0fsave_client_log\x18\x0c \x01(\x0b\x32).jackal.protobuf.SaveClientLogRequestData\x12L\n\x14pre_load_information\x18\r \x01(\x0b\x32..jackal.protobuf.PreLoadInformationRequestData\x12\x45\n\x10load_information\x18\x0e \x01(\x0b\x32+.jackal.protobuf.LoadInformationRequestData\x12\x42\n\x0fpre_save_replay\x18\x0f \x01(\x0b\x32).jackal.protobuf.PreSaveReplayRequestData\x12;\n\x0bsave_replay\x18\x10 \x01(\x0b\x32&.jackal.protobuf.SaveReplayRequestData\x12;\n\x0bsave_charge\x18\x11 \x01(\x0b\x32&.jackal.protobuf.SaveChargeRequestData\x12?\n\rcheck_ranking\x18\x12 \x01(\x0b\x32(.jackal.protobuf.CheckRankingRequestData\x12=\n\x0cload_ranking\x18\x13 \x01(\x0b\x32\'.jackal.protobuf.LoadRankingRequestData\x12\x42\n\x0fsave_ingame_log\x18\x14 \x01(\x0b\x32).jackal.protobuf.SaveInGameLogRequestData\x12[\n\x1cpre_load_information_attract\x18\x15 \x01(\x0b\x32\x35.jackal.protobuf.PreLoadInformationAttractRequestData\x12T\n\x18load_information_attract\x18\x16 \x01(\x0b\x32\x32.jackal.protobuf.LoadInformationAttractRequestData\x12L\n\x14load_client_settings\x18\x17 \x01(\x0b\x32..jackal.protobuf.LoadClientSettingsRequestData"\xd4\x0b\n\x08Response\x12*\n\x04type\x18\x01 \x02(\x0e\x32\x1c.jackal.protobuf.MessageType\x12\x0e\n\x06result\x18\x02 \x02(\r\x12/\n\x04noop\x18\x03 \x01(\x0b\x32!.jackal.protobuf.NoopResponseData\x12/\n\x04ping\x18\x04 \x01(\x0b\x32!.jackal.protobuf.PingResponseData\x12>\n\x0cregister_pcb\x18\x05 \x01(\x0b\x32(.jackal.protobuf.RegisterPcbResponseData\x12\x36\n\x08save_ads\x18\x06 \x01(\x0b\x32$.jackal.protobuf.SaveAdsResponseData\x12G\n\x11\x63heck_access_code\x18\x07 \x01(\x0b\x32,.jackal.protobuf.CheckAccessCodeResponseData\x12G\n\x11set_bnpassid_lock\x18\x08 \x01(\x0b\x32,.jackal.protobuf.SetBnpassIdLockResponseData\x12\x38\n\tload_user\x18\t \x01(\x0b\x32%.jackal.protobuf.LoadUserResponseData\x12\x38\n\tsave_user\x18\x0b \x01(\x0b\x32%.jackal.protobuf.SaveUserResponseData\x12\x44\n\x0f\x63heck_diagnosis\x18\x0c \x01(\x0b\x32+.jackal.protobuf.CheckDiagnosisResponseData\x12\x43\n\x0fsave_client_log\x18\r \x01(\x0b\x32*.jackal.protobuf.SaveClientLogResponseData\x12M\n\x14pre_load_information\x18\x0e \x01(\x0b\x32/.jackal.protobuf.PreLoadInformationResponseData\x12\x46\n\x10load_information\x18\x0f \x01(\x0b\x32,.jackal.protobuf.LoadInformationResponseData\x12\x43\n\x0fpre_save_replay\x18\x10 \x01(\x0b\x32*.jackal.protobuf.PreSaveReplayResponseData\x12<\n\x0bsave_replay\x18\x11 \x01(\x0b\x32\'.jackal.protobuf.SaveReplayResponseData\x12<\n\x0bsave_charge\x18\x12 \x01(\x0b\x32\'.jackal.protobuf.SaveChargeResponseData\x12@\n\rcheck_ranking\x18\x13 \x01(\x0b\x32).jackal.protobuf.CheckRankingResponseData\x12>\n\x0cload_ranking\x18\x14 \x01(\x0b\x32(.jackal.protobuf.LoadRankingResponseData\x12\x43\n\x0fsave_ingame_log\x18\x15 \x01(\x0b\x32*.jackal.protobuf.SaveInGameLogResponseData\x12\\\n\x1cpre_load_information_attract\x18\x16 \x01(\x0b\x32\x36.jackal.protobuf.PreLoadInformationAttractResponseData\x12U\n\x18load_information_attract\x18\x17 \x01(\x0b\x32\x33.jackal.protobuf.LoadInformationAttractResponseData\x12M\n\x14load_client_settings\x18\x18 \x01(\x0b\x32/.jackal.protobuf.LoadClientSettingsResponseData"1\n\x0fNoopRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t"\x12\n\x10NoopResponseData"1\n\x0fPingRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t"\x12\n\x10PingResponseData"\xce\x02\n\x16RegisterPcbRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x10\n\x08pcb_type\x18\x02 \x02(\r\x12\x15\n\rlocation_name\x18\x03 \x02(\t\x12\x19\n\x11location_nickname\x18\x04 \x02(\t\x12\x11\n\tpref_code\x18\x05 \x01(\r\x12\r\n\x05\x61\x64\x64r0\x18\x06 \x01(\t\x12\r\n\x05\x61\x64\x64r1\x18\x07 \x01(\t\x12\r\n\x05\x61\x64\x64r2\x18\x08 \x01(\t\x12\r\n\x05\x61\x64\x64r3\x18\t \x01(\t\x12\x0e\n\x06loc_id\x18\n \x02(\t\x12\x14\n\x0c\x63ountry_code\x18\x0b \x02(\t\x12\x13\n\x0bregion_code\x18\x0c \x02(\r\x12\r\n\x05karma\x18\r \x02(\x05\x12\x0f\n\x07game_id\x18\x0e \x02(\t\x12\x10\n\x08game_ver\x18\x0f \x02(\t\x12\x10\n\x08\x64isk_ver\x18\x10 \x02(\t\x12\x12\n\nutc_offset\x18\x11 \x02(\x05"\x85\x01\n\x17RegisterPcbResponseData\x12\x13\n\x0bserver_time\x18\x01 \x02(\r\x12\x15\n\roperate_start\x18\x02 \x01(\t\x12\x13\n\x0boperate_end\x18\x03 \x01(\t\x12\x13\n\x0b\x62np_baseuri\x18\x04 \x01(\t\x12\x14\n\x0c\x62iwa_setting\x18\x05 \x02(\t"\xd7\x02\n\x12SaveAdsRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t\x12\x17\n\x0f\x61\x64s_start_count\x18\x03 \x02(\r\x12\x16\n\x0e\x61\x64s_coin_count\x18\x04 \x02(\r\x12\x19\n\x11\x61\x64s_service_count\x18\x05 \x02(\r\x12\x1a\n\x12\x61\x64s_freeplay_count\x18\x06 \x02(\r\x12\x1a\n\x12\x61\x64s_operation_days\x18\x07 \x02(\r\x12\x1a\n\x12\x61\x64s_power_on_count\x18\x08 \x02(\r\x12\x46\n\rads_play_time\x18\t \x03(\x0b\x32/.jackal.protobuf.SaveAdsRequestData.AdsPlayTime\x1a\x39\n\x0b\x41\x64sPlayTime\x12\x12\n\npokemon_id\x18\x65 \x02(\r\x12\x16\n\x0e\x63harplay_count\x18\x66 \x02(\r"\x15\n\x13SaveAdsResponseData"M\n\x1a\x43heckAccessCodeRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t\x12\x0f\n\x07\x63hip_id\x18\x03 \x02(\t"M\n\x1b\x43heckAccessCodeResponseData\x12\x19\n\x11\x63ommidserv_result\x18\x01 \x02(\r\x12\x13\n\x0b\x61\x63\x63\x65ss_code\x18\x02 \x02(\t"\xa4\x01\n\x1aSetBnpassIdLockRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t\x12\x13\n\x0b\x62\x61napass_id\x18\x03 \x02(\r\x12\x13\n\x0b\x64\x65vice_type\x18\x04 \x02(\r\x12\x0f\n\x07\x63hip_id\x18\x05 \x02(\t\x12\x13\n\x0b\x61\x63\x63\x65ss_code\x18\x06 \x01(\t\x12\x16\n\x0e\x63\x61rd_lock_time\x18\x07 \x02(\r"\x1d\n\x1bSetBnpassIdLockResponseData"\x85\x01\n\x13LoadUserRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t\x12\x13\n\x0b\x64\x65vice_type\x18\x03 \x02(\r\x12\x0f\n\x07\x63hip_id\x18\x04 \x02(\t\x12\x13\n\x0b\x61\x63\x63\x65ss_code\x18\x05 \x01(\t\x12\x13\n\x0b\x63\x61rd_status\x18\x06 \x02(\x08"\xfc\x12\n\x14LoadUserResponseData\x12\x19\n\x11\x63ommidserv_result\x18\x01 \x02(\r\x12\x11\n\tload_hash\x18\x02 \x02(\r\x12\x17\n\x0f\x63\x61rdlock_status\x18\x03 \x02(\x08\x12\x13\n\x0b\x62\x61napass_id\x18\x04 \x02(\r\x12\x13\n\x0b\x61\x63\x63\x65ss_code\x18\x05 \x01(\t\x12\x15\n\rnew_card_flag\x18\x06 \x02(\x08\x12\x1e\n\x16precedent_release_flag\x18\x07 \x02(\r\x12\x18\n\x10navi_newbie_flag\x18\x08 \x02(\x08\x12\x18\n\x10navi_enable_flag\x18\t \x02(\x08\x12\x18\n\x10pad_vibrate_flag\x18\n \x02(\x08\x12\x18\n\x10home_region_code\x18\x0b \x02(\r\x12\x15\n\rhome_loc_name\x18\x0c \x02(\t\x12\x11\n\tpref_code\x18\r \x02(\r\x12\x14\n\x0ctrainer_name\x18\x0e \x01(\t\x12\x1a\n\x12trainer_rank_point\x18\x0f \x02(\r\x12\x0e\n\x06wallet\x18\x10 \x02(\r\x12\x13\n\x0b\x66ight_money\x18\x11 \x02(\r\x12\x13\n\x0bscore_point\x18\x12 \x02(\r\x12\x15\n\rgrade_max_num\x18\x13 \x02(\r\x12\x15\n\rextra_counter\x18\x14 \x01(\r\x12\x1e\n\x16tutorial_progress_flag\x18\x15 \x03(\r\x12\x17\n\x0ftotal_play_days\x18\x16 \x02(\r\x12\x16\n\x0eplay_date_time\x18\x17 \x02(\r\x12\x1a\n\x12lucky_box_fail_num\x18\x18 \x02(\r\x12\x1d\n\x15\x65vent_reward_get_flag\x18\x19 \x02(\r\x12\x14\n\x0crank_pvp_all\x18\x1a \x02(\r\x12\x14\n\x0crank_pvp_loc\x18\x1b \x02(\r\x12\x14\n\x0crank_cpu_all\x18\x1c \x02(\r\x12\x14\n\x0crank_cpu_loc\x18\x1d \x02(\r\x12\x12\n\nrank_event\x18\x1e \x02(\r\x12\x11\n\tawake_num\x18\x1f \x02(\r\x12\x17\n\x0fuse_support_num\x18  \x02(\r\x12\x16\n\x0erankmatch_flag\x18! \x02(\r\x12\x1a\n\x12rankmatch_progress\x18" \x03(\r\x12\x15\n\rrankmatch_max\x18# \x01(\r\x12\x19\n\x11rankmatch_success\x18$ \x01(\r\x12\x10\n\x08\x62\x65\x61t_num\x18% \x01(\x05\x12\x15\n\rtitle_text_id\x18& \x02(\r\x12\x16\n\x0etitle_plate_id\x18\' \x02(\r\x12\x1b\n\x13title_decoration_id\x18( \x02(\r\x12\x1c\n\x14support_pokemon_list\x18) \x03(\r\x12\x15\n\rsupport_set_1\x18* \x03(\r\x12\x15\n\rsupport_set_2\x18+ \x03(\r\x12\x15\n\rsupport_set_3\x18, \x03(\r\x12\x14\n\x0cnavi_trainer\x18- \x02(\r\x12\x17\n\x0fnavi_version_id\x18. \x02(\r\x12\x16\n\x0e\x61id_skill_list\x18/ \x03(\r\x12\x11\n\taid_skill\x18\x30 \x02(\r\x12\x17\n\x0f\x63omment_text_id\x18\x31 \x02(\r\x12\x17\n\x0f\x63omment_word_id\x18\x32 \x02(\r\x12\x1a\n\x12latest_use_pokemon\x18\x33 \x02(\r\x12\x11\n\tex_ko_num\x18\x34 \x02(\r\x12\x0f\n\x07wko_num\x18\x35 \x02(\r\x12\x16\n\x0etimeup_win_num\x18\x36 \x02(\r\x12\x13\n\x0b\x63ool_ko_num\x18\x37 \x02(\r\x12\x16\n\x0eperfect_ko_num\x18\x38 \x02(\r\x12\x13\n\x0brecord_flag\x18\x39 \x02(\r\x12\x1c\n\x14site_register_status\x18: \x02(\r\x12\x14\n\x0c\x63ontinue_num\x18; \x02(\r\x12\x18\n\x10\x61\x63hievement_flag\x18< \x03(\r\x12\x13\n\x0b\x61vatar_body\x18= \x01(\r\x12\x15\n\ravatar_gender\x18> \x01(\r\x12\x19\n\x11\x61vatar_background\x18? \x01(\r\x12\x13\n\x0b\x61vatar_head\x18@ \x01(\r\x12\x1a\n\x12\x61vatar_battleglass\x18\x41 \x01(\r\x12\x14\n\x0c\x61vatar_face0\x18\x42 \x01(\r\x12\x14\n\x0c\x61vatar_face1\x18\x43 \x01(\r\x12\x14\n\x0c\x61vatar_face2\x18\x44 \x01(\r\x12\x16\n\x0e\x61vatar_bodyall\x18\x45 \x01(\r\x12\x13\n\x0b\x61vatar_wear\x18\x46 \x01(\r\x12\x18\n\x10\x61vatar_accessory\x18G \x01(\r\x12\x14\n\x0c\x61vatar_stamp\x18H \x01(\r\x12G\n\x0cpokemon_data\x18I \x03(\x0b\x32\x31.jackal.protobuf.LoadUserResponseData.PokemonData\x12\x13\n\x0b\x65vent_state\x18J \x02(\r\x12\x10\n\x08\x65vent_id\x18K \x02(\r\x12\x1e\n\x16sp_bonus_category_id_1\x18L \x02(\r\x12\x1c\n\x14sp_bonus_key_value_1\x18M \x02(\r\x12\x1e\n\x16sp_bonus_category_id_2\x18N \x02(\r\x12\x1c\n\x14sp_bonus_key_value_2\x18O \x02(\r\x12\x1a\n\x12last_play_event_id\x18P \x01(\r\x12\x1e\n\x16\x65vent_achievement_flag\x18Q \x03(\r\x12\x1f\n\x17\x65vent_achievement_param\x18R \x03(\r\x1a\xf0\x02\n\x0bPokemonData\x12\x0f\n\x07\x63har_id\x18\x65 \x02(\r\x12\x1c\n\x14illustration_book_no\x18\x66 \x02(\r\x12\x13\n\x0bpokemon_exp\x18g \x02(\r\x12\x19\n\x11\x62\x61ttle_num_vs_wan\x18h \x02(\r\x12\x12\n\nwin_vs_wan\x18i \x02(\r\x12\x19\n\x11\x62\x61ttle_num_vs_lan\x18j \x02(\r\x12\x12\n\nwin_vs_lan\x18k \x02(\r\x12\x19\n\x11\x62\x61ttle_num_vs_cpu\x18l \x02(\r\x12\x0f\n\x07win_cpu\x18m \x02(\r\x12\x1f\n\x17\x62\x61ttle_all_num_tutorial\x18n \x02(\r\x12\x1b\n\x13\x62\x61ttle_num_tutorial\x18o \x02(\r\x12\x14\n\x0c\x62p_point_atk\x18p \x02(\r\x12\x14\n\x0c\x62p_point_res\x18q \x02(\r\x12\x14\n\x0c\x62p_point_def\x18r \x02(\r\x12\x13\n\x0b\x62p_point_sp\x18s \x02(\r"\x98\x0c\n\x13SaveUserRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t\x12\x13\n\x0b\x62\x61napass_id\x18\x03 \x02(\r\x12\x1e\n\x16get_trainer_rank_point\x18\x04 \x01(\x05\x12\x11\n\tget_money\x18\x05 \x02(\r\x12\x17\n\x0fget_score_point\x18\x06 \x01(\r\x12\x15\n\rgrade_max_num\x18\x07 \x01(\r\x12\x15\n\rextra_counter\x18\x08 \x01(\r\x12\x1e\n\x16tutorial_progress_flag\x18\t \x03(\r\x12\x1d\n\x15\x65vent_reward_get_flag\x18\n \x01(\r\x12\x14\n\x0c\x63ontinue_num\x18\x0b \x02(\r\x12\x17\n\x0ftotal_play_days\x18\x0c \x02(\r\x12\x18\n\x10\x61\x63hievement_flag\x18\r \x03(\r\x12\x11\n\tawake_num\x18\x0e \x02(\r\x12\x17\n\x0fuse_support_num\x18\x0f \x02(\r\x12\x16\n\x0erankmatch_flag\x18\x10 \x02(\r\x12\x1a\n\x12rank_match_process\x18\x11 \x03(\r\x12\x16\n\x0erank_match_max\x18\x12 \x01(\r\x12\x1a\n\x12rank_match_success\x18\x13 \x01(\r\x12\x10\n\x08\x62\x65\x61t_num\x18\x14 \x01(\x05\x12\x15\n\rsupport_set_1\x18\x15 \x03(\r\x12\x15\n\rsupport_set_2\x18\x16 \x03(\r\x12\x15\n\rsupport_set_3\x18\x17 \x03(\r\x12\x44\n\x0b\x62\x61ttle_data\x18\x18 \x02(\x0b\x32/.jackal.protobuf.SaveUserRequestData.BattleData\x12\x46\n\x0cpokemon_data\x18\x19 \x02(\x0b\x32\x30.jackal.protobuf.SaveUserRequestData.PokemonData\x12\x1c\n\x14trainer_name_pending\x18\x1a \x01(\t\x12\x15\n\ravatar_gender\x18\x1b \x01(\r\x12\x15\n\rcontinue_flag\x18\x1c \x02(\x08\x12\x14\n\x0creq_sendtime\x18\x1d \x02(\r\x12\x15\n\rplay_all_time\x18\x1e \x02(\r\x12\x11\n\tload_hash\x18\x1f \x02(\r\x12\x44\n\x0breward_data\x18  \x03(\x0b\x32/.jackal.protobuf.SaveUserRequestData.RewardData\x12\x13\n\x0b\x65vent_state\x18! \x01(\r\x12\x11\n\taid_skill\x18" \x01(\r\x12\x1a\n\x12last_play_event_id\x18# \x01(\r\x12\x1e\n\x16\x65vent_achievement_flag\x18$ \x03(\r\x12\x1f\n\x17\x65vent_achievement_param\x18% \x03(\r\x1a\xec\x01\n\nBattleData\x12\x11\n\tplay_mode\x18\x65 \x03(\r\x12\x0e\n\x06result\x18\x66 \x03(\r\x12\x11\n\tex_ko_num\x18g \x02(\r\x12\x0f\n\x07wko_num\x18h \x02(\r\x12\x16\n\x0etimeup_win_num\x18i \x02(\r\x12\x13\n\x0b\x63ool_ko_num\x18j \x02(\r\x12\x16\n\x0eperfect_ko_num\x18k \x02(\r\x12\x10\n\x08use_navi\x18l \x02(\r\x12\x16\n\x0euse_navi_cloth\x18m \x02(\r\x12\x15\n\ruse_aid_skill\x18n \x02(\r\x12\x11\n\tplay_date\x18o \x02(\r\x1a\xb3\x01\n\x0bPokemonData\x12\x10\n\x07\x63har_id\x18\xc9\x01 \x02(\r\x12\x1d\n\x14illustration_book_no\x18\xca\x01 \x02(\r\x12\x18\n\x0fget_pokemon_exp\x18\xcb\x01 \x02(\r\x12\x15\n\x0c\x62p_point_atk\x18\xcc\x01 \x02(\r\x12\x15\n\x0c\x62p_point_res\x18\xcd\x01 \x02(\r\x12\x15\n\x0c\x62p_point_def\x18\xce\x01 \x02(\r\x12\x14\n\x0b\x62p_point_sp\x18\xcf\x01 \x02(\r\x1aU\n\nRewardData\x12\x18\n\x0fget_category_id\x18\xad\x02 \x02(\r\x12\x17\n\x0eget_content_id\x18\xae\x02 \x02(\r\x12\x14\n\x0bget_type_id\x18\xaf\x02 \x02(\r"\x16\n\x14SaveUserResponseData";\n\x19\x43heckDiagnosisRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t"\x95\x02\n\x1a\x43heckDiagnosisResponseData\x12Q\n\x0e\x64iagnosis_data\x18\x01 \x03(\x0b\x32\x39.jackal.protobuf.CheckDiagnosisResponseData.DiagnosisData\x1a\xa3\x01\n\rDiagnosisData\x12\x14\n\x0crequest_type\x18\x65 \x02(\r\x12\x17\n\x0f\x63onnect_timeout\x18\x66 \x02(\r\x12\x14\n\x0csend_timeout\x18g \x02(\r\x12\x17\n\x0freceive_timeout\x18h \x02(\r\x12\x1c\n\x14retry_time_of_number\x18i \x02(\r\x12\x16\n\x0eretry_interval\x18j \x02(\r"\xf4\x01\n\x18SaveClientLogRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t\x12\x11\n\tserial_id\x18\x03 \x02(\r\x12\x14\n\x0creq_sendtime\x18\x04 \x02(\r\x12\r\n\x05karma\x18\x05 \x02(\x05\x12\x14\n\x0crequest_type\x18\x06 \x02(\r\x12\x1f\n\x17request_number_of_times\x18\x07 \x02(\r\x12\x1f\n\x17timeout_number_of_times\x18\x08 \x02(\r\x12\x11\n\tretry_max\x18\t \x02(\r\x12\x15\n\rresponse_time\x18\n \x02(\r"\x1b\n\x19SaveClientLogResponseData"V\n\x1dPreLoadInformationRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t\x12\x15\n\rinfo_small_id\x18\x03 \x02(\r"\xc9\x01\n\x1ePreLoadInformationResponseData\x12\x15\n\rinfo_small_id\x18\x01 \x02(\r\x12\x13\n\x0bregion_code\x18\x02 \x02(\r\x12\x12\n\nsession_id\x18\x03 \x02(\r\x12\x13\n\x0b\x62lock_total\x18\x04 \x02(\r\x12\x12\n\nblock_size\x18\x05 \x02(\r\x12\x10\n\x08interval\x18\x06 \x02(\r\x12\x16\n\x0einfo_data_size\x18\x07 \x02(\r\x12\x14\n\x0cinfo_data_id\x18\x08 \x02(\r"v\n\x1aLoadInformationRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t\x12\x15\n\rinfo_small_id\x18\x03 \x02(\r\x12\x12\n\nsession_id\x18\x04 \x02(\r\x12\r\n\x05\x62lock\x18\x05 \x02(\r"\x96\x01\n\x1bLoadInformationResponseData\x12\x15\n\rinfo_small_id\x18\x01 \x02(\r\x12\x12\n\nstart_date\x18\x02 \x02(\r\x12\x10\n\x08\x65nd_date\x18\x03 \x02(\r\x12\r\n\x05\x62lock\x18\x04 \x02(\r\x12\x13\n\x0b\x62lock_total\x18\x05 \x02(\r\x12\x16\n\x0einfo_data_body\x18\x06 \x02(\x0c"\x80\x01\n\x18PreSaveReplayRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t\x12\x13\n\x0bregion_code\x18\x03 \x02(\r\x12\x15\n\rcategory_code\x18\x04 \x02(\r\x12\x18\n\x10replay_data_size\x18\x05 \x02(\r"j\n\x19PreSaveReplayResponseData\x12\x12\n\nsession_id\x18\x01 \x02(\r\x12\x13\n\x0b\x62lock_total\x18\x02 \x02(\r\x12\x12\n\nblock_size\x18\x03 \x02(\r\x12\x10\n\x08interval\x18\x04 \x02(\r"\x82\x02\n\x15SaveReplayRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t\x12\x13\n\x0b\x62\x61napass_id\x18\x03 \x02(\r\x12\x12\n\npokemon_id\x18\x04 \x02(\r\x12\x17\n\x0ftrainer_rank_id\x18\x05 \x02(\r\x12\x13\n\x0bregion_code\x18\x06 \x02(\r\x12\x12\n\nsession_id\x18\x07 \x02(\r\x12\r\n\x05\x62lock\x18\x08 \x02(\r\x12\x1b\n\x13transfer_completion\x18\t \x02(\r\x12\x18\n\x10replay_data_size\x18\n \x02(\r\x12\x18\n\x10replay_data_body\x18\x0b \x02(\x0c"\x18\n\x16SaveReplayResponseData"\x8d\x01\n\x15SaveChargeRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t\x12\x0f\n\x07game_id\x18\x03 \x02(\t\x12\x19\n\x11\x63harge_data_index\x18\x04 \x02(\t\x12\x13\n\x0b\x63harge_type\x18\x05 \x02(\r\x12\x13\n\x0b\x63harge_time\x18\x06 \x02(\r"N\n\x16SaveChargeResponseData\x12\x19\n\x11\x63harge_error_code\x18\x01 \x02(\r\x12\x19\n\x11\x63harge_data_index\x18\x02 \x02(\t"u\n\x17\x43heckRankingRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t\x12\x13\n\x0bregion_code\x18\x03 \x02(\r\x12\x12\n\nranking_id\x18\x04 \x02(\r\x12\x11\n\ttimestamp\x18\x05 \x02(\r".\n\x18\x43heckRankingResponseData\x12\x12\n\nranking_id\x18\x01 \x02(\r"a\n\x16LoadRankingRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t\x12\x13\n\x0bregion_code\x18\x03 \x02(\r\x12\x12\n\nranking_id\x18\x04 \x02(\r"\xbd\x08\n\x17LoadRankingResponseData\x12\x12\n\nranking_id\x18\x01 \x02(\r\x12\x15\n\rranking_start\x18\x02 \x02(\r\x12\x13\n\x0branking_end\x18\x03 \x02(\r\x12\x11\n\tevent_end\x18\x04 \x02(\x08\x12J\n\x0ctrainer_data\x18\x05 \x03(\x0b\x32\x34.jackal.protobuf.LoadRankingResponseData.TrainerData\x12\x13\n\x0bmodify_date\x18\x06 \x02(\r\x12\x13\n\x0b\x65vent_state\x18\x07 \x01(\r\x1a\xd8\x06\n\x0bTrainerData\x12\x14\n\x0ctrainer_name\x18\x65 \x02(\t\x12\x1a\n\x12trainer_rank_point\x18\x66 \x02(\r\x12\r\n\x05point\x18g \x02(\r\x12\x13\n\x0brecord_flag\x18h \x02(\r\x12\x18\n\x10\x66\x61vorite_pokemon\x18i \x02(\r\x12\x12\n\nwin_vs_wan\x18j \x02(\r\x12\x19\n\x11\x62\x61ttle_num_vs_wan\x18k \x02(\r\x12\x12\n\nwin_vs_cpu\x18l \x02(\r\x12\x19\n\x11\x62\x61ttle_num_vs_cpu\x18m \x02(\r\x12\x15\n\rtitle_text_id\x18n \x02(\r\x12\x16\n\x0etitle_plate_id\x18o \x02(\r\x12\x1b\n\x13title_decoration_id\x18p \x02(\r\x12\x17\n\x0f\x63omment_text_id\x18q \x02(\r\x12\x17\n\x0f\x63omment_word_id\x18r \x02(\r\x12\x10\n\x08loc_name\x18s \x02(\t\x12\x11\n\tpref_code\x18t \x02(\r\x12\x10\n\x08rank_num\x18u \x02(\r\x12\x15\n\rlast_rank_num\x18v \x02(\r\x12\x0e\n\x06updown\x18w \x02(\r\x12\x12\n\npokemon_id\x18x \x02(\r\x12\x13\n\x0bpokemon_exp\x18y \x02(\r\x12\x14\n\x0c\x62p_point_atk\x18z \x02(\r\x12\x14\n\x0c\x62p_point_res\x18{ \x02(\r\x12\x14\n\x0c\x62p_point_def\x18| \x02(\r\x12\x13\n\x0b\x62p_point_sp\x18} \x02(\r\x12\x13\n\x0b\x61vatar_body\x18~ \x02(\r\x12\x15\n\ravatar_gender\x18\x7f \x02(\r\x12\x1a\n\x11\x61vatar_background\x18\x80\x01 \x02(\r\x12\x14\n\x0b\x61vatar_head\x18\x81\x01 \x02(\r\x12\x1b\n\x12\x61vatar_battleglass\x18\x82\x01 \x02(\r\x12\x15\n\x0c\x61vatar_face0\x18\x83\x01 \x02(\r\x12\x15\n\x0c\x61vatar_face1\x18\x84\x01 \x02(\r\x12\x15\n\x0c\x61vatar_face2\x18\x85\x01 \x02(\r\x12\x17\n\x0e\x61vatar_bodyall\x18\x86\x01 \x02(\r\x12\x14\n\x0b\x61vatar_wear\x18\x87\x01 \x02(\r\x12\x19\n\x10\x61vatar_accessory\x18\x88\x01 \x02(\r\x12\x15\n\x0c\x61vatar_stamp\x18\x89\x01 \x02(\r"h\n\x18SaveInGameLogRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t\x12\x13\n\x0bin_game_log\x18\x03 \x02(\x0c\x12\x17\n\x0flog_change_time\x18\x04 \x02(\r"\x1b\n\x19SaveInGameLogResponseData"]\n$PreLoadInformationAttractRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t\x12\x15\n\rinfo_large_id\x18\x03 \x02(\r"\xd0\x01\n%PreLoadInformationAttractResponseData\x12\x15\n\rinfo_large_id\x18\x01 \x02(\r\x12\x13\n\x0bregion_code\x18\x02 \x02(\r\x12\x12\n\nsession_id\x18\x03 \x02(\r\x12\x13\n\x0b\x62lock_total\x18\x04 \x02(\r\x12\x12\n\nblock_size\x18\x05 \x02(\r\x12\x10\n\x08interval\x18\x06 \x02(\r\x12\x16\n\x0einfo_data_size\x18\x07 \x02(\r\x12\x14\n\x0cinfo_data_id\x18\x08 \x02(\r"}\n!LoadInformationAttractRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t\x12\x15\n\rinfo_large_id\x18\x03 \x02(\r\x12\x12\n\nsession_id\x18\x04 \x02(\r\x12\r\n\x05\x62lock\x18\x05 \x02(\r"\x9d\x01\n"LoadInformationAttractResponseData\x12\x15\n\rinfo_large_id\x18\x01 \x02(\r\x12\x12\n\nstart_date\x18\x02 \x02(\r\x12\x10\n\x08\x65nd_date\x18\x03 \x02(\r\x12\r\n\x05\x62lock\x18\x04 \x02(\r\x12\x13\n\x0b\x62lock_total\x18\x05 \x02(\r\x12\x16\n\x0einfo_data_body\x18\x06 \x02(\x0c"?\n\x1dLoadClientSettingsRequestData\x12\x0e\n\x06pcb_id\x18\x01 \x02(\t\x12\x0e\n\x06loc_id\x18\x02 \x02(\t"\x8d\x10\n\x1eLoadClientSettingsResponseData\x12\x1b\n\x13money_magnification\x18\x01 \x02(\r\x12!\n\x19\x64m2_probability_single100\x18\x02 \x03(\r\x12\x1a\n\x12\x63ontinue_bonus_exp\x18\x03 \x02(\r\x12\x1c\n\x14\x63ontinue_fight_money\x18\x04 \x02(\r\x12\x17\n\x0f\x65vent_bonus_exp\x18\x05 \x02(\r\x12\x11\n\tlevel_cap\x18\x06 \x02(\r\x12\x15\n\rop_movie_flag\x18\x07 \x02(\r\x12M\n\nevent_info\x18\x08 \x03(\x0b\x32\x39.jackal.protobuf.LoadClientSettingsResponseData.EventInfo\x12O\n\x0b\x62\x61nner_info\x18\t \x03(\x0b\x32:.jackal.protobuf.LoadClientSettingsResponseData.BannerInfo\x12Q\n\x0c\x61ttract_info\x18\n \x03(\x0b\x32;.jackal.protobuf.LoadClientSettingsResponseData.AttractInfo\x12O\n\x0binfo_window\x18\x0b \x03(\x0b\x32:.jackal.protobuf.LoadClientSettingsResponseData.InfoWindow\x12\x18\n\x10lucky_bonus_rate\x18\x0c \x02(\r\x12\x18\n\x10\x66\x61il_support_num\x18\r \x02(\r\x12O\n\x0blucky_bonus\x18\x0e \x03(\x0b\x32:.jackal.protobuf.LoadClientSettingsResponseData.LuckyBonus\x12S\n\rspecial_bonus\x18\x0f \x03(\x0b\x32<.jackal.protobuf.LoadClientSettingsResponseData.SpecialBonus\x12\x17\n\x0f\x63hara_open_flag\x18\x10 \x02(\r\x12\x17\n\x0f\x63hara_open_date\x18\x11 \x02(\r\x12\x1b\n\x13\x63hara_pre_open_date\x18\x12 \x02(\r\x12\x11\n\tsearch_id\x18\x13 \x02(\r\x12\x16\n\x0e\x63lient_version\x18\x14 \x01(\t\x12!\n\x19\x63lient_version_start_date\x18\x15 \x01(\r\x1a\xe0\x01\n\tEventInfo\x12\x13\n\x0b\x65vent_state\x18\x65 \x02(\r\x12\x10\n\x08\x65vent_id\x18\x66 \x02(\r\x12\x1e\n\x16sp_bonus_category_id_1\x18g \x02(\r\x12\x1c\n\x14sp_bonus_key_value_1\x18h \x02(\r\x12\x1e\n\x16sp_bonus_category_id_2\x18i \x02(\r\x12\x1c\n\x14sp_bonus_key_value_2\x18j \x02(\r\x12\x18\n\x10\x65vent_start_date\x18k \x02(\r\x12\x16\n\x0e\x65vent_end_date\x18l \x02(\r\x1a\xa2\x01\n\nBannerInfo\x12\x1a\n\x11\x62\x61nner_start_date\x18\xc9\x01 \x02(\r\x12\x18\n\x0f\x62\x61nner_end_date\x18\xca\x01 \x02(\r\x12\x12\n\tbanner_id\x18\xcb\x01 \x02(\r\x12\x15\n\x0c\x62\x61nner_title\x18\xcc\x01 \x02(\t\x12\x18\n\x0f\x62\x61nner_sub_info\x18\xcd\x01 \x02(\t\x12\x19\n\x10\x62\x61nner_term_info\x18\xce\x01 \x02(\t\x1a\x84\x02\n\x0b\x41ttractInfo\x12 \n\x17\x61ttract_info_start_date\x18\xad\x02 \x02(\r\x12\x1e\n\x15\x61ttract_info_end_date\x18\xae\x02 \x02(\r\x12\x18\n\x0f\x61ttract_info_id\x18\xaf\x02 \x02(\r\x12\x1b\n\x12\x61ttract_info_title\x18\xb0\x02 \x02(\t\x12\x1e\n\x15\x61ttract_info_sub_info\x18\xb1\x02 \x02(\t\x12 \n\x17\x61ttract_info_start_info\x18\xb2\x02 \x02(\t\x12\x1e\n\x15\x61ttract_info_end_info\x18\xb3\x02 \x02(\t\x12\x1a\n\x11\x61ttract_info_text\x18\xb4\x02 \x02(\t\x1a\xfb\x01\n\nInfoWindow\x12\x1f\n\x16info_window_start_date\x18\x91\x03 \x02(\r\x12\x1d\n\x14info_window_end_date\x18\x92\x03 \x02(\r\x12\x17\n\x0einfo_window_id\x18\x93\x03 \x02(\r\x12\x1a\n\x11info_window_title\x18\x94\x03 \x02(\t\x12\x1d\n\x14info_window_sub_info\x18\x95\x03 \x02(\t\x12\x1f\n\x16info_window_start_info\x18\x96\x03 \x02(\t\x12\x1d\n\x14info_window_end_info\x18\x97\x03 \x02(\t\x12\x19\n\x10info_window_text\x18\x98\x03 \x02(\t\x1an\n\nLuckyBonus\x12 \n\x17lucky_bonus_category_id\x18\xf5\x03 \x02(\r\x12\x1c\n\x13lucky_bonus_data_id\x18\xf6\x03 \x02(\r\x12 \n\x17lucky_bonus_probability\x18\xf7\x03 \x02(\r\x1av\n\x0cSpecialBonus\x12"\n\x19special_bonus_category_id\x18\xd9\x04 \x02(\r\x12\x1e\n\x15special_bonus_data_id\x18\xda\x04 \x02(\r\x12"\n\x19special_bonus_probability\x18\xdb\x04 \x02(\r*\xb2\x03\n\x0bMessageType\x12\x08\n\x04NOOP\x10\x00\x12\x08\n\x04PING\x10\x01\x12\x10\n\x0cREGISTER_PCB\x10\x02\x12\x0c\n\x08SAVE_ADS\x10\x03\x12\x15\n\x11\x43HECK_ACCESS_CODE\x10\x04\x12\x15\n\x11SET_BNPASSID_LOCK\x10\x05\x12\r\n\tLOAD_USER\x10\x06\x12\r\n\tSAVE_USER\x10\t\x12\x13\n\x0f\x43HECK_DIAGNOSIS\x10\n\x12\x13\n\x0fSAVE_CLIENT_LOG\x10\x0b\x12\x18\n\x14PRE_LOAD_INFORMATION\x10\x0c\x12\x14\n\x10LOAD_INFORMATION\x10\r\x12\x13\n\x0fPRE_SAVE_REPLAY\x10\x0e\x12\x0f\n\x0bSAVE_REPLAY\x10\x0f\x12\x0f\n\x0bSAVE_CHARGE\x10\x10\x12\x11\n\rCHECK_RANKING\x10\x11\x12\x10\n\x0cLOAD_RANKING\x10\x12\x12\x13\n\x0fSAVE_INGAME_LOG\x10\x13\x12 \n\x1cPRE_LOAD_INFORMATION_ATTRACT\x10\x14\x12\x1c\n\x18LOAD_INFORMATION_ATTRACT\x10\x15\x12\x18\n\x14LOAD_CLIENT_SETTINGS\x10\x16'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "jackal_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _MESSAGETYPE._serialized_start = 14623
    _MESSAGETYPE._serialized_end = 15057
    _REQUEST._serialized_start = 34
    _REQUEST._serialized_end = 1488
    _RESPONSE._serialized_start = 1491
    _RESPONSE._serialized_end = 2983
    _NOOPREQUESTDATA._serialized_start = 2985
    _NOOPREQUESTDATA._serialized_end = 3034
    _NOOPRESPONSEDATA._serialized_start = 3036
    _NOOPRESPONSEDATA._serialized_end = 3054
    _PINGREQUESTDATA._serialized_start = 3056
    _PINGREQUESTDATA._serialized_end = 3105
    _PINGRESPONSEDATA._serialized_start = 3107
    _PINGRESPONSEDATA._serialized_end = 3125
    _REGISTERPCBREQUESTDATA._serialized_start = 3128
    _REGISTERPCBREQUESTDATA._serialized_end = 3462
    _REGISTERPCBRESPONSEDATA._serialized_start = 3465
    _REGISTERPCBRESPONSEDATA._serialized_end = 3598
    _SAVEADSREQUESTDATA._serialized_start = 3601
    _SAVEADSREQUESTDATA._serialized_end = 3944
    _SAVEADSREQUESTDATA_ADSPLAYTIME._serialized_start = 3887
    _SAVEADSREQUESTDATA_ADSPLAYTIME._serialized_end = 3944
    _SAVEADSRESPONSEDATA._serialized_start = 3946
    _SAVEADSRESPONSEDATA._serialized_end = 3967
    _CHECKACCESSCODEREQUESTDATA._serialized_start = 3969
    _CHECKACCESSCODEREQUESTDATA._serialized_end = 4046
    _CHECKACCESSCODERESPONSEDATA._serialized_start = 4048
    _CHECKACCESSCODERESPONSEDATA._serialized_end = 4125
    _SETBNPASSIDLOCKREQUESTDATA._serialized_start = 4128
    _SETBNPASSIDLOCKREQUESTDATA._serialized_end = 4292
    _SETBNPASSIDLOCKRESPONSEDATA._serialized_start = 4294
    _SETBNPASSIDLOCKRESPONSEDATA._serialized_end = 4323
    _LOADUSERREQUESTDATA._serialized_start = 4326
    _LOADUSERREQUESTDATA._serialized_end = 4459
    _LOADUSERRESPONSEDATA._serialized_start = 4462
    _LOADUSERRESPONSEDATA._serialized_end = 6890
    _LOADUSERRESPONSEDATA_POKEMONDATA._serialized_start = 6522
    _LOADUSERRESPONSEDATA_POKEMONDATA._serialized_end = 6890
    _SAVEUSERREQUESTDATA._serialized_start = 6893
    _SAVEUSERREQUESTDATA._serialized_end = 8453
    _SAVEUSERREQUESTDATA_BATTLEDATA._serialized_start = 7948
    _SAVEUSERREQUESTDATA_BATTLEDATA._serialized_end = 8184
    _SAVEUSERREQUESTDATA_POKEMONDATA._serialized_start = 8187
    _SAVEUSERREQUESTDATA_POKEMONDATA._serialized_end = 8366
    _SAVEUSERREQUESTDATA_REWARDDATA._serialized_start = 8368
    _SAVEUSERREQUESTDATA_REWARDDATA._serialized_end = 8453
    _SAVEUSERRESPONSEDATA._serialized_start = 8455
    _SAVEUSERRESPONSEDATA._serialized_end = 8477
    _CHECKDIAGNOSISREQUESTDATA._serialized_start = 8479
    _CHECKDIAGNOSISREQUESTDATA._serialized_end = 8538
    _CHECKDIAGNOSISRESPONSEDATA._serialized_start = 8541
    _CHECKDIAGNOSISRESPONSEDATA._serialized_end = 8818
    _CHECKDIAGNOSISRESPONSEDATA_DIAGNOSISDATA._serialized_start = 8655
    _CHECKDIAGNOSISRESPONSEDATA_DIAGNOSISDATA._serialized_end = 8818
    _SAVECLIENTLOGREQUESTDATA._serialized_start = 8821
    _SAVECLIENTLOGREQUESTDATA._serialized_end = 9065
    _SAVECLIENTLOGRESPONSEDATA._serialized_start = 9067
    _SAVECLIENTLOGRESPONSEDATA._serialized_end = 9094
    _PRELOADINFORMATIONREQUESTDATA._serialized_start = 9096
    _PRELOADINFORMATIONREQUESTDATA._serialized_end = 9182
    _PRELOADINFORMATIONRESPONSEDATA._serialized_start = 9185
    _PRELOADINFORMATIONRESPONSEDATA._serialized_end = 9386
    _LOADINFORMATIONREQUESTDATA._serialized_start = 9388
    _LOADINFORMATIONREQUESTDATA._serialized_end = 9506
    _LOADINFORMATIONRESPONSEDATA._serialized_start = 9509
    _LOADINFORMATIONRESPONSEDATA._serialized_end = 9659
    _PRESAVEREPLAYREQUESTDATA._serialized_start = 9662
    _PRESAVEREPLAYREQUESTDATA._serialized_end = 9790
    _PRESAVEREPLAYRESPONSEDATA._serialized_start = 9792
    _PRESAVEREPLAYRESPONSEDATA._serialized_end = 9898
    _SAVEREPLAYREQUESTDATA._serialized_start = 9901
    _SAVEREPLAYREQUESTDATA._serialized_end = 10159
    _SAVEREPLAYRESPONSEDATA._serialized_start = 10161
    _SAVEREPLAYRESPONSEDATA._serialized_end = 10185
    _SAVECHARGEREQUESTDATA._serialized_start = 10188
    _SAVECHARGEREQUESTDATA._serialized_end = 10329
    _SAVECHARGERESPONSEDATA._serialized_start = 10331
    _SAVECHARGERESPONSEDATA._serialized_end = 10409
    _CHECKRANKINGREQUESTDATA._serialized_start = 10411
    _CHECKRANKINGREQUESTDATA._serialized_end = 10528
    _CHECKRANKINGRESPONSEDATA._serialized_start = 10530
    _CHECKRANKINGRESPONSEDATA._serialized_end = 10576
    _LOADRANKINGREQUESTDATA._serialized_start = 10578
    _LOADRANKINGREQUESTDATA._serialized_end = 10675
    _LOADRANKINGRESPONSEDATA._serialized_start = 10678
    _LOADRANKINGRESPONSEDATA._serialized_end = 11763
    _LOADRANKINGRESPONSEDATA_TRAINERDATA._serialized_start = 10907
    _LOADRANKINGRESPONSEDATA_TRAINERDATA._serialized_end = 11763
    _SAVEINGAMELOGREQUESTDATA._serialized_start = 11765
    _SAVEINGAMELOGREQUESTDATA._serialized_end = 11869
    _SAVEINGAMELOGRESPONSEDATA._serialized_start = 11871
    _SAVEINGAMELOGRESPONSEDATA._serialized_end = 11898
    _PRELOADINFORMATIONATTRACTREQUESTDATA._serialized_start = 11900
    _PRELOADINFORMATIONATTRACTREQUESTDATA._serialized_end = 11993
    _PRELOADINFORMATIONATTRACTRESPONSEDATA._serialized_start = 11996
    _PRELOADINFORMATIONATTRACTRESPONSEDATA._serialized_end = 12204
    _LOADINFORMATIONATTRACTREQUESTDATA._serialized_start = 12206
    _LOADINFORMATIONATTRACTREQUESTDATA._serialized_end = 12331
    _LOADINFORMATIONATTRACTRESPONSEDATA._serialized_start = 12334
    _LOADINFORMATIONATTRACTRESPONSEDATA._serialized_end = 12491
    _LOADCLIENTSETTINGSREQUESTDATA._serialized_start = 12493
    _LOADCLIENTSETTINGSREQUESTDATA._serialized_end = 12556
    _LOADCLIENTSETTINGSRESPONSEDATA._serialized_start = 12559
    _LOADCLIENTSETTINGSRESPONSEDATA._serialized_end = 14620
    _LOADCLIENTSETTINGSRESPONSEDATA_EVENTINFO._serialized_start = 13482
    _LOADCLIENTSETTINGSRESPONSEDATA_EVENTINFO._serialized_end = 13706
    _LOADCLIENTSETTINGSRESPONSEDATA_BANNERINFO._serialized_start = 13709
    _LOADCLIENTSETTINGSRESPONSEDATA_BANNERINFO._serialized_end = 13871
    _LOADCLIENTSETTINGSRESPONSEDATA_ATTRACTINFO._serialized_start = 13874
    _LOADCLIENTSETTINGSRESPONSEDATA_ATTRACTINFO._serialized_end = 14134
    _LOADCLIENTSETTINGSRESPONSEDATA_INFOWINDOW._serialized_start = 14137
    _LOADCLIENTSETTINGSRESPONSEDATA_INFOWINDOW._serialized_end = 14388
    _LOADCLIENTSETTINGSRESPONSEDATA_LUCKYBONUS._serialized_start = 14390
    _LOADCLIENTSETTINGSRESPONSEDATA_LUCKYBONUS._serialized_end = 14500
    _LOADCLIENTSETTINGSRESPONSEDATA_SPECIALBONUS._serialized_start = 14502
    _LOADCLIENTSETTINGSRESPONSEDATA_SPECIALBONUS._serialized_end = 14620
# @@protoc_insertion_point(module_scope)
