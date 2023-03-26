from datetime import datetime, timedelta
import json, logging
from typing import Any, Dict
import random

from core.data import Data
from core import CoreConfig
from titles.pokken.config import PokkenConfig
from titles.pokken.proto import jackal_pb2


class PokkenBase:
    def __init__(self, core_cfg: CoreConfig, game_cfg: PokkenConfig) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.version = 0
        self.logger = logging.getLogger("pokken")
        self.data = Data(core_cfg)

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

        settings.money_magnification = 0
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
        user_id = self.data.card.get_user_id_from_card(access_code)

        if user_id is None: # TODO: Toggle auto-register
            user_id = self.data.user.create_user()
            card_id = self.data.card.create_card(user_id, access_code)
            
            self.logger.info(f"Register new card {access_code} (UserId {user_id}, CardId {card_id})")
        
        # TODO: Check for user data. For now just treat ever card-in as a new user

        load_usr = jackal_pb2.LoadUserResponseData()
        load_usr.commidserv_result = 1
        load_usr.load_hash = 1
        load_usr.cardlock_status = False
        load_usr.banapass_id = user_id
        load_usr.access_code = access_code
        load_usr.new_card_flag = True
        load_usr.precedent_release_flag = 0xFFFFFFFF
        load_usr.navi_newbie_flag = True
        load_usr.navi_enable_flag = True
        load_usr.pad_vibrate_flag = True
        load_usr.home_region_code = 0
        load_usr.home_loc_name = ""
        load_usr.pref_code = 0
        load_usr.trainer_name = "Newb" + str(random.randint(1111,999999))
        load_usr.trainer_rank_point = 0
        load_usr.wallet = 0
        load_usr.fight_money = 0
        load_usr.score_point = 0
        load_usr.grade_max_num = 0
        load_usr.total_play_days = 0
        load_usr.play_date_time = 0
        load_usr.lucky_box_fail_num = 0
        load_usr.event_reward_get_flag = 0
        load_usr.rank_pvp_all = 0
        load_usr.rank_pvp_loc = 0
        load_usr.rank_cpu_all = 0
        load_usr.rank_cpu_loc = 0
        load_usr.rank_event = 0
        load_usr.awake_num = 0
        load_usr.use_support_num = 0
        load_usr.rankmatch_flag = 0
        load_usr.title_text_id = 0
        load_usr.title_plate_id = 0
        load_usr.title_decoration_id = 0
        load_usr.navi_trainer = 0
        load_usr.navi_version_id = 0
        load_usr.aid_skill = 0
        load_usr.comment_text_id = 0
        load_usr.comment_word_id = 0
        load_usr.latest_use_pokemon = 0
        load_usr.ex_ko_num = 0
        load_usr.wko_num = 0
        load_usr.timeup_win_num = 0
        load_usr.cool_ko_num = 0
        load_usr.perfect_ko_num = 0
        load_usr.record_flag = 0
        load_usr.site_register_status = 0
        load_usr.continue_num = 0
        load_usr.event_state = 0
        load_usr.event_id = 0
        load_usr.sp_bonus_category_id_1 = 0
        load_usr.sp_bonus_key_value_1 = 0
        load_usr.sp_bonus_category_id_2 = 0
        load_usr.sp_bonus_key_value_2 = 0

        res.load_user.CopyFrom(load_usr)
        return res.SerializeToString()
    
    def handle_set_bnpassid_lock(self, data: jackal_pb2.Request) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.SET_BNPASSID_LOCK
        return res.SerializeToString()

    def handle_save_ingame_log(self, data: jackal_pb2.Request) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.SET_BNPASSID_LOCK
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