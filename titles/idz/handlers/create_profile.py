import json
import struct
from datetime import datetime

from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig

class IDZHandlerCreateProfile(IDZHandlerBase):
    cmd_codes = [0x0066, 0x0066, 0x0064, 0x0064]
    rsp_codes = [0x0067, 0x0065, 0x0065, 0x0065]
    name = "create_profile"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0020
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)

        aime_id = struct.unpack_from("<L", data, 0x04)[0]
        name = data[0x1E:0x0034].decode("shift-jis").replace("\x00", "")
        car = data[0x40:0xa0].hex()
        chara = data[0xa8:0xbc].hex()

        self.logger.info(f"Create profile for {name} (aime id {aime_id})")

        auto_team = None
        if not auto_team:
            team = {
                "bg": 0,
                "id": 0,
                "shop": ""
            }
        else:
            tdata = json.loads(auto_team["data"])
            
            team = {
                "bg": tdata["bg"],
                "id": tdata["fx"],
                "shop": ""
            }

        profile_data={
            "profile": {
                "xp": 0,
                "lv": 1,
                "fame": 0,
                "dpoint": 0,
                "milage": 0,
                "playstamps": 0,
                "last_login": int(datetime.now().timestamp()),
                "car_str": car, # These should probably be chaged to dicts
                "chara_str": chara, # But this works for now...
            },

            "options": {
                "music": 0,
                "pack": 13640,
                "aura": 0,
                "paper_cup": 0,
                "gauges": 5,
                "driving_style": 0
            },

            "missions": {
                "team": [],
                "solo": []
            },

            "story": {
                "x": 0,
                "y": 0,
                "rows": {}
            },

            "unlocks": {
                "auras": 1,
                "cup": 0,
                "gauges": 32,
                "music": 0,
                "last_mileage_reward": 0,
            },
            "team": team
        }
        
        if self.version > 2:
            struct.pack_into("<L", ret, 0x04, aime_id)
        else:
            struct.pack_into("<L", ret, 0x08, aime_id)
        return ret
