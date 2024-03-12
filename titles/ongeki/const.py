from typing import Final, Dict
from enum import Enum


class OngekiConstants:
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

    EVT_TYPES: Enum = Enum(
        "EVT_TYPES",
        [
            "Announcement",
            "Movie",
            "AddMyList",
            "UnlockChapter",
            "JewelEvent",
            "RankingEvent",
            "AcceptRankingEvent",
            "UnlockMusic",
            "UnlockCard",
            "UnlockTrophy",
            "UnlockNamePlate",
            "UnlockLimitBreakItem",
            "MissionEvent",
            "DailyBonus",
            "UnlockBossLockEarly",
            "UnlockPurchaseItem",
            "TechChallengeEvent",
            "AcceptTechChallengeEvent",
            "SilverJewelEvent",
            "Max",
            "None",
        ],
    )

    REWARD_TYPES: Enum = Enum(
        "REWARD_TYPES",
        [
            "Card",
            "NamePlate",
            "Trophy",
            "LimitBreakItem",
            "AlmightyJewel",
            "Money",
            "Music",
            "ProfileVoice",
            "Present",
            "ChapterJewel",
            "GachaTicket",
            "KaikaItem",
            "ExpUpItem",
            "IntimateUpItem",
            "BookItem",
            "SystemVoice",
            "Costume",
            "Medal",
            "Attachment",
            "UnlockItem",
            "Max",
            "None",
        ],
    )

    class CM_GACHA_KINDS(Enum):
        Normal = 0
        Pickup = 1
        BonusRestored = 2
        Free = 3
        PickupBonusRestored = 4

    class RARITY_TYPES(Enum):
        N = 0
        R = 1
        SR = 2
        SSR = 3
        SRPlus = 12

    # The game expects the server to give Lunatic an ID of 10, while the game uses 4 internally... except in Music.xml
    class DIFF_NAME(Enum):
        Basic = 0
        Advanced = 1
        Expert = 2
        Master = 3
        Lunatic = 10

    VERSION_NAMES = (
        "ONGEKI",
        "ONGEKI +",
        "ONGEKI SUMMER",
        "ONGEKI SUMMER +",
        "ONGEKI R.E.D.",
        "ONGEKI R.E.D. +",
        "ONGEKI bright",
        "ONGEKI bright MEMORY",
    )

    @classmethod
    def game_ver_to_string(cls, ver: int):
        return cls.VERSION_NAMES[ver]
