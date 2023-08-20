from construct import Struct, Int16ul, Padding, Bytes, Int32ul, Int32sl

from .base import *

class Campaign:
    def __init__(self) -> None:
        self.id = 0
        self.name = ""
        self.announce_date = 0
        self.start_date = 0
        self.end_date = 0
        self.distrib_start_date = 0
        self.distrib_end_date = 0
    
    def make(self) -> bytes:
        name_padding = bytes(128 - len(self.name))
        return Struct(
            "id" / Int32ul,
            "name" / Bytes(128),
            "announce_date" / Int32ul,
            "start_date" / Int32ul,
            "end_date" / Int32ul,
            "distrib_start_date" / Int32ul,
            "distrib_end_date" / Int32ul,
            Padding(8),
        ).build(dict(
            id = self.id,
            name = self.name.encode() + name_padding,
            announce_date = self.announce_date,
            start_date = self.start_date,
            end_date = self.end_date,
            distrib_start_date = self.distrib_start_date,
            distrib_end_date = self.distrib_end_date,
        ))

class CampaignClear:
    def __init__(self) -> None:
        self.id = 0
        self.entry_flag = 0
        self.clear_flag = 0
    
    def make(self) -> bytes:
        return Struct(
            "id" / Int32ul,
            "entry_flag" / Int32ul,
            "clear_flag" / Int32ul,
            Padding(4),
        ).build(dict(
            id = self.id,
            entry_flag = self.entry_flag,
            clear_flag = self.clear_flag,
        ))

class ADBCampaignResponse(ADBBaseResponse):
    def __init__(self, game_id: str = "SXXX", store_id: int = 1, keychip_id: str = "A69E01A8888", code: int = 0x0C, length: int = 0x200, status: int = 1) -> None:
        super().__init__(code, length, status, game_id, store_id, keychip_id)
        self.campaigns = [Campaign(), Campaign(), Campaign()]
    
    @classmethod
    def from_req(cls, req: ADBHeader) -> "ADBCampaignResponse":
        c = cls(req.game_id, req.store_id, req.keychip_id)
        c.head.protocol_ver = req.protocol_ver
        return c

    def make(self) -> bytes:
        body = b""
        
        for c in self.campaigns:
            body += c.make()
        
        self.head.length = HEADER_SIZE + len(body)
        return self.head.make() + body

class ADBOldCampaignRequest(ADBBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)
        self.campaign_id = struct.unpack_from("<I", data, 0x20)

class ADBOldCampaignResponse(ADBBaseResponse):
    def __init__(self, game_id: str = "SXXX", store_id: int = 1, keychip_id: str = "A69E01A8888", code: int = 0x0C, length: int = 0x30, status: int = 1) -> None:
        super().__init__(code, length, status, game_id, store_id, keychip_id)
        self.info0 = 0
        self.info1 = 0
        self.info2 = 0
        self.info3 = 0
    
    @classmethod
    def from_req(cls, req: ADBHeader) -> "ADBCampaignResponse":
        c = cls(req.game_id, req.store_id, req.keychip_id)
        c.head.protocol_ver = req.protocol_ver
        return c
    
    def make(self) -> bytes:
        resp_struct = Struct(
            "info0" / Int32sl,
            "info1" / Int32sl,
            "info2" / Int32sl,
            "info3" / Int32sl,
        ).build(
            info0 = self.info0,
            info1 = self.info1,
            info2 = self.info2,
            info3 = self.info3,
        )

        self.head.length = HEADER_SIZE + len(resp_struct)
        return self.head.make() + resp_struct

class ADBCampaignClearRequest(ADBBaseRequest):
    def __init__(self, data: bytes) -> None:
        super().__init__(data)
        self.aime_id = struct.unpack_from("<i", data, 0x20)

class ADBCampaignClearResponse(ADBBaseResponse):
    def __init__(self, game_id: str = "SXXX", store_id: int = 1, keychip_id: str = "A69E01A8888", code: int = 0x0E, length: int = 0x50, status: int = 1) -> None:
        super().__init__(code, length, status, game_id, store_id, keychip_id)
        self.campaign_clear_status = [CampaignClear(), CampaignClear(), CampaignClear()]
    
    @classmethod
    def from_req(cls, req: ADBHeader) -> "ADBCampaignResponse":
        c = cls(req.game_id, req.store_id, req.keychip_id)
        c.head.protocol_ver = req.protocol_ver
        return c
    
    def make(self) -> bytes:
        body = b""
        
        for c in self.campaign_clear_status:
            body += c.make()
        
        self.head.length = HEADER_SIZE + len(body)
        return self.head.make() + body
