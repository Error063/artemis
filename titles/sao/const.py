from enum import Enum


class SaoConstants:
    GAME_CODE = "SDEW"
    GAME_CDS = ["SAO1"]

    CONFIG_NAME = "sao.yaml"

    VER_SAO = 0

    VERSION_NAMES = ("Sword Art Online Arcade")
    
    SERIAL_IDENT_SATALITE = 4
    SERIAL_IDENT_TERMINAL = 5

    SERIAL_IDENT = [2825]
    NETID_PREFIX = ["ABLN"]
    SERIAL_REGIONS = [1]
    SERIAL_ROLES = [3]
    SERIAL_CAB_IDENTS = [SERIAL_IDENT_SATALITE, SERIAL_IDENT_TERMINAL]

    @classmethod
    def game_ver_to_string(cls, ver: int):
        return cls.VERSION_NAMES[ver]
