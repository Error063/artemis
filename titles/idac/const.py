class IDACConstants():
    GAME_CODE = "SDGT"

    CONFIG_NAME = "idac.yaml"

    VER_IDAC_SEASON_1 = 0
    VER_IDAC_SEASON_2 = 1

    VERSION_STRING = (
        "Initial D THE ARCADE Season 1",
        "Initial D THE ARCADE Season 2",
    )

    @classmethod
    def game_ver_to_string(cls, ver: int):
        return cls.VERSION_STRING[ver]
