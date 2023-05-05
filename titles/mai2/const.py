class Mai2Constants:
    GRADE = {
        "D": 0,
        "C": 1,
        "B": 2,
        "BB": 3,
        "BBB": 4,
        "A": 5,
        "AA": 6,
        "AAA": 7,
        "S": 8,
        "S+": 9,
        "SS": 10,
        "SS+": 11,
        "SSS": 12,
        "SSS+": 13,
    }
    FC = {"None": 0, "FC": 1, "FC+": 2, "AP": 3, "AP+": 4}
    SYNC = {"None": 0, "FS": 1, "FS+": 2, "FDX": 3, "FDX+": 4}

    DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    GAME_CODE = "SBXL"    
    GAME_CODE_GREEN = "SBZF"    
    GAME_CODE_ORANGE = "SDBM"    
    GAME_CODE_PINK = "SDCQ"    
    GAME_CODE_MURASAKI = "SDDK"    
    GAME_CODE_MILK = "SDDZ"    
    GAME_CODE_FINALE = "SDEY"    
    GAME_CODE_DX = "SDEZ"

    CONFIG_NAME = "mai2.yaml"

    VER_MAIMAI = 1000
    VER_MAIMAI_PLUS = 1001
    VER_MAIMAI_GREEN = 1002
    VER_MAIMAI_GREEN_PLUS = 1003
    VER_MAIMAI_ORANGE = 1004
    VER_MAIMAI_ORANGE_PLUS = 1005
    VER_MAIMAI_PINK = 1006
    VER_MAIMAI_PINK_PLUS = 1007
    VER_MAIMAI_MURASAKI = 1008
    VER_MAIMAI_MURASAKI_PLUS = 1009
    VER_MAIMAI_MILK = 1010
    VER_MAIMAI_MILK_PLUS = 1011
    VER_MAIMAI_FINALE = 1012

    VER_MAIMAI_DX = 0
    VER_MAIMAI_DX_PLUS = 1
    VER_MAIMAI_DX_SPLASH = 2
    VER_MAIMAI_DX_SPLASH_PLUS = 3
    VER_MAIMAI_DX_UNIVERSE = 4
    VER_MAIMAI_DX_UNIVERSE_PLUS = 5
    VER_MAIMAI_DX_FESTIVAL = 6

    VERSION_STRING = (
        "maimai DX",
        "maimai DX PLUS",
        "maimai DX Splash",
        "maimai DX Splash PLUS",
        "maimai DX Universe",
        "maimai DX Universe PLUS",
        "maimai DX Festival",
    )

    VERSION_STRING_OLD = (
        "maimai",
        "maimai PLUS",
        "maimai GreeN",
        "maimai GreeN PLUS",
        "maimai ORANGE",
        "maimai ORANGE PLUS",
        "maimai PiNK",
        "maimai PiNK PLUS",
        "maimai MURASAKi",
        "maimai MURASAKi PLUS",
        "maimai MiLK",
        "maimai MiLK PLUS",
        "maimai FiNALE",
    )

    @classmethod
    def game_ver_to_string(cls, ver: int):
        if ver >= 1000:
            return cls.VERSION_STRING_OLD[ver - 1000]
        return cls.VERSION_STRING[ver]
