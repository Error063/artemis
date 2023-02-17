class PokkenConstants():
    GAME_CODE = "SDAK"

    CONFIG_NAME = "pokken.yaml"

    VER_POKKEN = 0

    VERSION_NAMES = ("Pokken Tournament")

    @classmethod
    def game_ver_to_string(cls, ver: int):
        return cls.VERSION_NAMES[ver]