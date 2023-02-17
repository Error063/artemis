class Mai2Constants():
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
        "SSS+": 13
    }
    FC = {
        "None": 0,
        "FC": 1,
        "FC+": 2,
        "AP": 3,
        "AP+": 4
    }
    SYNC = {
        "None": 0,
        "FS": 1,
        "FS+": 2,
        "FDX": 3,
        "FDX+": 4
    }

    DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    GAME_CODE = "SDEZ"

    CONFIG_NAME = "mai2.yaml"

    VER_MAIMAI_DX = 0
    VER_MAIMAI_DX_PLUS = 1
    VER_MAIMAI_DX_SPLASH = 2
    VER_MAIMAI_DX_SPLASH_PLUS = 3
    VER_MAIMAI_DX_UNIVERSE = 4
    VER_MAIMAI_DX_UNIVERSE_PLUS = 5

    VERSION_STRING = ("maimai Delux", "maimai Delux PLUS", "maimai Delux Splash", "maimai Delux Splash PLUS", "maimai Delux Universe",
    "maimai Delux Universe PLUS")

    @classmethod
    def game_ver_to_string(cls, ver: int):
            return cls.VERSION_STRING[ver]