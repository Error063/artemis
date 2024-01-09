from typing import Any, List, Dict
from datetime import datetime, timedelta
import json

from core.config import CoreConfig
from titles.wacca.lilyr import WaccaLilyR
from titles.wacca.config import WaccaConfig
from titles.wacca.const import WaccaConstants

from titles.wacca.handlers import *


class WaccaReverse(WaccaLilyR):
    def __init__(self, cfg: CoreConfig, game_cfg: WaccaConfig) -> None:
        super().__init__(cfg, game_cfg)
        self.version = WaccaConstants.VER_WACCA_REVERSE

        self.season = 3

        self.OPTIONS_DEFAULTS["set_nav_id"] = 310001
        self.allowed_stages = [
            (3014, 14),
            (3013, 13),
            (3012, 12),
            (3011, 11),
            (3010, 10),
            (3009, 9),
            (3008, 8),
            (3007, 7),
            (3006, 6),
            (3005, 5),
            (3004, 4),
            (3003, 3),
            (3002, 2),
            (3001, 1),
            # Touhou
            (210001, 0),
            (210002, 0),
            (210003, 0),
            # Final spurt
            (310001, 0),
            (310002, 0),
            (310003, 0),
            # boss remix
            (310004, 0),
            (310005, 0),
            (310006, 0),
        ]

    async def handle_user_status_login_request(self, data: Dict) -> Dict:
        resp = await super().handle_user_status_login_request(data)
        resp["params"].append([])
        return resp

    async def handle_user_status_getDetail_request(self, data: Dict) -> Dict:
        req = UserStatusGetDetailRequest(data)
        resp = UserStatusGetDetailResponseV4()

        profile = self.data.profile.get_profile(req.userId)
        if profile is None:
            self.logger.warning(f"Unknown profile {req.userId}")
            return resp.make()

        self.logger.info(f"Get detail for profile {req.userId}")
        user_id = profile["user"]

        profile_scores = self.data.score.get_best_scores(user_id)
        profile_items = self.data.item.get_items(user_id)
        profile_song_unlocks = self.data.item.get_song_unlocks(user_id)
        profile_options = self.data.profile.get_options(user_id)
        profile_favorites = self.data.profile.get_favorite_songs(user_id)
        profile_gates = self.data.profile.get_gates(user_id)
        profile_bingo = self.data.profile.get_bingo(user_id)
        profile_trophies = self.data.item.get_trophies(user_id)
        profile_tickets = self.data.item.get_tickets(user_id)

        if profile["gate_tutorial_flags"] is not None:
            for x in profile["gate_tutorial_flags"]:
                resp.gateTutorialFlags.append(GateTutorialFlag(x[0], x[1]))

        if profile["vip_expire_time"] is None:
            resp.userStatus.vipExpireTime = 0

        else:
            resp.userStatus.vipExpireTime = int(profile["vip_expire_time"].timestamp())

        if profile["always_vip"] or self.game_config.mods.always_vip:
            resp.userStatus.vipExpireTime = int(
                (self.srvtime + timedelta(days=31)).timestamp()
            )

        resp.songUpdateTime = int(profile["last_login_date"].timestamp())
        resp.lastSongInfo = LastSongDetail(
            profile["last_song_id"],
            profile["last_song_difficulty"],
            profile["last_folder_order"],
            profile["last_folder_id"],
            profile["last_song_order"],
        )
        resp.songPlayStatus = [resp.lastSongInfo.lastSongId, 1]

        resp.userStatus.userId = profile["id"]
        resp.userStatus.username = profile["username"]
        resp.userStatus.xp = profile["xp"]
        resp.userStatus.danLevel = profile["dan_level"]
        resp.userStatus.danType = profile["dan_type"]
        resp.userStatus.wp = profile["wp"]
        resp.userStatus.useCount = profile["login_count"]
        resp.userStatus.loginDays = profile["login_count_days"]
        resp.userStatus.loginConsecutiveDays = profile["login_count_days_consec"]
        resp.userStatus.loginsToday = profile["login_count_today"]
        resp.userStatus.rating = profile["rating"]

        if self.game_config.mods.infinite_wp:
            resp.userStatus.wp = 999999

        for fav in profile_favorites:
            resp.favorites.append(fav["song_id"])

        if profile["friend_view_1"] is not None:
            pass
        if profile["friend_view_2"] is not None:
            pass
        if profile["friend_view_3"] is not None:
            pass

        resp.seasonalPlayModeCounts.append(
            PlayModeCounts(self.season, 1, profile["playcount_single"])
        )
        resp.seasonalPlayModeCounts.append(
            PlayModeCounts(self.season, 2, profile["playcount_multi_vs"])
        )
        resp.seasonalPlayModeCounts.append(
            PlayModeCounts(self.season, 3, profile["playcount_multi_coop"])
        )
        resp.seasonalPlayModeCounts.append(
            PlayModeCounts(self.season, 4, profile["playcount_stageup"])
        )
        resp.seasonalPlayModeCounts.append(
            PlayModeCounts(self.season, 5, profile["playcount_time_free"])
        )

        # For some fucking reason if this isn't here time play is disabled
        resp.seasonalPlayModeCounts.append(PlayModeCounts(0, 1, 1))

        for opt in profile_options:
            resp.options.append(UserOption(opt["opt_id"], opt["value"]))

        if profile_bingo is not None:
            resp.bingoStatus = BingoDetail(profile_bingo["page_number"])
            for x in profile_bingo["page_progress"]:
                resp.bingoStatus.pageStatus.append(BingoPageStatus(x[0], x[1], x[2]))

        for gate in self.game_config.gates.enabled_gates:
            added_gate = False

            for user_gate in profile_gates:
                if user_gate["gate_id"] == gate:
                    resp.gateInfo.append(
                        GateDetailV2(
                            user_gate["gate_id"],
                            user_gate["page"],
                            user_gate["progress"],
                            user_gate["loops"],
                            int(user_gate["last_used"].timestamp()),
                            user_gate["mission_flag"],
                        )
                    )

                    resp.seasonInfo.cumulativeGatePts += user_gate["total_points"]

                    added_gate = True
                    break

            if not added_gate:
                resp.gateInfo.append(GateDetailV2(gate))

        for unlock in profile_song_unlocks:
            for x in range(1, unlock["highest_difficulty"] + 1):
                resp.userItems.songUnlocks.append(
                    SongUnlock(
                        unlock["song_id"], x, 0, int(unlock["acquire_date"].timestamp())
                    )
                )

        for song in profile_scores:
            resp.seasonInfo.cumulativeScore += song["score"]

            clear_cts = SongDetailClearCounts(
                song["play_ct"],
                song["clear_ct"],
                song["missless_ct"],
                song["fullcombo_ct"],
                song["allmarv_ct"],
            )

            grade_cts = SongDetailGradeCountsV2(
                song["grade_d_ct"],
                song["grade_c_ct"],
                song["grade_b_ct"],
                song["grade_a_ct"],
                song["grade_aa_ct"],
                song["grade_aaa_ct"],
                song["grade_s_ct"],
                song["grade_ss_ct"],
                song["grade_sss_ct"],
                song["grade_master_ct"],
                song["grade_sp_ct"],
                song["grade_ssp_ct"],
                song["grade_sssp_ct"],
            )

            deets = BestScoreDetailV2(song["song_id"], song["chart_id"])
            deets.clearCounts = clear_cts
            deets.clearCountsSeason = clear_cts
            deets.gradeCounts = grade_cts
            deets.score = song["score"]
            deets.bestCombo = song["best_combo"]
            deets.lowestMissCtMaybe = song["lowest_miss_ct"]
            deets.rating = song["rating"]

            resp.scores.append(deets)

        for trophy in profile_trophies:
            resp.userItems.trophies.append(
                TrophyItem(
                    trophy["trophy_id"],
                    trophy["season"],
                    trophy["progress"],
                    trophy["badge_type"],
                )
            )

        if self.game_config.mods.infinite_tickets:
            for x in range(5):
                resp.userItems.tickets.append(TicketItem(x, 106002, 0))
        else:
            for ticket in profile_tickets:
                if ticket["expire_date"] is None:
                    expire = int((self.srvtime + timedelta(days=30)).timestamp())
                else:
                    expire = int(ticket["expire_date"].timestamp())

                resp.userItems.tickets.append(
                    TicketItem(ticket["id"], ticket["ticket_id"], expire)
                )

        if profile_items:
            for item in profile_items:
                try:
                    if item["type"] == WaccaConstants.ITEM_TYPES["icon"]:
                        resp.userItems.icons.append(
                            IconItem(
                                item["item_id"],
                                1,
                                item["use_count"],
                                int(item["acquire_date"].timestamp()),
                            )
                        )

                    elif item["type"] == WaccaConstants.ITEM_TYPES["navigator"]:
                        resp.userItems.navigators.append(
                            NavigatorItem(
                                item["item_id"],
                                1,
                                int(item["acquire_date"].timestamp()),
                                item["use_count"],
                                item["use_count"],
                            )
                        )

                    else:
                        itm_send = GenericItemSend(
                            item["item_id"], 1, int(item["acquire_date"].timestamp())
                        )

                        if item["type"] == WaccaConstants.ITEM_TYPES["title"]:
                            resp.userItems.titles.append(itm_send)

                        elif item["type"] == WaccaConstants.ITEM_TYPES["user_plate"]:
                            resp.userItems.plates.append(itm_send)

                        elif item["type"] == WaccaConstants.ITEM_TYPES["touch_effect"]:
                            resp.userItems.touchEffect.append(itm_send)

                        elif item["type"] == WaccaConstants.ITEM_TYPES["note_color"]:
                            resp.userItems.noteColors.append(itm_send)

                        elif item["type"] == WaccaConstants.ITEM_TYPES["note_sound"]:
                            resp.userItems.noteSounds.append(itm_send)

                except Exception:
                    self.logger.error(
                        f"{__name__} Failed to load item {item['item_id']} for user {profile['user']}"
                    )

        resp.seasonInfo.level = profile["xp"]
        resp.seasonInfo.wpObtained = profile["wp_total"]
        resp.seasonInfo.wpSpent = profile["wp_spent"]
        resp.seasonInfo.titlesObtained = len(resp.userItems.titles)
        resp.seasonInfo.iconsObtained = len(resp.userItems.icons)
        resp.seasonInfo.noteColorsObtained = len(resp.userItems.noteColors)
        resp.seasonInfo.noteSoundsObtained = len(resp.userItems.noteSounds)
        resp.seasonInfo.platesObtained = len(resp.userItems.plates)

        return resp.make()

    async def handle_user_status_create_request(self, data: Dict) -> Dict:
        req = UserStatusCreateRequest(data)
        resp = await super().handle_user_status_create_request(data)

        self.data.item.put_item(
            req.aimeId, WaccaConstants.ITEM_TYPES["navigator"], 310001
        )  # Added reverse
        self.data.item.put_item(
            req.aimeId, WaccaConstants.ITEM_TYPES["navigator"], 310002
        )  # Added reverse
        
        self.data.item.put_item(
            req.aimeId, WaccaConstants.ITEM_TYPES["touch_effect"], 312000
        )  # Added reverse
        self.data.item.put_item(
            req.aimeId, WaccaConstants.ITEM_TYPES["touch_effect"], 312001
        )  # Added reverse

        return resp
