from construct import Struct, Int32sl, Padding, Int8sl
from typing import Union

from .base import *

class ADBStatusLogRequest(ADBBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)
        self.aime_id, status = struct.unpack_from("<II", data, 0x20)
        self.status = LogStatus(status)

class ADBLogRequest(ADBBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)
        self.aime_id, status, self.user_id, self.credit_ct, self.bet_ct, self.won_ct = struct.unpack_from("<IIQiii", data, 0x20)
        self.status = LogStatus(status)

class ADBLogExRequest(ADBBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)
        self.aime_id, status, self.user_id, self.credit_ct, self.bet_ct, self.won_ct, self.local_time, \
            self.tseq, self.place_id, self.num_logs = struct.unpack_from("<IIQiii4xQiII", data, 0x20)
        self.status = LogStatus(status)