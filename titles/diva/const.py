class DivaConstants():
    GAME_CODE = "SBZV"

    VER_PROJECT_DIVA_ARCADE = 0
    VER_PROJECT_DIVA_ARCADE_FUTURE_TONE = 1

    VERSION_NAMES = ("Project Diva Arcade", "Project Diva Arcade Future Tone")

    @classmethod
    def game_ver_to_string(cls, ver: int):
        return cls.VERSION_NAMES[ver]