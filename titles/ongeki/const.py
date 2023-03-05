from typing import Final, Dict
from enum import Enum
class OngekiConstants():
    GAME_CODE = "SDDT"

    CONFIG_NAME = "ongeki.yaml"

    VER_ONGEKI = 0
    VER_ONGEKI_PLUS = 1
    VER_ONGEKI_SUMMER = 2
    VER_ONGEKI_SUMMER_PLUS = 3
    VER_ONGEKI_RED = 4
    VER_ONGEKI_RED_PLUS = 5
    VER_ONGEKI_BRIGHT = 6
    VER_ONGEKI_BRIGHT_MEMORY = 7

    EVT_TYPES: Enum = Enum('EVT_TYPES', [
        'None',
        'Announcement',
        'Movie',
        'AddMyList',
        'UnlockChapter',
        'JewelEvent',
        'RankingEvent',
        'AcceptRankingEvent',
        'UnlockMusic',
        'UnlockCard',
        'UnlockTrophy',
        'UnlockNamePlate',
        'UnlockLimitBreakItem',
        'MissionEvent',
        'DailyBonus',
        'UnlockBossLockEarly',
        'UnlockPurchaseItem',
        'TechChallengeEvent',
        'AcceptTechChallengeEvent',
        'SilverJewelEvent',
    ])

    # The game expects the server to give Lunatic an ID of 10, while the game uses 4 internally... except in Music.xml
    class DIFF_NAME(Enum):
        Basic = 0
        Advanced = 1
        Expert = 2
        Master = 3
        Lunatic = 10

    VERSION_NAMES = ("ONGEKI", "ONGEKI+", "ONGEKI Summer", "ONGEKI Summer+", "ONGEKI Red", "ONGEKI Red+", 
        "ONGEKI Bright", "ONGEKI Bright Memory")

    @classmethod
    def game_ver_to_string(cls, ver: int):
        return cls.VERSION_NAMES[ver]