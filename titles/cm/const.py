class CardMakerConstants:
    GAME_CODE = "SDED"

    CONFIG_NAME = "cardmaker.yaml"

    VER_CARD_MAKER = 0
    VER_CARD_MAKER_136 = 1

    VERSION_NAMES = ("Card Maker 1.34", "Card Maker 1.36")

    @classmethod
    def game_ver_to_string(cls, ver: int):
        return cls.VERSION_NAMES[ver]
