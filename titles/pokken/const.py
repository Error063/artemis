from enum import Enum


class PokkenConstants:
    GAME_CODE = "SDAK"
    GAME_CDS = ["PKF1"]

    CONFIG_NAME = "pokken.yaml"

    VER_POKKEN = 0

    VERSION_NAMES = "Pokken Tournament"

    SERIAL_IDENT = [2747]
    NETID_PREFIX = ["ABGN"]
    SERIAL_REGIONS = [1]
    SERIAL_ROLES = [3]
    SERIAL_CAB_IDENTS = [19]

    class BATTLE_TYPE(Enum):
        TUTORIAL = 1
        AI = 2
        LAN = 3
        WAN = 4
        TUTORIAL_3 = 7

    class BATTLE_RESULT(Enum):
        WIN = 1
        LOSS = 2

    @classmethod
    def game_ver_to_string(cls, ver: int):
        return cls.VERSION_NAMES[ver]
