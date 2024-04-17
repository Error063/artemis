from core.data.schema import BaseData, metadata
from titles.mai2.const import Mai2Constants

from typing import Optional, Dict, List
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON, BigInteger
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select
from sqlalchemy.engine import Row
from sqlalchemy.dialects.mysql import insert
from datetime import datetime

detail = Table(
    "mai2_profile_detail",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("userName", String(25)),
    Column("isNetMember", Integer),
    Column("iconId", Integer),
    Column("plateId", Integer),
    Column("titleId", Integer),
    Column("partnerId", Integer),
    Column("frameId", Integer),
    Column("selectMapId", Integer),
    Column("totalAwake", Integer),
    Column("gradeRating", Integer),
    Column("musicRating", Integer),
    Column("playerRating", Integer),
    Column("highestRating", Integer),
    Column("gradeRank", Integer),
    Column("classRank", Integer),
    Column("courseRank", Integer),
    Column("charaSlot", JSON),
    Column("charaLockSlot", JSON),
    Column("contentBit", BigInteger),
    Column("playCount", Integer),
    Column("currentPlayCount", Integer), # new with buddies
    Column("renameCredit", Integer), # new with buddies
    Column("mapStock", Integer),  # new with fes+
    Column("eventWatchedDate", String(25)),
    Column("lastGameId", String(25)),
    Column("lastRomVersion", String(25)),
    Column("lastDataVersion", String(25)),
    Column("lastLoginDate", String(25)),
    Column("lastPairLoginDate", String(25)),  # new with uni+
    Column("lastPlayDate", String(25)),
    Column("lastTrialPlayDate", String(25)),  # new with uni+
    Column("lastPlayCredit", Integer),
    Column("lastPlayMode", Integer),
    Column("lastPlaceId", Integer),
    Column("lastPlaceName", String(25)),
    Column("lastAllNetId", Integer),
    Column("lastRegionId", Integer),
    Column("lastRegionName", String(25)),
    Column("lastClientId", String(25)),
    Column("lastCountryCode", String(25)),
    Column("lastSelectEMoney", Integer),
    Column("lastSelectTicket", Integer),
    Column("lastSelectCourse", Integer),
    Column("lastCountCourse", Integer),
    Column("firstGameId", String(25)),
    Column("firstRomVersion", String(25)),
    Column("firstDataVersion", String(25)),
    Column("firstPlayDate", String(25)),
    Column("compatibleCmVersion", String(25)),
    Column("dailyBonusDate", String(25)),
    Column("dailyCourseBonusDate", String(25)),
    Column("playVsCount", Integer),
    Column("playSyncCount", Integer),
    Column("winCount", Integer),
    Column("helpCount", Integer),
    Column("comboCount", Integer),
    Column("totalDeluxscore", BigInteger),
    Column("totalBasicDeluxscore", BigInteger),
    Column("totalAdvancedDeluxscore", BigInteger),
    Column("totalExpertDeluxscore", BigInteger),
    Column("totalMasterDeluxscore", BigInteger),
    Column("totalReMasterDeluxscore", BigInteger),
    Column("totalSync", Integer),
    Column("totalBasicSync", Integer),
    Column("totalAdvancedSync", Integer),
    Column("totalExpertSync", Integer),
    Column("totalMasterSync", Integer),
    Column("totalReMasterSync", Integer),
    Column("totalAchievement", BigInteger),
    Column("totalBasicAchievement", BigInteger),
    Column("totalAdvancedAchievement", BigInteger),
    Column("totalExpertAchievement", BigInteger),
    Column("totalMasterAchievement", BigInteger),
    Column("totalReMasterAchievement", BigInteger),
    Column("playerOldRating", BigInteger),
    Column("playerNewRating", BigInteger),
    Column("dateTime", BigInteger),
    Column("banState", Integer),  # new with uni+
    UniqueConstraint("user", "version", name="mai2_profile_detail_uk"),
    mysql_charset="utf8mb4",
)

detail_old = Table(
    "maimai_profile_detail",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("lastDataVersion", Integer),
    Column("userName", String(8)),
    Column("point", Integer),
    Column("totalPoint", Integer),
    Column("iconId", Integer),
    Column("nameplateId", Integer),
    Column("frameId", Integer),
    Column("trophyId", Integer),
    Column("playCount", Integer),
    Column("playVsCount", Integer),
    Column("playSyncCount", Integer),
    Column("winCount", Integer),
    Column("helpCount", Integer),
    Column("comboCount", Integer),
    Column("feverCount", Integer),
    Column("totalHiScore", Integer),
    Column("totalEasyHighScore", Integer),
    Column("totalBasicHighScore", Integer),
    Column("totalAdvancedHighScore", Integer),
    Column("totalExpertHighScore", Integer),
    Column("totalMasterHighScore", Integer),
    Column("totalReMasterHighScore", Integer),
    Column("totalHighSync", Integer),
    Column("totalEasySync", Integer),
    Column("totalBasicSync", Integer),
    Column("totalAdvancedSync", Integer),
    Column("totalExpertSync", Integer),
    Column("totalMasterSync", Integer),
    Column("totalReMasterSync", Integer),
    Column("playerRating", Integer),
    Column("highestRating", Integer),
    Column("rankAuthTailId", Integer),
    Column("eventWatchedDate", String(255)),
    Column("webLimitDate", String(255)),
    Column("challengeTrackPhase", Integer),
    Column("firstPlayBits", Integer),
    Column("lastPlayDate", String(255)),
    Column("lastPlaceId", Integer),
    Column("lastPlaceName", String(255)),
    Column("lastRegionId", Integer),
    Column("lastRegionName", String(255)),
    Column("lastClientId", String(255)),
    Column("lastCountryCode", String(255)),
    Column("eventPoint", Integer),
    Column("totalLv", Integer),
    Column("lastLoginBonusDay", Integer),
    Column("lastSurvivalBonusDay", Integer),
    Column("loginBonusLv", Integer),
    UniqueConstraint("user", "version", name="maimai_profile_detail_uk"),
    mysql_charset="utf8mb4",
)

ghost = Table(
    "mai2_profile_ghost",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version_int", Integer, nullable=False),
    Column("name", String(25)),
    Column("iconId", Integer),
    Column("plateId", Integer),
    Column("titleId", Integer),
    Column("rate", Integer),
    Column("udemaeRate", Integer),
    Column("courseRank", Integer),
    Column("classRank", Integer),
    Column("classValue", Integer),
    Column("playDatetime", String(25)),
    Column("shopId", Integer),
    Column("regionCode", Integer),
    Column("typeId", Integer),
    Column("musicId", Integer),
    Column("difficulty", Integer),
    Column("version", Integer),
    Column("resultBitList", JSON),
    Column("resultNum", Integer),
    Column("achievement", Integer),
    UniqueConstraint(
        "user", "version", "musicId", "difficulty", name="mai2_profile_ghost_uk"
    ),
    mysql_charset="utf8mb4",
)

extend = Table(
    "mai2_profile_extend",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("selectMusicId", Integer),
    Column("selectDifficultyId", Integer),
    Column("categoryIndex", Integer),
    Column("musicIndex", Integer),
    Column("extraFlag", Integer),
    Column("selectScoreType", Integer),
    Column("extendContentBit", BigInteger),
    Column("isPhotoAgree", Boolean),
    Column("isGotoCodeRead", Boolean),
    Column("selectResultDetails", Boolean),
    Column("selectResultScoreViewType", Integer),  # new with fes+	
    Column("sortCategorySetting", Integer),
    Column("sortMusicSetting", Integer),
    Column("selectedCardList", JSON),
    Column("encountMapNpcList", JSON),
    Column("playStatusSetting", Integer, server_default="0"),
    UniqueConstraint("user", "version", name="mai2_profile_extend_uk"),
    mysql_charset="utf8mb4",
)

option = Table(
    "mai2_profile_option",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("selectMusicId", Integer),
    Column("optionKind", Integer),
    Column("noteSpeed", Integer),
    Column("slideSpeed", Integer),
    Column("touchSpeed", Integer),
    Column("tapDesign", Integer),
    Column("tapSe", Integer, server_default="0"),
    Column("holdDesign", Integer),
    Column("slideDesign", Integer),
    Column("starType", Integer),
    Column("outlineDesign", Integer),
    Column("noteSize", Integer),
    Column("slideSize", Integer),
    Column("touchSize", Integer),
    Column("starRotate", Integer),
    Column("dispCenter", Integer),
    Column("outFrameType", Integer),  # new with fes+
    Column("dispChain", Integer),
    Column("dispRate", Integer),
    Column("dispBar", Integer),
    Column("touchEffect", Integer),
    Column("submonitorAnimation", Integer),
    Column("submonitorAchive", Integer),
    Column("submonitorAppeal", Integer),
    Column("matching", Integer),
    Column("trackSkip", Integer),
    Column("brightness", Integer),
    Column("mirrorMode", Integer),
    Column("dispJudge", Integer),
    Column("dispJudgePos", Integer),
    Column("dispJudgeTouchPos", Integer),
    Column("adjustTiming", Integer),
    Column("judgeTiming", Integer),
    Column("ansVolume", Integer),
    Column("tapHoldVolume", Integer),
    Column("criticalSe", Integer),
    Column("breakSe", Integer),
    Column("breakVolume", Integer),
    Column("exSe", Integer),
    Column("exVolume", Integer),
    Column("slideSe", Integer),
    Column("slideVolume", Integer),
    Column("breakSlideVolume", Integer),  # new with fes+
    Column("touchVolume", Integer),  # new with fes+
    Column("touchHoldVolume", Integer),
    Column("damageSeVolume", Integer),
    Column("headPhoneVolume", Integer),
    Column("sortTab", Integer),
    Column("sortMusic", Integer),
    UniqueConstraint("user", "version", name="mai2_profile_option_uk"),
    mysql_charset="utf8mb4",
)

option_old = Table(
    "maimai_profile_option",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("soudEffect", Integer),
    Column("mirrorMode", Integer),
    Column("guideSpeed", Integer),
    Column("bgInfo", Integer),
    Column("brightness", Integer),
    Column("isStarRot", Integer),
    Column("breakSe", Integer),
    Column("slideSe", Integer),
    Column("hardJudge", Integer),
    Column("isTagJump", Integer),
    Column("breakSeVol", Integer),
    Column("slideSeVol", Integer),
    Column("isUpperDisp", Integer),
    Column("trackSkip", Integer),
    Column("optionMode", Integer),
    Column("simpleOptionParam", Integer),
    Column("adjustTiming", Integer),
    Column("dispTiming", Integer),
    Column("timingPos", Integer),
    Column("ansVol", Integer),
    Column("noteVol", Integer),
    Column("dmgVol", Integer),
    Column("appealFlame", Integer),
    Column("isFeverDisp", Integer),
    Column("dispJudge", Integer),
    Column("judgePos", Integer),
    Column("ratingGuard", Integer),
    Column("selectChara", Integer),
    Column("sortType", Integer),
    Column("filterGenre", Integer),
    Column("filterLevel", Integer),
    Column("filterRank", Integer),
    Column("filterVersion", Integer),
    Column("filterRec", Integer),
    Column("filterFullCombo", Integer),
    Column("filterAllPerfect", Integer),
    Column("filterDifficulty", Integer),
    Column("filterFullSync", Integer),
    Column("filterReMaster", Integer),
    Column("filterMaxFever", Integer),
    Column("finalSelectId", Integer),
    Column("finalSelectCategory", Integer),
    UniqueConstraint("user", "version", name="maimai_profile_option_uk"),
    mysql_charset="utf8mb4",
)

web_opt = Table(
    "maimai_profile_web_option",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("isNetMember", Boolean),
    Column("dispRate", Integer),
    Column("dispJudgeStyle", Integer),
    Column("dispRank", Integer),
    Column("dispHomeRanker", Integer),
    Column("dispTotalLv", Integer),
    UniqueConstraint("user", "version", name="maimai_profile_web_option_uk"),
    mysql_charset="utf8mb4",
)

grade_status = Table(
    "maimai_profile_grade_status",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("gradeVersion", Integer),
    Column("gradeLevel", Integer),
    Column("gradeSubLevel", Integer),
    Column("gradeMaxId", Integer),
    UniqueConstraint("user", "gradeVersion", name="maimai_profile_grade_status_uk"),
    mysql_charset="utf8mb4",
)

rating = Table(
    "mai2_profile_rating",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("rating", Integer),
    Column("ratingList", JSON),
    Column("newRatingList", JSON),
    Column("nextRatingList", JSON),
    Column("nextNewRatingList", JSON),
    Column("udemae", JSON),
    UniqueConstraint("user", "version", name="mai2_profile_rating_uk"),
    mysql_charset="utf8mb4",
)

region = Table(
    "mai2_profile_region",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("regionId", Integer),
    Column("playCount", Integer, server_default="1"),
    Column("created", String(25)),
    UniqueConstraint("user", "regionId", name="mai2_profile_region_uk"),
    mysql_charset="utf8mb4",
)

activity = Table(
    "mai2_profile_activity",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("kind", Integer),
    Column("activityId", Integer),
    Column("param1", Integer),
    Column("param2", Integer),
    Column("param3", Integer),
    Column("param4", Integer),
    Column("sortNumber", Integer),
    UniqueConstraint("user", "kind", "activityId", name="mai2_profile_activity_uk"),
    mysql_charset="utf8mb4",
)

boss = Table(
    "maimai_profile_boss",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("pandoraFlagList0", Integer),
    Column("pandoraFlagList1", Integer),
    Column("pandoraFlagList2", Integer),
    Column("pandoraFlagList3", Integer),
    Column("pandoraFlagList4", Integer),
    Column("pandoraFlagList5", Integer),
    Column("pandoraFlagList6", Integer),
    Column("emblemFlagList", Integer),
    UniqueConstraint("user", name="mai2_profile_boss_uk"),
    mysql_charset="utf8mb4",
)

recent_rating = Table(
    "maimai_profile_recent_rating",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("userRecentRatingList", JSON),
    UniqueConstraint("user", name="mai2_profile_recent_rating_uk"),
    mysql_charset="utf8mb4",
)

consec_logins = Table(
    "mai2_profile_consec_logins",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("logins", Integer),
    UniqueConstraint("user", "version", name="mai2_profile_consec_logins_uk"),
    mysql_charset="utf8mb4",
)


class Mai2ProfileData(BaseData):
    async def put_profile_detail(
        self, user_id: int, version: int, detail_data: Dict, is_dx: bool = True
    ) -> Optional[Row]:
        detail_data["user"] = user_id
        detail_data["version"] = version

        if is_dx:
            sql = insert(detail).values(**detail_data)
        else:
            sql = insert(detail_old).values(**detail_data)

        conflict = sql.on_duplicate_key_update(**detail_data)

        result = await self.execute(conflict)
        if result is None:
            self.logger.warning(
                f"put_profile: Failed to create profile! user_id {user_id} is_dx {is_dx}"
            )
            return None
        return result.lastrowid

    async def get_profile_detail(
        self, user_id: int, version: int, is_dx: bool = True
    ) -> Optional[Row]:
        if is_dx:
            sql = (
                select(detail)
                .where(and_(detail.c.user == user_id, detail.c.version <= version))
                .order_by(detail.c.version.desc())
            )

        else:
            sql = (
                select(detail_old)
                .where(
                    and_(detail_old.c.user == user_id, detail_old.c.version <= version)
                )
                .order_by(detail_old.c.version.desc())
            )

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    async def put_profile_ghost(
        self, user_id: int, version: int, ghost_data: Dict
    ) -> Optional[int]:
        ghost_data["user"] = user_id
        ghost_data["version_int"] = version

        sql = insert(ghost).values(**ghost_data)
        conflict = sql.on_duplicate_key_update(**ghost_data)

        result = await self.execute(conflict)
        if result is None:
            self.logger.warning(f"put_profile_ghost: failed to update! {user_id}")
            return None
        return result.lastrowid

    async def get_profile_ghost(self, user_id: int, version: int) -> Optional[Row]:
        sql = (
            select(ghost)
            .where(and_(ghost.c.user == user_id, ghost.c.version_int <= version))
            .order_by(ghost.c.version.desc())
        )

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    async def put_profile_extend(
        self, user_id: int, version: int, extend_data: Dict
    ) -> Optional[int]:
        extend_data["user"] = user_id
        extend_data["version"] = version

        sql = insert(extend).values(**extend_data)
        conflict = sql.on_duplicate_key_update(**extend_data)

        result = await self.execute(conflict)
        if result is None:
            self.logger.warning(f"put_profile_extend: failed to update! {user_id}")
            return None
        return result.lastrowid

    async def get_profile_extend(self, user_id: int, version: int) -> Optional[Row]:
        sql = (
            select(extend)
            .where(and_(extend.c.user == user_id, extend.c.version <= version))
            .order_by(extend.c.version.desc())
        )

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    async def put_profile_option(
        self, user_id: int, version: int, option_data: Dict, is_dx: bool = True
    ) -> Optional[int]:
        option_data["user"] = user_id
        option_data["version"] = version

        if is_dx:
            sql = insert(option).values(**option_data)
        else:
            sql = insert(option_old).values(**option_data)
        conflict = sql.on_duplicate_key_update(**option_data)

        result = await self.execute(conflict)
        if result is None:
            self.logger.warning(
                f"put_profile_option: failed to update! {user_id} is_dx {is_dx}"
            )
            return None
        return result.lastrowid

    async def get_profile_option(
        self, user_id: int, version: int, is_dx: bool = True
    ) -> Optional[Row]:
        if is_dx:
            sql = (
                select(option)
                .where(and_(option.c.user == user_id, option.c.version <= version))
                .order_by(option.c.version.desc())
            )
        else:
            sql = (
                select(option_old)
                .where(
                    and_(option_old.c.user == user_id, option_old.c.version <= version)
                )
                .order_by(option_old.c.version.desc())
            )

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    async def put_profile_rating(
        self, user_id: int, version: int, rating_data: Dict
    ) -> Optional[int]:
        rating_data["user"] = user_id
        rating_data["version"] = version

        sql = insert(rating).values(**rating_data)
        conflict = sql.on_duplicate_key_update(**rating_data)

        result = await self.execute(conflict)
        if result is None:
            self.logger.warning(f"put_profile_rating: failed to update! {user_id}")
            return None
        return result.lastrowid

    async def get_profile_rating(self, user_id: int, version: int) -> Optional[Row]:
        sql = (
            select(rating)
            .where(and_(rating.c.user == user_id, rating.c.version <= version))
            .order_by(rating.c.version.desc())
        )

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    async def put_profile_region(self, user_id: int, region_id: int) -> Optional[int]:
        sql = insert(region).values(
            user=user_id,
            regionId=region_id,
            created=datetime.strftime(datetime.now(), Mai2Constants.DATE_TIME_FORMAT),
        )

        conflict = sql.on_duplicate_key_update(playCount=region.c.playCount + 1)

        result = await self.execute(conflict)
        if result is None:
            self.logger.warning(f"put_region: failed to update! {user_id}")
            return None
        return result.lastrowid

    async def get_regions(self, user_id: int) -> Optional[List[Dict]]:
        sql = select(region).where(region.c.user == user_id)

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    async def put_profile_activity(self, user_id: int, activity_data: Dict) -> Optional[int]:
        if "id" in activity_data:
            activity_data["activityId"] = activity_data["id"]
            activity_data.pop("id")

        activity_data["user"] = user_id

        sql = insert(activity).values(**activity_data)

        conflict = sql.on_duplicate_key_update(**activity_data)

        result = await self.execute(conflict)
        if result is None:
            self.logger.warning(
                f"put_profile_activity: failed to update! user_id: {user_id}"
            )
            return None
        return result.lastrowid

    async def get_profile_activity(
        self, user_id: int, kind: int = None
    ) -> Optional[List[Row]]:
        sql = activity.select(
            and_(
                activity.c.user == user_id,
                (activity.c.kind == kind) if kind is not None else True,
            )
        )

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    async def put_web_option(
        self, user_id: int, version: int, web_opts: Dict
    ) -> Optional[int]:
        web_opts["user"] = user_id
        web_opts["version"] = version
        sql = insert(web_opt).values(**web_opts)

        conflict = sql.on_duplicate_key_update(**web_opts)

        result = await self.execute(conflict)
        if result is None:
            self.logger.warning(f"put_web_option: failed to update! user_id: {user_id}")
            return None
        return result.lastrowid

    async def get_web_option(self, user_id: int, version: int) -> Optional[Row]:
        sql = web_opt.select(
            and_(web_opt.c.user == user_id, web_opt.c.version == version)
        )

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    async def put_grade_status(self, user_id: int, grade_stat: Dict) -> Optional[int]:
        grade_stat["user"] = user_id
        sql = insert(grade_status).values(**grade_stat)

        conflict = sql.on_duplicate_key_update(**grade_stat)

        result = await self.execute(conflict)
        if result is None:
            self.logger.warning(
                f"put_grade_status: failed to update! user_id: {user_id}"
            )
            return None
        return result.lastrowid

    async def get_grade_status(self, user_id: int) -> Optional[Row]:
        sql = grade_status.select(grade_status.c.user == user_id)

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    async def put_boss_list(self, user_id: int, boss_stat: Dict) -> Optional[int]:
        boss_stat["user"] = user_id
        sql = insert(boss).values(**boss_stat)

        conflict = sql.on_duplicate_key_update(**boss_stat)

        result = await self.execute(conflict)
        if result is None:
            self.logger.warning(f"put_boss_list: failed to update! user_id: {user_id}")
            return None
        return result.lastrowid

    async def get_boss_list(self, user_id: int) -> Optional[Row]:
        sql = boss.select(boss.c.user == user_id)

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    async def put_recent_rating(self, user_id: int, rr: Dict) -> Optional[int]:
        sql = insert(recent_rating).values(user=user_id, userRecentRatingList=rr)

        conflict = sql.on_duplicate_key_update({"userRecentRatingList": rr})

        result = await self.execute(conflict)
        if result is None:
            self.logger.warning(
                f"put_recent_rating: failed to update! user_id: {user_id}"
            )
            return None
        return result.lastrowid

    async def get_recent_rating(self, user_id: int) -> Optional[Row]:
        sql = recent_rating.select(recent_rating.c.user == user_id)

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    async def add_consec_login(self, user_id: int, version: int) -> None:
        sql = insert(consec_logins).values(user=user_id, version=version, logins=1)

        conflict = sql.on_duplicate_key_update(logins=consec_logins.c.logins + 1)

        result = await self.execute(conflict)
        if result is None:
            self.logger.error(
                f"Failed to update consecutive login count for user {user_id} version {version}"
            )

    async def get_consec_login(self, user_id: int, version: int) -> Optional[Row]:
        sql = select(consec_logins).where(
            and_(
                consec_logins.c.user == user_id,
                consec_logins.c.version == version,
            )
        )

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    async def reset_consec_login(self, user_id: int, version: int) -> Optional[Row]:
        sql = consec_logins.update(
            and_(
                consec_logins.c.user == user_id,
                consec_logins.c.version == version,
            )
        ).values(logins=1)

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()
