import struct
from construct import Struct, Int16ul, Int32ul, PaddedString
from enum import Enum
import re
from typing import Union, Final

class LogStatus(Enum):
    NONE = 0
    START = 1
    CONTINUE = 2
    END = 3
    OTHER = 4

class PortalRegStatus(Enum):
    NO_REG = 0
    PORTAL = 1
    SEGA_ID = 2

class ADBStatus(Enum):
    UNKNOWN = 0
    GOOD = 1
    BAD_AMIE_ID = 2
    ALREADY_REG = 3
    BAN_SYS_USER = 4
    BAN_SYS = 5
    BAN_USER = 6
    BAN_GEN = 7
    LOCK_SYS_USER = 8
    LOCK_SYS = 9
    LOCK_USER = 10

class CompanyCodes(Enum):
    NONE = 0
    SEGA = 1
    BAMCO = 2
    KONAMI = 3
    TAITO = 4

class ReaderFwVer(Enum): # Newer readers use a singly byte value
    NONE = 0
    TN32_10 = 1
    TN32_12 = 2
    OTHER = 9
    
    def __str__(self) -> str:
        if self == self.TN32_10:
            return "TN32MSEC003S F/W Ver1.0"
        elif self == self.TN32_12:
            return "TN32MSEC003S F/W Ver1.2"
        elif self == self.NONE:
            return "Not Specified"
        elif self == self.OTHER:
            return "Unknown/Other"
        else:
            raise ValueError(f"Bad ReaderFwVer value {self.value}")
    
    @classmethod
    def from_byte(self, byte: bytes) -> Union["ReaderFwVer", int]:
        try:
            i = int.from_bytes(byte, 'little')
            try:
                return ReaderFwVer(i)
            except ValueError:
                return i
        except TypeError:
            return 0

class ADBHeaderException(Exception):
    pass

HEADER_SIZE: Final[int] = 0x20
CMD_CODE_GOODBYE: Final[int] = 0x66

# everything is LE
class ADBHeader:
    def __init__(self, magic: int, protocol_ver: int, cmd: int, length: int, status: int, game_id: Union[str, bytes], store_id: int, keychip_id: Union[str, bytes]) -> None:
        self.magic = magic # u16
        self.protocol_ver = protocol_ver # u16
        self.cmd = cmd # u16
        self.length = length # u16
        self.status = ADBStatus(status) # u16
        self.game_id = game_id # 4 char + \x00
        self.store_id = store_id # u32
        self.keychip_id = keychip_id# 11 char + \x00
                
        if type(self.game_id) == bytes:
            self.game_id = self.game_id.decode()
        
        if type(self.keychip_id) == bytes:
            self.keychip_id = self.keychip_id.decode()
        
        self.game_id = self.game_id.replace("\0", "")
        self.keychip_id = self.keychip_id.replace("\0", "")
        if self.cmd != CMD_CODE_GOODBYE: # Games for some reason send no data with goodbye
            self.validate()
    
    @classmethod
    def from_data(cls, data: bytes) -> "ADBHeader":
        magic, protocol_ver, cmd, length, status, game_id, store_id, keychip_id = struct.unpack_from("<5H6sI12s", data)
        head = cls(magic, protocol_ver, cmd, length, status, game_id, store_id, keychip_id)
        
        if head.length != len(data):
            raise ADBHeaderException(f"Length is incorrect! Expect {head.length}, got {len(data)}")
        
        return head
    
    def validate(self) -> bool:
        if self.magic != 0xa13e:
            raise ADBHeaderException(f"Magic {self.magic} != 0xa13e")
        
        if self.protocol_ver < 0x1000:
            raise ADBHeaderException(f"Protocol version {hex(self.protocol_ver)} is invalid!")

        if re.fullmatch(r"^S[0-9A-Z]{3}[P]?$", self.game_id) is None:
            raise ADBHeaderException(f"Game ID {self.game_id} is invalid!")
        
        if self.store_id == 0:
            raise ADBHeaderException(f"Store ID cannot be 0!")

        if re.fullmatch(r"^A[0-9]{2}[E|X][0-9]{2}[A-HJ-NP-Z][0-9]{4}$", self.keychip_id) is None:
            raise ADBHeaderException(f"Keychip ID {self.keychip_id} is invalid!")
        
        return True

    def make(self) -> bytes:
        resp_struct = Struct(
            "magic" / Int16ul,
            "unknown" / Int16ul,
            "response_code" / Int16ul,
            "length" / Int16ul,
            "status" / Int16ul,
            "game_id" / PaddedString(6, 'utf_8'),
            "store_id" / Int32ul,
            "keychip_id" / PaddedString(12, 'utf_8'),
        )

        return resp_struct.build(dict(
            magic=self.magic,
            unknown=self.protocol_ver,
            response_code=self.cmd,
            length=self.length,
            status=self.status.value,
            game_id = self.game_id,
            store_id = self.store_id,
            keychip_id = self.keychip_id,
        ))

class ADBBaseRequest:
    def __init__(self, data: bytes) -> None:
        self.head = ADBHeader.from_data(data)

class ADBBaseResponse:
    def __init__(self, code: int = 0, length: int = 0x20, status: int = 1, game_id: str = "SXXX", store_id: int = 1, keychip_id: str = "A69E01A8888", protocol_ver: int = 0x3087) -> None:
        self.head = ADBHeader(0xa13e, protocol_ver, code, length, status, game_id, store_id, keychip_id)

    @classmethod
    def from_req(cls, req: ADBHeader, cmd: int, length: int = 0x20, status: int = 1) -> "ADBBaseResponse":
        return cls(cmd, length, status, req.game_id, req.store_id, req.keychip_id, req.protocol_ver)

    def append_padding(self, data: bytes):
        """Appends 0s to the end of the data until it's at the correct size"""
        padding_size = self.head.length - len(data)
        data += bytes(padding_size)
        return data

    def make(self) -> bytes:
        return self.head.make()
