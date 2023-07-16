from typing import Any, List, Dict
from datetime import datetime, timedelta
import json

from core.config import CoreConfig
from titles.wacca.s import WaccaS
from titles.wacca.config import WaccaConfig
from titles.wacca.const import WaccaConstants

from titles.wacca.handlers import *


class WaccaLily(WaccaS):
    def __init__(self, cfg: CoreConfig, game_cfg: WaccaConfig) -> None:
        super().__init__(cfg, game_cfg)
        self.version = WaccaConstants.VER_WACCA_LILY
        self.season = 2

        self.OPTIONS_DEFAULTS["set_nav_id"] = 210002
        self.allowed_stages = [
            (2014, 14),
            (2013, 13),
            (2012, 12),
            (2011, 11),
            (2010, 10),
            (2009, 9),
            (2008, 8),
            (2007, 7),
            (2006, 6),
            (2005, 5),
            (2004, 4),
            (2003, 3),
            (2002, 2),
            (2001, 1),
            (210001, 0),
            (210002, 0),
            (210003, 0),
        ]

    def handle_advertise_GetNews_request(self, data: Dict) -> Dict:
        resp = GetNewsResponseV3()
        return resp.make()

    def handle_housing_start_request(self, data: Dict) -> Dict:
        req = HousingStartRequestV2(data)

        if req.appVersion.country != "JPN" and req.appVersion.country in [
            region.name for region in WaccaConstants.Region
        ]:
            region_id = WaccaConstants.Region[req.appVersion.country]
        else:
            region_id = self.region_id

        resp = HousingStartResponseV1(region_id)
        return resp.make()

    def handle_user_status_create_request(self, data: Dict) -> Dict:
        req = UserStatusCreateRequest(data)
        resp = super().handle_user_status_create_request(data)

        self.data.item.put_item(
            req.aimeId, WaccaConstants.ITEM_TYPES["navigator"], 210002
        )  # Lily, Added Lily

        return resp

    def handle_user_status_get_request(self, data: Dict) -> Dict:
        req = UserStatusGetRequest(data)
        resp = UserStatusGetV2Response()

        profile = self.data.profile.get_profile(aime_id=req.aimeId)
        if profile is None:
            self.logger.info(f"No user exists for aime id {req.aimeId}")
            resp.profileStatus = ProfileStatus.ProfileRegister
            return resp.make()

        opts = self.data.profile.get_options(req.aimeId)

        self.logger.info(f"User preview for {req.aimeId} from {req.chipId}")
        if profile["last_game_ver"] is None:
            resp.lastGameVersion = ShortVersion(str(req.appVersion))
        else:
            resp.lastGameVersion = ShortVersion(profile["last_game_ver"])

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

        set_title_id = self.data.profile.get_options(
            WaccaConstants.OPTIONS["set_title_id"], profile["user"]
        )
        if set_title_id is None:
            set_title_id = self.OPTIONS_DEFAULTS["set_title_id"]
        resp.setTitleId = set_title_id

        set_icon_id = self.data.profile.get_options(
            WaccaConstants.OPTIONS["set_title_id"], profile["user"]
        )
        if set_icon_id is None:
            set_icon_id = self.OPTIONS_DEFAULTS["set_icon_id"]
        resp.setIconId = set_icon_id

        if profile["last_login_date"].timestamp() < int(
            datetime.now()
            .replace(hour=0, minute=0, second=0, microsecond=0)
            .timestamp()
        ):
            resp.userStatus.loginsToday = 0

        if profile["last_login_date"].timestamp() < int(
            (
                datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                - timedelta(days=1)
            ).timestamp()
        ):
            resp.userStatus.loginConsecutiveDays = 0

        if req.appVersion > resp.lastGameVersion:
            resp.versionStatus = PlayVersionStatus.VersionUpgrade

        elif req.appVersion < resp.lastGameVersion:
            resp.versionStatus = PlayVersionStatus.VersionTooNew

        if profile["vip_expire_time"] is not None:
            resp.userStatus.vipExpireTime = int(profile["vip_expire_time"].timestamp())

        if profile["always_vip"] or self.game_config.mods.always_vip:
            resp.userStatus.vipExpireTime = int(
                (datetime.now() + timedelta(days=30)).timestamp()
            )

        if self.game_config.mods.infinite_wp:
            resp.userStatus.wp = 999999

        for opt in opts:
            resp.options.append(UserOption(opt["opt_id"], opt["value"]))

        return resp.make()

    def handle_user_status_login_request(self, data: Dict) -> Dict:
        req = UserStatusLoginRequest(data)
        resp = UserStatusLoginResponseV2()
        is_consec_day = True

        if req.userId == 0:
            self.logger.info(f"Guest login on {req.chipId}")
            resp.lastLoginDate = 0

        else:
            profile = self.data.profile.get_profile(req.userId)
            if profile is None:
                self.logger.warn(
                    f"Unknown user id {req.userId} attempted login from {req.chipId}"
                )
                return resp.make()

            self.logger.info(f"User {req.userId} login on {req.chipId}")
            last_login_time = int(profile["last_login_date"].timestamp())
            resp.lastLoginDate = last_login_time
            midnight_today_ts = int(
                datetime.now()
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .timestamp()
            )

            # If somebodies login timestamp < midnight of current day, then they are logging in for the first time today
            if last_login_time < midnight_today_ts:
                resp.firstLoginDaily = True

            # If the difference between midnight today and their last login is greater then 1 day (86400 seconds) they've broken their streak
            if midnight_today_ts - last_login_time > 86400:
                is_consec_day = False

            self.data.profile.session_login(
                req.userId, resp.firstLoginDaily, is_consec_day
            )
            resp.vipInfo.pageYear = datetime.now().year
            resp.vipInfo.pageMonth = datetime.now().month
            resp.vipInfo.pageDay = datetime.now().day
            resp.vipInfo.numItem = 1

        return resp.make()

    def handle_user_status_getDetail_request(self, data: Dict) -> Dict:
        req = UserStatusGetDetailRequest(data)
        if req.appVersion.minor >= 53:
            resp = UserStatusGetDetailResponseV3()
        else:
            resp = UserStatusGetDetailResponseV2()

        profile = self.data.profile.get_profile(req.userId)
        if profile is None:
            self.logger.warn(f"Unknown profile {req.userId}")
            return resp.make()

        self.logger.info(f"Get detail for profile {req.userId}")
        user_id = profile["user"]

        profile_scores = self.data.score.get_best_scores(user_id)
        profile_items = self.data.item.get_items(user_id)
        profile_song_unlocks = self.data.item.get_song_unlocks(user_id)
        profile_options = self.data.profile.get_options(user_id)
        profile_favorites = self.data.profile.get_favorite_songs(user_id)
        profile_gates = self.data.profile.get_gates(user_id)
        profile_trophies = self.data.item.get_trophies(user_id)
        profile_tickets = self.data.item.get_tickets(user_id)

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

        for opt in profile_options:
            resp.options.append(UserOption(opt["opt_id"], opt["value"]))

        for gate in self.game_config.gates.enabled_gates:
            added_gate = False

            for user_gate in profile_gates:
                if user_gate["gate_id"] == gate:
                    if req.appVersion.minor >= 53:
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

                    else:
                        resp.gateInfo.append(
                            GateDetailV1(
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
                if req.appVersion.minor >= 53:
                    resp.gateInfo.append(GateDetailV2(gate))

                else:
                    resp.gateInfo.append(GateDetailV1(gate))

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

            grade_cts = SongDetailGradeCountsV1(
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
            )

            deets = BestScoreDetailV1(song["song_id"], song["chart_id"])
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

    def handle_user_info_getMyroom_request(self, data: Dict) -> Dict:
        return UserInfogetMyroomResponseV2().make()

    def handle_user_status_update_request(self, data: Dict) -> Dict:
        super().handle_user_status_update_request(data)
        req = UserStatusUpdateRequestV2(data)
        self.data.profile.update_profile_lastplayed(
            req.profileId,
            req.lastSongInfo.lastSongId,
            req.lastSongInfo.lastSongDiff,
            req.lastSongInfo.lastFolderOrd,
            req.lastSongInfo.lastFolderId,
            req.lastSongInfo.lastSongOrd,
        )
        return BaseResponse().make()
