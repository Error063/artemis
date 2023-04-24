from enum import Enum


class IDZConstants:
    GAME_CODE = "SDDF"

    CONFIG_NAME = "idz.yaml"

    VER_IDZ_110 = 0
    VER_IDZ_130 = 1
    VER_IDZ_210 = 2
    VER_IDZ_230 = 3
    NUM_VERS = 4

    VERSION_NAMES = (
        "Initial D Arcade Stage Zero v1.10",
        "Initial D Arcade Stage Zero v1.30",
        "Initial D Arcade Stage Zero v2.10",
        "Initial D Arcade Stage Zero v2.30",
    )

    class PROFILE_STATUS(Enum):
        LOCKED = 0
        UNLOCKED = 1
        OLD = 2

    HASH_LUT = [
        # No clue
        0x9C82E674,
        0x5A4738D9,
        0x8B8D7AE0,
        0x29EC9D81,
        # These three are from AES TE0
        0x1209091B,
        0x1D83839E,
        0x582C2C74,
        0x341A1A2E,
        0x361B1B2D,
        0xDC6E6EB2,
        0xB45A5AEE,
        0x5BA0A0FB,
        0xA45252F6,
        0x763B3B4D,
        0xB7D6D661,
        0x7DB3B3CE,
    ]
    HASH_NUM = 0
    HASH_MUL = [5, 7, 11, 12][HASH_NUM]
    HASH_XOR = [0xB3, 0x8C, 0x14, 0x50][HASH_NUM]

    @classmethod
    def game_ver_to_string(cls, ver: int):
        return cls.VERSION_NAMES[ver]
