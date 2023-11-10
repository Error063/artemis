from typing import Tuple
import struct
import logging

BIGINT_OFF = 16
LONG_OFF = 8
INT_OFF = 4
SHORT_OFF = 2
BYTE_OFF = 1

def decode_num(data: bytes, offset: int, size: int) -> int:
    try:
        return int.from_bytes(data[offset:offset + size], 'big')
    except:
        logging.getLogger('sao').error(f"Failed to parse {data[offset:offset + size]} as BE number of width {size}")
        return 0

def decode_byte(data: bytes, offset: int) -> int:
    return decode_num(data, offset, BYTE_OFF)

def decode_short(data: bytes, offset: int) -> int:
    return decode_num(data, offset, SHORT_OFF)

def decode_int(data: bytes, offset: int) -> int:
    return decode_num(data, offset, INT_OFF)

def decode_long(data: bytes, offset: int) -> int:
    return decode_num(data, offset, LONG_OFF)

def decode_bigint(data: bytes, offset: int) -> int:
    return decode_num(data, offset, BIGINT_OFF)

def decode_str(data: bytes, offset: int) -> Tuple[str, int]:
    try:
        str_len = decode_int(data, offset)
        num_bytes_decoded = INT_OFF + str_len
        str_out = data[offset + INT_OFF:offset + num_bytes_decoded].decode("utf-16-le", errors="replace")
        return (str_out, num_bytes_decoded)
    except:
        logging.getLogger('sao').error(f"Failed to parse {data[offset:]} as string!")
        return ("", 0)

def encode_str(s: str) -> bytes:
    try:
        str_bytes = s.encode("utf-16-le", errors="replace")
        str_len_bytes = struct.pack("!I", len(str_bytes))
        return str_len_bytes + str_bytes
    except:
        logging.getLogger('sao').error(f"Failed to encode {s} as bytes!")
        return b""
    
class BaseHelper:
    def __init__(self, data: bytes, offset: int) -> None:
        pass
    
    def get_size(self) -> int:
        return 0
    
class MaterialCommonRewardUserData(BaseHelper):
    def __init__(self, data: bytes, offset: int) -> None:
        self.common_reward_type = decode_short(data, offset)
        offset += SHORT_OFF

        self.user_common_reward_id = decode_short(data, offset)
    
    def get_size(self) -> int:
        return SHORT_OFF + SHORT_OFF