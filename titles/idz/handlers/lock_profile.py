import struct
from typing import Dict
from datetime import datetime, timedelta

from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig
from ..const import IDZConstants

class IDZHandlerLockProfile(IDZHandlerBase):
    cmd_codes = [0x0069, 0x0069, 0x0065, 0x0065]
    rsp_codes = [0x006a, 0x006a, 0x0066, 0x0066]
    name = "lock_profile"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0020
    
    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        profile_data = {
            "status": IDZConstants.PROFILE_STATUS.UNLOCKED.value, 
            "expire_time": int((datetime.now() + timedelta(hours=1)).timestamp() / 1000)
        }
        user_id = struct.unpack_from("<I", data, 0x04)[0]
        profile = None

        if profile is None and self.version > 0:
            old_profile = None
            if old_profile is not None:
                profile_data["status"] = IDZConstants.PROFILE_STATUS.OLD.value
        
        return self.handle_common(profile_data, ret)
    
    def handle_common(cls, data: Dict, ret: bytearray) -> bytearray:
        struct.pack_into("<B", ret, 0x18, data["status"])
        struct.pack_into("<h", ret, 0x1a, -1)
        struct.pack_into("<I", ret, 0x1c, data["expire_time"])
        return ret
