from enum import Enum


class PokkenConstants:
    GAME_CODE = "SDAK"

    CONFIG_NAME = "pokken.yaml"

    VER_POKKEN = 0

    VERSION_NAMES = "Pokken Tournament"

    class BATTLE_TYPE(Enum):
        BATTLE_TYPE_TUTORIAL = 1
        BATTLE_TYPE_AI = 2
        BATTLE_TYPE_LAN = 3
        BATTLE_TYPE_WAN = 4

    class BATTLE_RESULT(Enum):
        BATTLE_RESULT_WIN = 1
        BATTLE_RESULT_LOSS = 2

    @classmethod
    def game_ver_to_string(cls, ver: int):
        return cls.VERSION_NAMES[ver]
