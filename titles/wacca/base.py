from typing import Any, List, Dict
import logging
import inflection
from math import floor
from datetime import datetime, timedelta
from core.config import CoreConfig
from titles.wacca.config import WaccaConfig
from titles.wacca.const import WaccaConstants
from titles.wacca.database import WaccaData

from titles.wacca.handlers import *
from core.const import AllnetCountryCode


class WaccaBase:
    def __init__(self, cfg: CoreConfig, game_cfg: WaccaConfig) -> None:
        self.config = cfg  # Config file
        self.game_config = game_cfg  # Game Config file
        self.game = WaccaConstants.GAME_CODE  # Game code
        self.version = WaccaConstants.VER_WACCA  # Game version
        self.data = WaccaData(cfg)  # Database
        self.logger = logging.getLogger("wacca")
        self.srvtime = datetime.now()
        self.season = 1

        self.OPTIONS_DEFAULTS: Dict[str, Any] = {
            "note_speed": 5,
            "field_mask": 0,
            "note_sound": 105001,
            "note_color": 203001,
            "bgm_volume": 10,
            "bg_video": 0,
            "mirror": 0,
            "judge_display_pos": 0,
            "judge_detail_display": 0,
            "measure_guidelines": 1,
            "guideline_mask": 1,
            "judge_line_timing_adjust": 10,
            "note_design": 3,
            "bonus_effect": 1,
            "chara_voice": 1,
            "score_display_method": 0,
            "give_up": 0,
            "guideline_spacing": 1,
            "center_display": 1,
            "ranking_display": 1,
            "stage_up_icon_display": 1,
            "rating_display": 1,
            "player_level_display": 1,
            "touch_effect": 1,
            "guide_sound_vol": 3,
            "touch_note_vol": 8,
            "hold_note_vol": 8,
            "slide_note_vol": 8,
            "snap_note_vol": 8,
            "chain_note_vol": 8,
            "bonus_note_vol": 8,
            "gate_skip": 0,
            "key_beam_display": 1,
            "left_slide_note_color": 4,
            "right_slide_note_color": 3,
            "forward_slide_note_color": 1,
            "back_slide_note_color": 2,
            "master_vol": 3,
            "set_title_id": 104001,
            "set_icon_id": 102001,
            "set_nav_id": 210001,
            "set_plate_id": 211001,
        }
        self.allowed_stages = []

        prefecture_name = (
            inflection.underscore(game_cfg.server.prefecture_name)
            .replace(" ", "_")
            .upper()
        )
        if prefecture_name not in [region.name for region in WaccaConstants.Region]:
            self.logger.warning(
                f"Invalid prefecture name {game_cfg.server.prefecture_name} in config file"
            )
            self.region_id = WaccaConstants.Region.HOKKAIDO

        else:
            self.region_id = WaccaConstants.Region[prefecture_name]

    async def handle_housing_get_request(self, data: Dict) -> Dict:
        req = BaseRequest(data)
        housing_id = 1337
        self.logger.info(f"{req.chipId} -> {housing_id}")
        resp = HousingGetResponse(housing_id)
        return resp.make()

    async def handle_advertise_GetRanking_request(self, data: Dict) -> Dict:
        req = AdvertiseGetRankingRequest(data)
        return AdvertiseGetRankingResponse().make()

    async def handle_housing_start_request(self, data: Dict) -> Dict:
        req = HousingStartRequestV1(data)
        allnet_region_id = None

        machine = self.data.arcade.get_machine(req.chipId)
        if machine is not None:
            arcade = self.data.arcade.get_arcade(machine["arcade"])
            allnet_region_id = arcade["region_id"]

        if req.appVersion.country == AllnetCountryCode.JAPAN.value:
            if allnet_region_id is not None:
                region = WaccaConstants.allnet_region_id_to_wacca_region(
                    allnet_region_id
                )

                if region is None:
                    region_id = self.region_id
                else:
                    region_id = region

            else:
                region_id = self.region_id

        elif req.appVersion.country in WaccaConstants.VALID_COUNTRIES:
            region_id = WaccaConstants.Region[req.appVersion.country]

        else:
            region_id = WaccaConstants.Region.NONE

        resp = HousingStartResponseV1(region_id)
        return resp.make()

    async def handle_advertise_GetNews_request(self, data: Dict) -> Dict:
        resp = GetNewsResponseV1()
        return resp.make()

    async def handle_user_status_logout_request(self, data: Dict) -> Dict:
        req = UserStatusLogoutRequest(data)
        self.logger.info(f"Log out user {req.userId} from {req.chipId}")
        return BaseResponse().make()

    async def handle_user_status_get_request(self, data: Dict) -> Dict:
        req = UserStatusGetRequest(data)
        resp = UserStatusGetV1Response()

        profile = self.data.profile.get_profile(aime_id=req.aimeId)
        if profile is None:
            self.logger.info(f"No user exists for aime id {req.aimeId}")
            resp.profileStatus = ProfileStatus.ProfileRegister
            return resp.make()

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

        if req.appVersion > resp.lastGameVersion:
            resp.versionStatus = PlayVersionStatus.VersionUpgrade

        elif req.appVersion < resp.lastGameVersion:
            resp.versionStatus = PlayVersionStatus.VersionTooNew

        return resp.make()

    async def handle_user_status_login_request(self, data: Dict) -> Dict:
        req = UserStatusLoginRequest(data)
        resp = UserStatusLoginResponseV1()
        is_consec_day = True

        if req.userId == 0:
            self.logger.info(f"Guest login on {req.chipId}")
            resp.lastLoginDate = 0

        else:
            profile = self.data.profile.get_profile(req.userId)
            if profile is None:
                self.logger.warning(
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

            if resp.firstLoginDaily:
                # TODO: Daily bonus
                pass

            # TODO: VIP dialy/monthly rewards

        return resp.make()

    async def handle_user_status_create_request(self, data: Dict) -> Dict:
        req = UserStatusCreateRequest(data)

        profileId = self.data.profile.create_profile(
            req.aimeId, req.username, self.version
        )

        if profileId is None:
            return BaseResponse().make()
        
        if profileId == 0:
            # We've already made this profile, just return success
            new_user = self.data.profile.get_profile(aime_id=req.aimeId)
            profileId = new_user['id']

        # Insert starting items
        self.data.item.put_item(req.aimeId, WaccaConstants.ITEM_TYPES["title"], 104001)
        self.data.item.put_item(req.aimeId, WaccaConstants.ITEM_TYPES["title"], 104002)
        self.data.item.put_item(req.aimeId, WaccaConstants.ITEM_TYPES["title"], 104003)
        self.data.item.put_item(req.aimeId, WaccaConstants.ITEM_TYPES["title"], 104005)

        self.data.item.put_item(req.aimeId, WaccaConstants.ITEM_TYPES["icon"], 102001)
        self.data.item.put_item(req.aimeId, WaccaConstants.ITEM_TYPES["icon"], 102002)

        self.data.item.put_item(
            req.aimeId, WaccaConstants.ITEM_TYPES["note_color"], 103001
        )
        self.data.item.put_item(
            req.aimeId, WaccaConstants.ITEM_TYPES["note_color"], 203001
        )

        self.data.item.put_item(
            req.aimeId, WaccaConstants.ITEM_TYPES["note_sound"], 105001
        )

        self.data.item.put_item(
            req.aimeId, WaccaConstants.ITEM_TYPES["navigator"], 210001
        )

        return UserStatusCreateResponseV2(profileId, req.username).make()

    async def handle_user_status_getDetail_request(self, data: Dict) -> Dict:
        req = UserStatusGetDetailRequest(data)
        resp = UserStatusGetDetailResponseV1()

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
        profile_trophies = self.data.item.get_trophies(user_id)
        profile_tickets = self.data.item.get_tickets(user_id)

        resp.songUpdateTime = int(profile["last_login_date"].timestamp())
        resp.songPlayStatus = [profile["last_song_id"], 1]

        resp.userStatus.userId = profile["id"]
        resp.userStatus.username = profile["username"]
        resp.userStatus.xp = profile["xp"]
        resp.userStatus.danLevel = profile["dan_level"]
        resp.userStatus.danType = profile["dan_type"]
        resp.userStatus.wp = profile["wp"]
        resp.userStatus.useCount = profile["login_count"]

        if self.game_config.mods.infinite_wp:
            resp.userStatus.wp = 999999

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

                    else:
                        itm_send = GenericItemSend(
                            item["item_id"], 1, int(item["acquire_date"].timestamp())
                        )

                        if item["type"] == WaccaConstants.ITEM_TYPES["title"]:
                            resp.userItems.titles.append(itm_send)

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

        return resp.make()

    async def handle_user_trial_get_request(self, data: Dict) -> Dict:
        req = UserTrialGetRequest(data)
        resp = UserTrialGetResponse()

        user_id = self.data.profile.profile_to_aime_user(req.profileId)
        if user_id is None:
            self.logger.error(
                f"handle_user_trial_get_request: No profile with id {req.profileId}"
            )
            return resp.make()

        self.logger.info(f"Get trial info for user {req.profileId}")
        stages = self.data.score.get_stageup(user_id, self.version)
        if stages is None:
            stages = []

        tmp: List[StageInfo] = []

        for d in self.allowed_stages:
            stage_info = StageInfo(d[0], d[1])

            for score in stages:
                if score["stage_id"] == stage_info.danId:
                    stage_info.clearStatus = score["clear_status"]
                    stage_info.numSongCleared = score["clear_song_ct"]
                    stage_info.song1BestScore = score["song1_score"]
                    stage_info.song2BestScore = score["song2_score"]
                    stage_info.song3BestScore = score["song3_score"]
                    break

            tmp.append(stage_info)

        for x in range(len(tmp)):
            if tmp[x].danLevel >= 10 and (
                tmp[x + 1].clearStatus >= 1 or tmp[x].clearStatus >= 1
            ):
                resp.stageList.append(tmp[x])
            elif tmp[x].danLevel < 10:
                resp.stageList.append(tmp[x])

        return resp.make()

    async def handle_user_trial_update_request(self, data: Dict) -> Dict:
        req = UserTrialUpdateRequest(data)

        total_score = 0
        for score in req.songScores:
            total_score += score

        while len(req.songScores) < 3:
            req.songScores.append(0)

        profile = self.data.profile.get_profile(req.profileId)

        user_id = profile["user"]
        old_stage = self.data.score.get_stageup_stage(
            user_id, self.version, req.stageId
        )

        if old_stage is None:
            self.data.score.put_stageup(
                user_id,
                self.version,
                req.stageId,
                req.clearType.value,
                req.numSongsCleared,
                req.songScores[0],
                req.songScores[1],
                req.songScores[2],
            )

        else:
            # We only care about total score for best of, even if one score happens to be lower (I think)
            if total_score > (
                old_stage["song1_score"]
                + old_stage["song2_score"]
                + old_stage["song3_score"]
            ):
                best_score1 = req.songScores[0]
                best_score2 = req.songScores[1]
                best_score3 = req.songScores[2]
            else:
                best_score1 = old_stage["song1_score"]
                best_score2 = old_stage["song2_score"]
                best_score3 = old_stage["song3_score"]

            self.data.score.put_stageup(
                user_id,
                self.version,
                req.stageId,
                req.clearType.value,
                req.numSongsCleared,
                best_score1,
                best_score2,
                best_score3,
            )

        if (
            req.stageLevel > 0 and req.stageLevel <= 14 and req.clearType.value > 0
        ):  # For some reason, special stages send dan level 1001...
            if req.stageLevel > profile["dan_level"] or (
                req.stageLevel == profile["dan_level"]
                and req.clearType.value > profile["dan_type"]
            ):
                self.data.profile.update_profile_dan(
                    req.profileId, req.stageLevel, req.clearType.value
                )

        self.util_put_items(req.profileId, user_id, req.itemsObtained)

        # user/status/update isn't called after stageup so we have to do some things now
        current_icon = self.data.profile.get_options(
            user_id, WaccaConstants.OPTIONS["set_icon_id"]
        )
        current_nav = self.data.profile.get_options(
            user_id, WaccaConstants.OPTIONS["set_nav_id"]
        )

        if current_icon is None:
            current_icon = self.OPTIONS_DEFAULTS["set_icon_id"]
        else:
            current_icon = current_icon["value"]
        if current_nav is None:
            current_nav = self.OPTIONS_DEFAULTS["set_nav_id"]
        else:
            current_nav = current_nav["value"]

        self.data.item.put_item(
            user_id, WaccaConstants.ITEM_TYPES["icon"], current_icon
        )
        self.data.item.put_item(
            user_id, WaccaConstants.ITEM_TYPES["navigator"], current_nav
        )
        self.data.profile.update_profile_playtype(
            req.profileId, 4, data["appVersion"][:7]
        )
        return BaseResponse().make()

    async def handle_user_sugoroku_update_request(self, data: Dict) -> Dict:
        ver_split = data["appVersion"].split(".")
        resp = BaseResponse()

        if int(ver_split[0]) <= 2 and int(ver_split[1]) < 53:
            req = UserSugarokuUpdateRequestV1(data)
            mission_flg = 0

        else:
            req = UserSugarokuUpdateRequestV2(data)
            mission_flg = req.mission_flag

        user_id = self.data.profile.profile_to_aime_user(req.profileId)
        if user_id is None:
            self.logger.info(
                f"handle_user_sugoroku_update_request unknwon profile ID {req.profileId}"
            )
            return resp.make()

        self.util_put_items(req.profileId, user_id, req.itemsObtainted)

        self.data.profile.update_gate(
            user_id,
            req.gateId,
            req.page,
            req.progress,
            req.loops,
            mission_flg,
            req.totalPts,
        )
        return resp.make()

    async def handle_user_info_getMyroom_request(self, data: Dict) -> Dict:
        return UserInfogetMyroomResponseV1().make()

    async def handle_user_music_unlock_request(self, data: Dict) -> Dict:
        req = UserMusicUnlockRequest(data)

        profile = self.data.profile.get_profile(req.profileId)
        if profile is None:
            return BaseResponse().make()
        user_id = profile["user"]
        current_wp = profile["wp"]

        tickets = self.data.item.get_tickets(user_id)
        new_tickets: List[TicketItem] = []

        for ticket in tickets:
            new_tickets.append(TicketItem(ticket["id"], ticket["ticket_id"], 9999999999))

        for item in req.itemsUsed:
            if (
                item.itemType == WaccaConstants.ITEM_TYPES["wp"]
                and not self.game_config.mods.infinite_wp
            ):
                if current_wp >= item.quantity:
                    current_wp -= item.quantity
                    self.data.profile.spend_wp(req.profileId, item.quantity)
                else:
                    return BaseResponse().make()

            elif (
                item.itemType == WaccaConstants.ITEM_TYPES["ticket"]
                and not self.game_config.mods.infinite_tickets
            ):
                for x in range(len(new_tickets)):
                    if new_tickets[x].ticketId == item.itemId:
                        self.logger.debug(
                            f"Remove ticket ID {new_tickets[x].userTicketId} type {new_tickets[x].ticketId} from {user_id}"
                        )
                        self.data.item.spend_ticket(new_tickets[x].userTicketId)
                        new_tickets.pop(x)
                        break

        # wp, ticket info
        if req.difficulty > WaccaConstants.Difficulty.HARD.value:
            old_score = self.data.score.get_best_score(
                user_id, req.songId, req.difficulty
            )
            if not old_score:
                self.data.score.put_best_score(
                    user_id, req.songId, req.difficulty, 0, [0] * 5, [0] * 13, 0, 0
                )

        self.data.item.unlock_song(
            user_id,
            req.songId,
            req.difficulty
            if req.difficulty > WaccaConstants.Difficulty.HARD.value
            else WaccaConstants.Difficulty.HARD.value,
        )

        if self.game_config.mods.infinite_tickets:
            for x in range(5):
                new_tickets.append(TicketItem(x, 106002, 0))

        if self.game_config.mods.infinite_wp:
            current_wp = 999999

        return UserMusicUnlockResponse(current_wp, new_tickets).make()

    async def handle_user_info_getRanking_request(self, data: Dict) -> Dict:
        # total score, high score by song, cumulative socre, stage up score, other score, WP ranking
        # This likely requies calculating standings at regular intervals and caching the results
        return UserInfogetRankingResponse().make()

    async def handle_user_music_update_request(self, data: Dict) -> Dict:
        ver_split = data["appVersion"].split(".")
        if int(ver_split[0]) >= 3:
            resp = UserMusicUpdateResponseV3()
            req = UserMusicUpdateRequestV2(data)
        elif int(ver_split[0]) >= 2:
            resp = UserMusicUpdateResponseV2()
            req = UserMusicUpdateRequestV2(data)
        else:
            resp = UserMusicUpdateResponseV1()
            req = UserMusicUpdateRequestV1(data)

        resp.songDetail.songId = req.songDetail.songId
        resp.songDetail.difficulty = req.songDetail.difficulty

        if req.profileId == 0:
            self.logger.info(
                f"Guest score for song {req.songDetail.songId} difficulty {req.songDetail.difficulty}"
            )
            return resp.make()

        profile = self.data.profile.get_profile(req.profileId)

        if profile is None:
            self.logger.warning(
                f"handle_user_music_update_request: No profile for game_id {req.profileId}"
            )
            return resp.make()

        user_id = profile["user"]
        self.util_put_items(req.profileId, user_id, req.itemsObtained)

        playlog_clear_status = (
            req.songDetail.flagCleared
            + req.songDetail.flagMissless
            + req.songDetail.flagFullcombo
            + req.songDetail.flagAllMarvelous
        )

        self.data.score.put_playlog(
            user_id,
            req.songDetail.songId,
            req.songDetail.difficulty,
            req.songDetail.score,
            playlog_clear_status,
            req.songDetail.grade.value,
            req.songDetail.maxCombo,
            req.songDetail.judgements.marvCt,
            req.songDetail.judgements.greatCt,
            req.songDetail.judgements.goodCt,
            req.songDetail.judgements.missCt,
            req.songDetail.fastCt,
            req.songDetail.slowCt,
            self.season,
        )

        old_score = self.data.score.get_best_score(
            user_id, req.songDetail.songId, req.songDetail.difficulty
        )

        if not old_score:
            grades = [0] * 13
            clears = [0] * 5

            clears[0] = 1
            clears[1] = 1 if req.songDetail.flagCleared else 0
            clears[2] = 1 if req.songDetail.flagMissless else 0
            clears[3] = 1 if req.songDetail.flagFullcombo else 0
            clears[4] = 1 if req.songDetail.flagAllMarvelous else 0

            grades[req.songDetail.grade.value - 1] = 1

            self.data.score.put_best_score(
                user_id,
                req.songDetail.songId,
                req.songDetail.difficulty,
                req.songDetail.score,
                clears,
                grades,
                req.songDetail.maxCombo,
                req.songDetail.judgements.missCt,
            )

            resp.songDetail.score = req.songDetail.score
            resp.songDetail.lowestMissCount = req.songDetail.judgements.missCt

        else:
            grades = [
                old_score["grade_d_ct"],
                old_score["grade_c_ct"],
                old_score["grade_b_ct"],
                old_score["grade_a_ct"],
                old_score["grade_aa_ct"],
                old_score["grade_aaa_ct"],
                old_score["grade_s_ct"],
                old_score["grade_ss_ct"],
                old_score["grade_sss_ct"],
                old_score["grade_master_ct"],
                old_score["grade_sp_ct"],
                old_score["grade_ssp_ct"],
                old_score["grade_sssp_ct"],
            ]
            clears = [
                old_score["play_ct"],
                old_score["clear_ct"],
                old_score["missless_ct"],
                old_score["fullcombo_ct"],
                old_score["allmarv_ct"],
            ]

            clears[0] += 1
            clears[1] += 1 if req.songDetail.flagCleared else 0
            clears[2] += 1 if req.songDetail.flagMissless else 0
            clears[3] += 1 if req.songDetail.flagFullcombo else 0
            clears[4] += 1 if req.songDetail.flagAllMarvelous else 0

            grades[req.songDetail.grade.value - 1] += 1

            best_score = max(req.songDetail.score, old_score["score"])
            best_max_combo = max(req.songDetail.maxCombo, old_score["best_combo"])
            lowest_miss_ct = min(
                req.songDetail.judgements.missCt, old_score["lowest_miss_ct"]
            )
            best_rating = max(
                self.util_calc_song_rating(req.songDetail.score, req.songDetail.level),
                old_score["rating"],
            )

            self.data.score.put_best_score(
                user_id,
                req.songDetail.songId,
                req.songDetail.difficulty,
                best_score,
                clears,
                grades,
                best_max_combo,
                lowest_miss_ct,
            )

            resp.songDetail.score = best_score
            resp.songDetail.lowestMissCount = lowest_miss_ct
            resp.songDetail.rating = best_rating

        resp.songDetail.clearCounts = SongDetailClearCounts(counts=clears)
        resp.songDetail.clearCountsSeason = SongDetailClearCounts(counts=clears)

        if int(ver_split[0]) >= 3:
            resp.songDetail.grades = SongDetailGradeCountsV2(counts=grades)
        else:
            resp.songDetail.grades = SongDetailGradeCountsV1(counts=grades)
        resp.songDetail.lockState = 1
        return resp.make()

    # TODO: Coop and vs data
    async def handle_user_music_updateCoop_request(self, data: Dict) -> Dict:
        coop_info = data["params"][4]
        return self.handle_user_music_update_request(data)

    async def handle_user_music_updateVersus_request(self, data: Dict) -> Dict:
        vs_info = data["params"][4]
        return self.handle_user_music_update_request(data)

    async def handle_user_music_updateTrial_request(self, data: Dict) -> Dict:
        return self.handle_user_music_update_request(data)

    async def handle_user_mission_update_request(self, data: Dict) -> Dict:
        req = UserMissionUpdateRequest(data)
        page_status = req.params[1][1]

        profile = self.data.profile.get_profile(req.profileId)
        if profile is None:
            return BaseResponse().make()

        if len(req.itemsObtained) > 0:
            self.util_put_items(req.profileId, profile["user"], req.itemsObtained)

        self.data.profile.update_bingo(
            profile["user"], req.bingoDetail.pageNumber, page_status
        )
        self.data.profile.update_tutorial_flags(req.profileId, req.params[3])

        return BaseResponse().make()

    async def handle_user_goods_purchase_request(self, data: Dict) -> Dict:
        req = UserGoodsPurchaseRequest(data)
        resp = UserGoodsPurchaseResponse()

        profile = self.data.profile.get_profile(req.profileId)
        if profile is None:
            return BaseResponse().make()

        user_id = profile["user"]
        resp.currentWp = profile["wp"]

        if (
            req.purchaseType == PurchaseType.PurchaseTypeWP
            and not self.game_config.mods.infinite_wp
        ):
            resp.currentWp -= req.cost
            self.data.profile.spend_wp(req.profileId, req.cost)

        elif req.purchaseType == PurchaseType.PurchaseTypeCredit:
            self.logger.info(
                f"User {req.profileId} Purchased item {req.itemObtained.itemType} id {req.itemObtained.itemId} for {req.cost} credits on machine {req.chipId}"
            )

        self.util_put_items(req.profileId, user_id, [req.itemObtained])

        if self.game_config.mods.infinite_tickets:
            for x in range(5):
                resp.tickets.append(TicketItem(x, 106002, 0))
        else:
            tickets = self.data.item.get_tickets(user_id)

            for ticket in tickets:
                resp.tickets.append(
                    TicketItem(
                        ticket["id"],
                        ticket["ticket_id"],
                        int((self.srvtime + timedelta(days=30)).timestamp()),
                    )
                )

        if self.game_config.mods.infinite_wp:
            resp.currentWp = 999999

        return resp.make()

    async def handle_competition_status_login_request(self, data: Dict) -> Dict:
        return BaseResponse().make()

    async def handle_competition_status_update_request(self, data: Dict) -> Dict:
        return BaseResponse().make()

    async def handle_user_rating_update_request(self, data: Dict) -> Dict:
        req = UserRatingUpdateRequest(data)

        user_id = self.data.profile.profile_to_aime_user(req.profileId)

        if user_id is None:
            self.logger.error(
                f"handle_user_rating_update_request: No profild with ID {req.profileId}"
            )
            return BaseResponse().make()

        for song in req.songs:
            self.data.score.update_song_rating(
                user_id, song.songId, song.difficulty, song.rating
            )

        self.data.profile.update_user_rating(req.profileId, req.totalRating)

        return BaseResponse().make()

    async def handle_user_status_update_request(self, data: Dict) -> Dict:
        req = UserStatusUpdateRequestV1(data)

        user_id = self.data.profile.profile_to_aime_user(req.profileId)
        if user_id is None:
            self.logger.info(
                f"handle_user_status_update_request: No profile with ID {req.profileId}"
            )
            return BaseResponse().make()

        self.util_put_items(req.profileId, user_id, req.itemsRecieved)
        self.data.profile.update_profile_playtype(
            req.profileId, req.playType.value, data["appVersion"][:7]
        )

        current_icon = self.data.profile.get_options(
            user_id, WaccaConstants.OPTIONS["set_icon_id"]
        )
        current_nav = self.data.profile.get_options(
            user_id, WaccaConstants.OPTIONS["set_nav_id"]
        )

        if current_icon is None:
            current_icon = self.OPTIONS_DEFAULTS["set_icon_id"]
        else:
            current_icon = current_icon["value"]
        if current_nav is None:
            current_nav = self.OPTIONS_DEFAULTS["set_nav_id"]
        else:
            current_nav = current_nav["value"]

        self.data.item.put_item(
            user_id, WaccaConstants.ITEM_TYPES["icon"], current_icon
        )
        self.data.item.put_item(
            user_id, WaccaConstants.ITEM_TYPES["navigator"], current_nav
        )
        return BaseResponse().make()

    async def handle_user_info_update_request(self, data: Dict) -> Dict:
        req = UserInfoUpdateRequest(data)

        user_id = self.data.profile.profile_to_aime_user(req.profileId)

        for opt in req.optsUpdated:
            self.data.profile.update_option(user_id, opt.optId, opt.optVal)

        for update in req.datesUpdated:
            pass

        for fav in req.favoritesAdded:
            self.data.profile.add_favorite_song(user_id, fav)

        for unfav in req.favoritesRemoved:
            self.data.profile.remove_favorite_song(user_id, unfav)

        return BaseResponse().make()

    async def handle_user_vip_get_request(self, data: Dict) -> Dict:
        req = UserVipGetRequest(data)
        resp = UserVipGetResponse()

        profile = self.data.profile.get_profile(req.profileId)
        if profile is None:
            self.logger.warning(
                f"handle_user_vip_get_request no profile with ID {req.profileId}"
            )
            return BaseResponse().make()

        if (
            "vip_expire_time" in profile
            and profile["vip_expire_time"] is not None
            and profile["vip_expire_time"].timestamp() > int(self.srvtime.timestamp())
        ):
            resp.vipDays = int(
                (profile["vip_expire_time"].timestamp() - int(self.srvtime.timestamp()))
                / 86400
            )

        resp.vipDays += 30

        resp.presents.append(VipLoginBonus(1, 0, 16, 211025, 1))
        resp.presents.append(VipLoginBonus(2, 0, 6, 202086, 1))
        resp.presents.append(VipLoginBonus(3, 0, 11, 205008, 1))
        resp.presents.append(VipLoginBonus(4, 0, 10, 203009, 1))
        resp.presents.append(VipLoginBonus(5, 0, 16, 211026, 1))
        resp.presents.append(VipLoginBonus(6, 0, 9, 206001, 1))

        return resp.make()

    async def handle_user_vip_start_request(self, data: Dict) -> Dict:
        req = UserVipStartRequest(data)

        profile = self.data.profile.get_profile(req.profileId)
        if profile is None:
            return BaseResponse().make()

        # This should never happen because wacca stops you from buying VIP
        # if you have more then 10 days remaining, but this IS wacca we're dealing with...
        if (
            "always_vip" in profile
            and profile["always_vip"]
            or self.game_config.mods.always_vip
        ):
            return UserVipStartResponse(
                int((self.srvtime + timedelta(days=req.days)).timestamp())
            ).make()

        vip_exp_time = self.srvtime + timedelta(days=req.days)
        self.data.profile.update_vip_time(req.profileId, vip_exp_time)
        return UserVipStartResponse(int(vip_exp_time.timestamp())).make()

    def util_put_items(
        self, profile_id: int, user_id: int, items_obtained: List[GenericItemRecv]
    ) -> None:
        if user_id is None or profile_id <= 0:
            return None

        if items_obtained:
            for item in items_obtained:
                if item.itemType == WaccaConstants.ITEM_TYPES["xp"]:
                    self.data.profile.add_xp(profile_id, item.quantity)

                elif item.itemType == WaccaConstants.ITEM_TYPES["wp"]:
                    self.data.profile.add_wp(profile_id, item.quantity)

                elif (
                    item.itemType
                    == WaccaConstants.ITEM_TYPES["music_difficulty_unlock"]
                    or item.itemType == WaccaConstants.ITEM_TYPES["music_unlock"]
                ):
                    if item.quantity > WaccaConstants.Difficulty.HARD.value:
                        old_score = self.data.score.get_best_score(
                            user_id, item.itemId, item.quantity
                        )
                        if not old_score:
                            self.data.score.put_best_score(
                                user_id,
                                item.itemId,
                                item.quantity,
                                0,
                                [0] * 5,
                                [0] * 13,
                                0,
                                0,
                            )

                    if item.quantity == 0:
                        item.quantity = WaccaConstants.Difficulty.HARD.value
                    self.data.item.unlock_song(user_id, item.itemId, item.quantity)

                elif item.itemType == WaccaConstants.ITEM_TYPES["ticket"]:
                    self.data.item.add_ticket(user_id, item.itemId)

                elif item.itemType == WaccaConstants.ITEM_TYPES["trophy"]:
                    self.data.item.update_trophy(
                        user_id, item.itemId, self.season, item.quantity, 0
                    )

                else:
                    self.data.item.put_item(user_id, item.itemType, item.itemId)

    def util_calc_song_rating(self, score: int, difficulty: float) -> int:
        if score >= 990000:
            const = 4.00
        elif score >= 980000 and score < 990000:
            const = 3.75
        elif score >= 970000 and score < 980000:
            const = 3.50
        elif score >= 960000 and score < 970000:
            const = 3.25
        elif score >= 950000 and score < 960000:
            const = 3.00
        elif score >= 940000 and score < 950000:
            const = 2.75
        elif score >= 930000 and score < 940000:
            const = 2.50
        elif score >= 920000 and score < 930000:
            const = 2.25
        elif score >= 910000 and score < 920000:
            const = 2.00
        elif score >= 900000 and score < 910000:
            const = 1.00
        else:
            const = 0.00

        return floor((difficulty * const) * 10)
