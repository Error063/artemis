from enum import Enum


class SaoConstants:
    GAME_CODE = "SDEW"

    CONFIG_NAME = "sao.yaml"

    VER_SAO = 0

    VERSION_NAMES = ("Sword Art Online Arcade")

    @classmethod
    def game_ver_to_string(cls, ver: int):
        return cls.VERSION_NAMES[ver]
