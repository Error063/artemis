class CardMakerConstants():
    GAME_CODE = "SDED"

    VER_CARD_MAKER = 0

    VERSION_NAMES = ["Card Maker 1.34"]

    @classmethod
    def game_ver_to_string(cls, ver: int):
        return cls.VERSION_NAMES[ver]
