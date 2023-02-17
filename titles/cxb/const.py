class CxbConstants():
    GAME_CODE = "SDCA"

    CONFIG_NAME = "cxb.yaml"

    VER_CROSSBEATS_REV = 0
    VER_CROSSBEATS_REV_SUNRISE_S1 = 1
    VER_CROSSBEATS_REV_SUNRISE_S2 = 2
    VER_CROSSBEATS_REV_SUNRISE_S2_OMNI = 3

    VERSION_NAMES = ("crossbeats REV.", "crossbeats REV. SUNRISE", "crossbeats REV. SUNRISE S2", "crossbeats REV. SUNRISE S2 Omnimix")

    @classmethod
    def game_ver_to_string(cls, ver: int):
        return cls.VERSION_NAMES[ver]