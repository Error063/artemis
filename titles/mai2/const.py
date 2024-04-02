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

    VER_MAIMAI = 0
    VER_MAIMAI_PLUS = 1
    VER_MAIMAI_GREEN = 2
    VER_MAIMAI_GREEN_PLUS = 3
    VER_MAIMAI_ORANGE = 4
    VER_MAIMAI_ORANGE_PLUS = 5
    VER_MAIMAI_PINK = 6
    VER_MAIMAI_PINK_PLUS = 7
    VER_MAIMAI_MURASAKI = 8
    VER_MAIMAI_MURASAKI_PLUS = 9
    VER_MAIMAI_MILK = 10
    VER_MAIMAI_MILK_PLUS = 11
    VER_MAIMAI_FINALE = 12

    VER_MAIMAI_DX = 13
    VER_MAIMAI_DX_PLUS = 14
    VER_MAIMAI_DX_SPLASH = 15
    VER_MAIMAI_DX_SPLASH_PLUS = 16
    VER_MAIMAI_DX_UNIVERSE = 17
    VER_MAIMAI_DX_UNIVERSE_PLUS = 18
    VER_MAIMAI_DX_FESTIVAL = 19
    VER_MAIMAI_DX_FESTIVAL_PLUS = 20
    VER_MAIMAI_DX_BUDDIES = 21

    VERSION_STRING = (
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
        "maimai DX",
        "maimai DX PLUS",
        "maimai DX Splash",
        "maimai DX Splash PLUS",
        "maimai DX UNiVERSE",
        "maimai DX UNiVERSE PLUS",
        "maimai DX FESTiVAL",
        "maimai DX FESTiVAL PLUS",
        "maimai DX BUDDiES"
    )

    @classmethod
    def game_ver_to_string(cls, ver: int):
        return cls.VERSION_STRING[ver]
