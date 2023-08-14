from construct import Struct, Int32sl, Padding, Int8sl
from typing import Union

from .base import *

class ADBLookupException(Exception):
    pass

class ADBLookupRequest(ADBBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)
        self.access_code = data[0x20:0x2A].hex()
        company_code, fw_version, self.serial_number = struct.unpack_from("<bbI", data, 0x2A)
        
        try:
            self.company_code = CompanyCodes(company_code)
        except ValueError as e:
            raise ADBLookupException(f"Invalid company code - {e}")
        
        self.fw_version = ReaderFwVer.from_byte(fw_version)


class ADBLookupResponse(ADBBaseResponse):
    def __init__(self, user_id: Union[int, None], game_id: str = "SXXX", store_id: int = 1, keychip_id: str = "A69E01A8888", code: int = 0x06, length: int = 0x30, status: int = 1) -> None:
        super().__init__(code, length, status, game_id, store_id, keychip_id)
        self.user_id = user_id if user_id is not None else -1
        self.portal_reg = PortalRegStatus.NO_REG

    def make(self):
        resp_struct = Struct(
            "user_id" / Int32sl,
            "portal_reg" / Int8sl,
            Padding(11)
        )

        body = resp_struct.build(dict(
            user_id = self.user_id,
            portal_reg = self.portal_reg.value
        ))

        self.head.length = HEADER_SIZE + len(body)
        return self.head.make() + body

class ADBLookupExResponse(ADBBaseResponse):
    def __init__(self, user_id: Union[int, None], game_id: str = "SXXX", store_id: int = 1, keychip_id: str = "A69E01A8888", 
                code: int = 0x10, length: int = 0x130, status: int = 1) -> None:
        super().__init__(code, length, status, game_id, store_id, keychip_id)
        self.user_id = user_id if user_id is not None else -1
        self.portal_reg = PortalRegStatus.NO_REG

    def make(self):
        resp_struct = Struct(
            "user_id" / Int32sl,
            "portal_reg" / Int8sl,
            Padding(3),
            "auth_key" / Int8sl[256],
            "relation1" / Int32sl,
            "relation2" / Int32sl,
        )

        body = resp_struct.build(dict(
            user_id = self.user_id,
            portal_reg = self.portal_reg.value,
            auth_key = [0] * 256,
            relation1 = -1,
            relation2 = -1
        ))

        self.head.length = HEADER_SIZE + len(body)
        return self.head.make() + body
