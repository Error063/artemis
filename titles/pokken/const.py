from enum import Enum


class PokkenConstants:
    GAME_CODE = "SDAK"

    CONFIG_NAME = "pokken.yaml"

    VER_POKKEN = 0

    VERSION_NAMES = "Pokken Tournament"

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
