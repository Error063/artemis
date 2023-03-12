from datetime import datetime, timedelta
import json
from typing import Any

from core.config import CoreConfig
from titles.pokken.config import PokkenConfig
from titles.pokken.proto import jackal_pb2


class PokkenBase:
    def __init__(self, core_cfg: CoreConfig, game_cfg: PokkenConfig) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = game_cfg
        self.version = 0

    def handle_noop(self, request: Any) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = request.type

        return res.SerializeToString()

    def handle_ping(self, request: jackal_pb2.PingRequestData) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.PING

        return res.SerializeToString()

    def handle_register_pcb(self, request: jackal_pb2.RegisterPcbRequestData) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.REGISTER_PCB

        regist_pcb = jackal_pb2.RegisterPcbResponseData()
        regist_pcb.server_time = int(datetime.now().timestamp() / 1000)
        biwa_setting = {
            "MatchingServer": {
                "host": f"https://{self.game_cfg.server.hostname}",
                "port": self.game_cfg.server.port_matching,
                "url": "SDAK/100/matching",
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

    def handle_save_ads(self, request: jackal_pb2.SaveAdsRequestData) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.SAVE_ADS

        return res.SerializeToString()

    def handle_save_client_log(
        self, request: jackal_pb2.SaveClientLogRequestData
    ) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.SAVE_CLIENT_LOG

        return res.SerializeToString()

    def handle_check_diagnosis(
        self, request: jackal_pb2.CheckDiagnosisRequestData
    ) -> bytes:
        res = jackal_pb2.Response()
        res.result = 1
        res.type = jackal_pb2.MessageType.CHECK_DIAGNOSIS

        return res.SerializeToString()

    def handle_load_client_settings(
        self, request: jackal_pb2.CheckDiagnosisRequestData
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
