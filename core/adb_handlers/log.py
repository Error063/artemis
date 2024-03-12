from construct import Struct, Padding, Int8sl
from typing import Final, List

from .base import *
NUM_LOGS: Final[int] = 20
NUM_LEN_LOG_EX: Final[int] = 48

class AmLogEx:
    def __init__(self, data: bytes) -> None:
        self.aime_id, status, self.user_id, self.credit_ct, self.bet_ct, self.won_ct, self.local_time, \
            self.tseq, self.place_id = struct.unpack("<IIQiii4xQiI", data)
        self.status = LogStatus(status)

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
        self.logs: List[AmLogEx] = []

        for x in range(NUM_LOGS):
            self.logs.append(AmLogEx(data[0x20 + (NUM_LEN_LOG_EX * x): 0x50 + (NUM_LEN_LOG_EX * x)]))
        
        self.num_logs = struct.unpack_from("<I", data, 0x03E0)[0]

class ADBLogExResponse(ADBBaseResponse):
    def __init__(self, game_id: str = "SXXX", store_id: int = 1, keychip_id: str = "A69E01A8888", protocol_ver: int = 12423, code: int = 20, length: int = 64, status: int = 1) -> None:
        super().__init__(code, length, status, game_id, store_id, keychip_id, protocol_ver)

    @classmethod
    def from_req(cls, req: ADBHeader) -> "ADBLogExResponse":
        c = cls(req.game_id, req.store_id, req.keychip_id, req.protocol_ver)
        return c
    
    def make(self) -> bytes:
        resp_struct = Struct(
            "log_result" / Int8sl[NUM_LOGS],
            Padding(12)
        )

        body = resp_struct.build(dict(
            log_result = [1] * NUM_LOGS
        ))

        self.head.length = HEADER_SIZE + len(body)
        return self.head.make() + body
