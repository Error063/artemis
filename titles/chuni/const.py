class ChuniConstants():
    GAME_CODE = "SDBT"
    GAME_CODE_NEW = "SDHD"

    CONFIG_NAME = "chuni.yaml"

    VER_CHUNITHM = 0
    VER_CHUNITHM_PLUS = 1
    VER_CHUNITHM_AIR = 2
    VER_CHUNITHM_AIR_PLUS = 3
    VER_CHUNITHM_STAR = 4 
    VER_CHUNITHM_STAR_PLUS = 5
    VER_CHUNITHM_AMAZON = 6
    VER_CHUNITHM_AMAZON_PLUS = 7
    VER_CHUNITHM_CRYSTAL = 8
    VER_CHUNITHM_CRYSTAL_PLUS = 9
    VER_CHUNITHM_PARADISE = 10
    VER_CHUNITHM_NEW = 11
    VER_CHUNITHM_NEW_PLUS = 12

    VERSION_NAMES = ["Chunithm", "Chunithm+", "Chunithm Air", "Chunithm Air+", "Chunithm Star", "Chunithm Star+", "Chunithm Amazon",
    "Chunithm Amazon+", "Chunithm Crystal", "Chunithm Crystal+", "Chunithm Paradise", "Chunithm New!!", "Chunithm New!!+"]

    @classmethod
    def game_ver_to_string(cls, ver: int):
        return cls.VERSION_NAMES[ver]
