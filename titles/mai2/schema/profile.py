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
    Column("sortCategorySetting", Integer),
    Column("sortMusicSetting", Integer),
    Column("selectedCardList", JSON),
    Column("encountMapNpcList", JSON),
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
    Column("holdDesign", Integer),
    Column("slideDesign", Integer),
    Column("starType", Integer),
    Column("outlineDesign", Integer),
    Column("noteSize", Integer),
    Column("slideSize", Integer),
    Column("touchSize", Integer),
    Column("starRotate", Integer),
    Column("dispCenter", Integer),
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
    Column("touchHoldVolume", Integer),
    Column("damageSeVolume", Integer),
    Column("headPhoneVolume", Integer),
    Column("sortTab", Integer),
    Column("sortMusic", Integer),
    UniqueConstraint("user", "version", name="mai2_profile_option_uk"),
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
    Column("kind", Integer, nullable=False),
    Column("activityId", Integer, nullable=False),
    Column("param1", Integer, nullable=False),
    Column("param2", Integer, nullable=False),
    Column("param3", Integer, nullable=False),
    Column("param4", Integer, nullable=False),
    Column("sortNumber", Integer, nullable=False),
    UniqueConstraint("user", "kind", "activityId", name="mai2_profile_activity_uk"),
    mysql_charset="utf8mb4",
)


class Mai2ProfileData(BaseData):
    def put_profile_detail(
        self, user_id: int, version: int, detail_data: Dict
    ) -> Optional[Row]:
        detail_data["user"] = user_id
        detail_data["version"] = version
        sql = insert(detail).values(**detail_data)

        conflict = sql.on_duplicate_key_update(**detail_data)

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(
                f"put_profile: Failed to create profile! user_id {user_id}"
            )
            return None
        return result.lastrowid

    def get_profile_detail(self, user_id: int, version: int) -> Optional[Row]:
        sql = select(detail).where(
            and_(detail.c.user == user_id, detail.c.version == version)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_profile_ghost(
        self, user_id: int, version: int, ghost_data: Dict
    ) -> Optional[int]:
        ghost_data["user"] = user_id
        ghost_data["version_int"] = version

        sql = insert(ghost).values(**ghost_data)
        conflict = sql.on_duplicate_key_update(**ghost_data)

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(f"put_profile_ghost: failed to update! {user_id}")
            return None
        return result.lastrowid

    def get_profile_ghost(self, user_id: int, version: int) -> Optional[Row]:
        sql = select(ghost).where(
            and_(ghost.c.user == user_id, ghost.c.version_int == version)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_profile_extend(
        self, user_id: int, version: int, extend_data: Dict
    ) -> Optional[int]:
        extend_data["user"] = user_id
        extend_data["version"] = version

        sql = insert(extend).values(**extend_data)
        conflict = sql.on_duplicate_key_update(**extend_data)

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(f"put_profile_extend: failed to update! {user_id}")
            return None
        return result.lastrowid

    def get_profile_extend(self, user_id: int, version: int) -> Optional[Row]:
        sql = select(extend).where(
            and_(extend.c.user == user_id, extend.c.version == version)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_profile_option(
        self, user_id: int, version: int, option_data: Dict
    ) -> Optional[int]:
        option_data["user"] = user_id
        option_data["version"] = version

        sql = insert(option).values(**option_data)
        conflict = sql.on_duplicate_key_update(**option_data)

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(f"put_profile_option: failed to update! {user_id}")
            return None
        return result.lastrowid

    def get_profile_option(self, user_id: int, version: int) -> Optional[Row]:
        sql = select(option).where(
            and_(option.c.user == user_id, option.c.version == version)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_profile_rating(
        self, user_id: int, version: int, rating_data: Dict
    ) -> Optional[int]:
        rating_data["user"] = user_id
        rating_data["version"] = version

        sql = insert(rating).values(**rating_data)
        conflict = sql.on_duplicate_key_update(**rating_data)

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(f"put_profile_rating: failed to update! {user_id}")
            return None
        return result.lastrowid

    def get_profile_rating(self, user_id: int, version: int) -> Optional[Row]:
        sql = select(rating).where(
            and_(rating.c.user == user_id, rating.c.version == version)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_profile_region(self, user_id: int, region_id: int) -> Optional[int]:
        sql = insert(region).values(
            user=user_id,
            regionId=region_id,
            created=datetime.strftime(datetime.now(), Mai2Constants.DATE_TIME_FORMAT),
        )

        conflict = sql.on_duplicate_key_update(playCount=region.c.playCount + 1)

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(f"put_region: failed to update! {user_id}")
            return None
        return result.lastrowid

    def get_regions(self, user_id: int) -> Optional[List[Dict]]:
        sql = select(region).where(region.c.user == user_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_profile_activity(self, user_id: int, activity_data: Dict) -> Optional[int]:
        if "id" in activity_data:
            activity_data["activityId"] = activity_data["id"]
            activity_data.pop("id")

        activity_data["user"] = user_id

        sql = insert(activity).values(**activity_data)

        conflict = sql.on_duplicate_key_update(**activity_data)

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(
                f"put_profile_activity: failed to update! user_id: {user_id}"
            )
            return None
        return result.lastrowid

    def get_profile_activity(self, user_id: int, kind: int = None) -> Optional[Row]:
        sql = activity.select(
            and_(
                activity.c.user == user_id,
                (activity.c.kind == kind) if kind is not None else True,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()
