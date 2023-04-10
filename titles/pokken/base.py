from datetime import datetime, timedelta
import json, logging
from typing import Any, Dict
import random

from core.data import Data
from core import CoreConfig
from .config import PokkenConfig
from .proto import jackal_pb2
from .database import PokkenData


class PokkenBase:
    def __init__(self, core_cfg: CoreConfig, game_cfg: PokkenConfig) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.version = 0
        self.logger = logging.getLogger("pokken")
        self.data = PokkenData(core_cfg)

    def handle_noop(self, request: Any) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = request.type

        return res.SerializeToString()

    def handle_ping(self, request: jackal_pb2.Request) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.PING

        return res.SerializeToString()

    def handle_register_pcb(self, request: jackal_pb2.Request) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.REGISTER_PCB
        self.logger.info(f"Register PCB {request.register_pcb.pcb_id}")

        regist_pcb = jackal_pb2.RegisterPcbResponseData()
        regist_pcb.server_time = int(datetime.now().timestamp())
        biwa_setting = {
            "MatchingServer": {
                "host": f"https://{self.game_cfg.server.hostname}",
                "port": self.game_cfg.server.port,
                "url": "/SDAK/100/matching",
            },
            "StunServer": {
                "addr": self.game_cfg.server.hostname,
                "port": self.game_cfg.server.port_stun,
            },
            "TurnServer": {
                "addr": self.game_cfg.server.hostname,
                "port": self.game_cfg.server.port_turn,
            },
            "AdmissionUrl": f"ws://{self.game_cfg.server.hostname}:{self.game_cfg.server.port_admission}",
            "locationId": 123,
            "logfilename": "JackalMatchingLibrary.log",
            "biwalogfilename": "./biwa.log",
        }
        regist_pcb.bnp_baseuri = f"{self.core_cfg.title.hostname}/bna"
        regist_pcb.biwa_setting = json.dumps(biwa_setting)

        res.register_pcb.CopyFrom(regist_pcb)

        return res.SerializeToString()

    def handle_save_ads(self, request: jackal_pb2.Request) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.SAVE_ADS

        return res.SerializeToString()

    def handle_save_client_log(
        self, request: jackal_pb2.Request
    ) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.SAVE_CLIENT_LOG

        return res.SerializeToString()

    def handle_check_diagnosis(
        self, request: jackal_pb2.Request
    ) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.CHECK_DIAGNOSIS

        return res.SerializeToString()

    def handle_load_client_settings(
        self, request: jackal_pb2.Request
    ) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.LOAD_CLIENT_SETTINGS
        settings = jackal_pb2.LoadClientSettingsResponseData()

        settings.money_magnification = 1
        settings.continue_bonus_exp = 100
        settings.continue_fight_money = 100
        settings.event_bonus_exp = 100
        settings.level_cap = 999
        settings.op_movie_flag = 0xFFFFFFFF
        settings.lucky_bonus_rate = 1
        settings.fail_support_num = 10
        settings.chara_open_flag = 0xFFFFFFFF
        settings.chara_open_date = int(datetime.now().timestamp() / 1000)
        settings.chara_pre_open_date = int(datetime.now().timestamp() / 1000)
        settings.search_id = 123
        res.load_client_settings.CopyFrom(settings)

        return res.SerializeToString()

    def handle_load_ranking(self, request: jackal_pb2.Request) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.LOAD_RANKING
        ranking = jackal_pb2.LoadRankingResponseData()

        ranking.ranking_id = 1
        ranking.ranking_start = 0
        ranking.ranking_end = 1
        ranking.event_end = True
        ranking.modify_date = int(datetime.now().timestamp() / 1000)
        res.load_ranking.CopyFrom(ranking)
        return res.SerializeToString()
    
    def handle_load_user(self, request: jackal_pb2.Request) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.LOAD_USER
        access_code = request.load_user.access_code        
        load_usr = jackal_pb2.LoadUserResponseData()
        user_id = self.data.card.get_user_id_from_card(access_code)

        if user_id is None and self.game_cfg.server.auto_register:
            user_id = self.data.user.create_user()
            card_id = self.data.card.create_card(user_id, access_code)
            
            self.logger.info(f"Register new card {access_code} (UserId {user_id}, CardId {card_id})")
        
        elif user_id is None:
            self.logger.info(f"Registration of card {access_code} blocked!")
            res.load_user.CopyFrom(load_usr)
            return res.SerializeToString()
        
        """ 
        TODO: Add repeated values
        tutorial_progress_flag
        rankmatch_progress
        support_pokemon_list
        support_set_1
        support_set_2
        support_set_3
        aid_skill_list
        achievement_flag
        pokemon_data
        event_achievement_flag
        event_achievement_param
        """
        profile = self.data.profile.get_profile(user_id)
        load_usr.commidserv_result = 1
        load_usr.load_hash = 1
        load_usr.cardlock_status = False
        load_usr.banapass_id = user_id
        load_usr.access_code = access_code        
        load_usr.precedent_release_flag = 0xFFFFFFFF
        
        if profile is None:
            profile_id = self.data.profile.create_profile(user_id)            
            profile_dict = {'id': profile_id, 'user': user_id}
            pokemon_data = []
            tutorial_progress = []
            rankmatch_progress = []
            achievement_flag = []
            event_achievement_flag = []
            event_achievement_param = []
            load_usr.new_card_flag = True
        
        else:
            profile_dict = { k: v for k, v in profile._asdict().items() if v is not None }            
            self.logger.info(f"Card-in user {user_id} (Trainer name {profile_dict.get('trainer_name', '')})")
            pokemon_data = self.data.profile.get_all_pokemon_data(user_id)
            tutorial_progress = []
            rankmatch_progress = []
            achievement_flag = []
            event_achievement_flag = []
            event_achievement_param = []
            load_usr.new_card_flag = False

        load_usr.navi_newbie_flag = profile_dict.get('navi_newbie_flag', True)
        load_usr.navi_enable_flag = profile_dict.get('navi_enable_flag', True)
        load_usr.pad_vibrate_flag = profile_dict.get('pad_vibrate_flag', True)
        load_usr.home_region_code = profile_dict.get('home_region_code', 0)
        load_usr.home_loc_name = profile_dict.get('home_loc_name', "")
        load_usr.pref_code = profile_dict.get('pref_code', 0)
        load_usr.trainer_name = profile_dict.get('trainer_name', "Newb" + str(random.randint(1111,999999))) 
        load_usr.trainer_rank_point = profile_dict.get('trainer_rank_point', 0)
        load_usr.wallet = profile_dict.get('wallet', 0)
        load_usr.fight_money = profile_dict.get('fight_money', 0)
        load_usr.score_point = profile_dict.get('score_point', 0)
        load_usr.grade_max_num = profile_dict.get('grade_max_num', 0)
        load_usr.extra_counter = profile_dict.get('extra_counter', 0)
        load_usr.total_play_days = profile_dict.get('total_play_days', 0)
        load_usr.play_date_time = profile_dict.get('play_date_time', 0)
        load_usr.lucky_box_fail_num = profile_dict.get('lucky_box_fail_num', 0)
        load_usr.event_reward_get_flag = profile_dict.get('event_reward_get_flag', 0)
        load_usr.rank_pvp_all = profile_dict.get('rank_pvp_all', 0)
        load_usr.rank_pvp_loc = profile_dict.get('rank_pvp_loc', 0)
        load_usr.rank_cpu_all = profile_dict.get('rank_cpu_all', 0)
        load_usr.rank_cpu_loc = profile_dict.get('rank_cpu_loc', 0)
        load_usr.rank_event = profile_dict.get('rank_event', 0)
        load_usr.awake_num = profile_dict.get('awake_num', 0)
        load_usr.use_support_num = profile_dict.get('use_support_num', 0)
        load_usr.rankmatch_flag = profile_dict.get('rankmatch_flag', 0)
        load_usr.rankmatch_max = profile_dict.get('rankmatch_max', 0)
        load_usr.rankmatch_success = profile_dict.get('rankmatch_success', 0)
        load_usr.beat_num = profile_dict.get('beat_num', 0)
        load_usr.title_text_id = profile_dict.get('title_text_id', 0)
        load_usr.title_plate_id = profile_dict.get('title_plate_id', 0)
        load_usr.title_decoration_id = profile_dict.get('title_decoration_id', 0)
        load_usr.navi_trainer = profile_dict.get('navi_trainer', 0)
        load_usr.navi_version_id = profile_dict.get('navi_version_id', 0)
        load_usr.aid_skill = profile_dict.get('aid_skill', 0)
        load_usr.comment_text_id = profile_dict.get('comment_text_id', 0)
        load_usr.comment_word_id = profile_dict.get('comment_word_id', 0)
        load_usr.latest_use_pokemon = profile_dict.get('latest_use_pokemon', 0)
        load_usr.ex_ko_num = profile_dict.get('ex_ko_num', 0)
        load_usr.wko_num = profile_dict.get('wko_num', 0)
        load_usr.timeup_win_num = profile_dict.get('timeup_win_num', 0)
        load_usr.cool_ko_num = profile_dict.get('cool_ko_num', 0)
        load_usr.perfect_ko_num = profile_dict.get('perfect_ko_num', 0)
        load_usr.record_flag = profile_dict.get('record_flag', 0)
        load_usr.site_register_status = profile_dict.get('site_register_status', 0)
        load_usr.continue_num = profile_dict.get('continue_num', 0)

        load_usr.avatar_body = profile_dict.get('avatar_body', 0)
        load_usr.avatar_gender = profile_dict.get('avatar_gender', 0)
        load_usr.avatar_background = profile_dict.get('avatar_background', 0)
        load_usr.avatar_head = profile_dict.get('avatar_head', 0)
        load_usr.avatar_battleglass = profile_dict.get('avatar_battleglass', 0)
        load_usr.avatar_face0 = profile_dict.get('avatar_face0', 0)
        load_usr.avatar_face1 = profile_dict.get('avatar_face1', 0)
        load_usr.avatar_face2 = profile_dict.get('avatar_face2', 0)
        load_usr.avatar_bodyall = profile_dict.get('avatar_bodyall', 0)
        load_usr.avatar_wear = profile_dict.get('avatar_wear', 0)
        load_usr.avatar_accessory = profile_dict.get('avatar_accessory', 0)
        load_usr.avatar_stamp = profile_dict.get('avatar_stamp', 0)

        load_usr.event_state = profile_dict.get('event_state', 0)
        load_usr.event_id = profile_dict.get('event_id', 0)
        load_usr.sp_bonus_category_id_1 = profile_dict.get('sp_bonus_category_id_1', 0)
        load_usr.sp_bonus_key_value_1 = profile_dict.get('sp_bonus_key_value_1', 0)
        load_usr.sp_bonus_category_id_2 = profile_dict.get('sp_bonus_category_id_2', 0)
        load_usr.sp_bonus_key_value_2 = profile_dict.get('sp_bonus_key_value_2', 0)
        load_usr.last_play_event_id = profile_dict.get('last_play_event_id', 0)

        res.load_user.CopyFrom(load_usr)
        return res.SerializeToString()
    
    def handle_set_bnpassid_lock(self, data: jackal_pb2.Request) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.SET_BNPASSID_LOCK
        return res.SerializeToString()

    def handle_save_user(self, request: jackal_pb2.Request) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.SAVE_USER

        return res.SerializeToString()

    def handle_save_ingame_log(self, data: jackal_pb2.Request) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.SAVE_INGAME_LOG
        return res.SerializeToString()

    def handle_matching_noop(self, data: Dict = {}, client_ip: str = "127.0.0.1") -> Dict:
        return {}
    
    def handle_matching_start_matching(self, data: Dict = {}, client_ip: str = "127.0.0.1") -> Dict:
        return {}

    def handle_matching_is_matching(self, data: Dict = {}, client_ip: str = "127.0.0.1") -> Dict:
        """
        "sessionId":"12345678",
                "A":{
                    "pcb_id": data["data"]["must"]["pcb_id"],
                    "gip": client_ip
                }, 
                "list":[]
        """
        return {}
    
    def handle_matching_stop_matching(self, data: Dict = {}, client_ip: str = "127.0.0.1") -> Dict:
        return {}