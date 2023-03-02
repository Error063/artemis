from enum import Enum

class WaccaConstants():
    CONFIG_NAME = "wacca.yaml"
    GAME_CODE = "SDFE"

    VER_WACCA = 0
    VER_WACCA_S = 1
    VER_WACCA_LILY = 2
    VER_WACCA_LILY_R = 3
    VER_WACCA_REVERSE = 4

    VERSION_NAMES = ("WACCA", "WACCA S", "WACCA Lily", "WACCA Lily R", "WACCA Reverse")

    class GRADES(Enum):
        D = 1
        C = 2
        B = 3
        A = 4
        AA = 5
        AAA = 6
        S = 7
        SS = 8
        SSS = 9
        MASTER = 10
        S_PLUS = 11
        SS_PLUS = 12
        SSS_PLUS = 13

    ITEM_TYPES = {
        "xp": 1,
        "wp": 2,
        "music_unlock": 3,
        "music_difficulty_unlock": 4,
        "title": 5,
        "icon": 6,
        "trophy": 7,
        "skill": 8,
        "ticket": 9,
        "note_color": 10,
        "note_sound": 11,
        "baht_do_not_send": 12,
        "boost_badge": 13,
        "gate_point": 14,
        "navigator": 15,
        "user_plate": 16,
        "touch_effect": 17,
    }

    OPTIONS = {
        "note_speed": 1, # 1.0 - 6.0
        "field_mask": 2, # 0-4
        "note_sound": 3, # ID
        "note_color": 4, # ID
        "bgm_volume": 5, # 0-100 incremements of 10
        "bg_video": 7, # ask, on, or off

        "mirror": 101, # none or left+right swap
        "judge_display_pos": 102, # center, under, over, top or off
        "judge_detail_display": 103, # on or off
        "measure_guidelines": 105, # on or off
        "guideline_mask": 106, # 0 - 5
        "judge_line_timing_adjust": 108, # -10 - 10
        "note_design": 110, # 1 - 5
        "bonus_effect": 114, # on or off
        "chara_voice": 115, # "usually" or none
        "score_display_method": 116, # add or subtract
        "give_up": 117, # off, no touch, can't achieve s, ss, sss, pb
        "guideline_spacing": 118, # none, or a-g type
        "center_display": 119, # none, combo, score add, score sub, s ss sss pb boarder
        "ranking_display": 120, # on or off
        "stage_up_icon_display": 121, # on or off
        "rating_display": 122, # on or off
        "player_level_display": 123, # on or off
        "touch_effect": 124, # on or off
        "guide_sound_vol": 125, # 0-100 incremements of 10
        "touch_note_vol": 126, # 0-100 incremements of 10
        "hold_note_vol": 127, # 0-100 incremements of 10
        "slide_note_vol": 128, # 0-100 incremements of 10
        "snap_note_vol": 129, # 0-100 incremements of 10
        "chain_note_vol": 130, # 0-100 incremements of 10
        "bonus_note_vol": 131, # 0-100 incremements of 10
        "gate_skip": 132, # on or off
        "key_beam_display": 133, # on or off

        "left_slide_note_color": 201, # red blue green or orange
        "right_slide_note_color": 202, # red blue green or orange
        "forward_slide_note_color": 203, # red blue green or orange
        "back_slide_note_color": 204, # red blue green or orange

        "master_vol": 1001, # 0-100 incremements of 10
        "set_title_id": 1002, # ID
        "set_icon_id": 1003, # ID
        "set_nav_id": 1004, # ID
        "set_plate_id": 1005, # ID
    }

    class Difficulty(Enum):
        NORMAL = 1
        HARD = 2
        EXPERT = 3
        INFERNO = 4
    
    class Region(Enum):
        NONE = 0
        HOKKAIDO = 1
        AOMORI = 2
        IWATE = 3
        MIYAGI = 4
        AKITA = 5
        YAMAGATA = 6
        FUKUSHIMA = 7
        IBARAKI = 8
        TOCHIGI = 9
        GUNMA = 10
        SAITAMA = 11
        CHIBA = 12
        TOKYO = 13
        KANAGAWA = 14
        NIIGATA = 15
        TOYAMA = 16
        ISHIKAWA = 17
        FUKUI = 18
        YAMANASHI = 19
        NAGANO = 20
        GIFU = 21
        SHIZUOKA = 22
        AICHI = 23
        MIE = 24
        SHIGA = 25
        KYOTO = 26
        OSAKA = 27
        HYOGO = 28
        NARA = 29
        WAKAYAMA = 30
        TOTTORI = 31
        SHIMANE = 32
        OKAYAMA = 33
        HIROSHIMA = 34
        YAMAGUCHI = 35
        TOKUSHIMA = 36
        KAGAWA = 37
        EHIME = 38
        KOCHI = 39
        FUKUOKA = 40
        SAGA = 41
        NAGASAKI = 42
        KUMAMOTO = 43
        OITA = 44
        MIYAZAKI = 45
        KAGOSHIMA = 46
        OKINAWA = 47
        UNITED_STATES = 48
        TAIWAN = 49
        HONG_KONG = 50
        SINGAPORE = 51
        KOREA = 52
    
    VALID_COUNTRIES = set(["JPN", "USA", "KOR", "HKG", "SGP"])

    @classmethod
    def game_ver_to_string(cls, ver: int):
        return cls.VERSION_NAMES[ver]