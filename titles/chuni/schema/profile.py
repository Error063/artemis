from typing import Dict, List, Optional
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON, BigInteger
from sqlalchemy.engine.base import Connection
from sqlalchemy.schema import ForeignKey
from sqlalchemy.engine import Row
from sqlalchemy.sql import func, select
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

profile = Table(
    "chuni_profile_data",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("exp", Integer),
    Column("level", Integer),
    Column("point", Integer),
    Column("frameId", Integer),
    Column("isMaimai", Boolean),
    Column("trophyId", Integer),
    Column("userName", String(25)),
    Column("isWebJoin", Boolean),
    Column("playCount", Integer),
    Column("lastGameId", String(25)),
    Column("totalPoint", BigInteger),
    Column("characterId", Integer),
    Column("firstGameId", String(25)),
    Column("friendCount", Integer),
    Column("lastPlaceId", Integer),
    Column("nameplateId", Integer),
    Column("totalMapNum", Integer),
    Column("lastAllNetId", Integer),
    Column("lastClientId", String(25)),
    Column("lastPlayDate", String(25)),
    Column("lastRegionId", Integer),
    Column("playerRating", Integer),
    Column("totalHiScore", Integer),
    Column("webLimitDate", String(25)),
    Column("firstPlayDate", String(25)),
    Column("highestRating", Integer),
    Column("lastPlaceName", String(25)),
    Column("multiWinCount", Integer),
    Column("acceptResCount", Integer),
    Column("lastRegionName", String(25)),
    Column("lastRomVersion", String(25)),
    Column("multiPlayCount", Integer),
    Column("firstRomVersion", String(25)),
    Column("lastDataVersion", String(25)),
    Column("requestResCount", Integer),
    Column("successResCount", Integer),
    Column("eventWatchedDate", String(25)),
    Column("firstDataVersion", String(25)),
    Column("reincarnationNum", Integer),
    Column("playedTutorialBit", Integer),
    Column("totalBasicHighScore", Integer),
    Column("totalExpertHighScore", Integer),
    Column("totalMasterHighScore", Integer),
    Column("totalRepertoireCount", Integer),
    Column("firstTutorialCancelNum", Integer),
    Column("totalAdvancedHighScore", Integer),
    Column("masterTutorialCancelNum", Integer),
    Column("ext1", Integer),  # Added in chunew
    Column("ext2", Integer),
    Column("ext3", Integer),
    Column("ext4", Integer),
    Column("ext5", Integer),
    Column("ext6", Integer),
    Column("ext7", Integer),
    Column("ext8", Integer),
    Column("ext9", Integer),
    Column("ext10", Integer),
    Column("extStr1", String(255)),
    Column("extStr2", String(255)),
    Column("extLong1", Integer),
    Column("extLong2", Integer),
    Column("mapIconId", Integer),
    Column("compatibleCmVersion", String(25)),
    Column("medal", Integer),
    Column("voiceId", Integer),
    Column(
        "teamId",
        Integer,
        ForeignKey("chuni_profile_team.id", ondelete="SET NULL", onupdate="SET NULL"),
    ),
    Column("eliteRankPoint", Integer, server_default="0"),
    Column("stockedGridCount", Integer, server_default="0"),
    Column("netBattleLoseCount", Integer, server_default="0"),
    Column("netBattleHostErrCnt", Integer, server_default="0"),
    Column("netBattle4thCount", Integer, server_default="0"),
    Column("overPowerRate", Integer, server_default="0"),
    Column("battleRewardStatus", Integer, server_default="0"),
    Column("netBattle1stCount", Integer, server_default="0"),
    Column("charaIllustId", Integer, server_default="0"),
    Column("userNameEx", String(8), server_default=""),
    Column("netBattleWinCount", Integer, server_default="0"),
    Column("netBattleCorrection", Integer, server_default="0"),
    Column("classEmblemMedal", Integer, server_default="0"),
    Column("overPowerPoint", Integer, server_default="0"),
    Column("netBattleErrCnt", Integer, server_default="0"),
    Column("battleRankId", Integer, server_default="0"),
    Column("netBattle3rdCount", Integer, server_default="0"),
    Column("netBattleConsecutiveWinCount", Integer, server_default="0"),
    Column("overPowerLowerRank", Integer, server_default="0"),
    Column("classEmblemBase", Integer, server_default="0"),
    Column("battleRankPoint", Integer, server_default="0"),
    Column("netBattle2ndCount", Integer, server_default="0"),
    Column("totalUltimaHighScore", Integer, server_default="0"),
    Column("skillId", Integer, server_default="0"),
    Column("lastCountryCode", String(5), server_default="JPN"),
    Column("isNetBattleHost", Boolean, server_default="0"),
    Column("battleRewardCount", Integer, server_default="0"),
    Column("battleRewardIndex", Integer, server_default="0"),
    Column("netBattlePlayCount", Integer, server_default="0"),
    Column("exMapLoopCount", Integer, server_default="0"),
    Column("netBattleEndState", Integer, server_default="0"),
    Column("rankUpChallengeResults", JSON),
    Column("avatarBack", Integer, server_default="0"),
    Column("avatarFace", Integer, server_default="0"),
    Column("avatarPoint", Integer, server_default="0"),
    Column("avatarItem", Integer, server_default="0"),
    Column("avatarWear", Integer, server_default="0"),
    Column("avatarFront", Integer, server_default="0"),
    Column("avatarSkin", Integer, server_default="0"),
    Column("avatarHead", Integer, server_default="0"),
    UniqueConstraint("user", "version", name="chuni_profile_profile_uk"),
    mysql_charset="utf8mb4",
)

profile_ex = Table(
    "chuni_profile_data_ex",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("ext1", Integer),
    Column("ext2", Integer),
    Column("ext3", Integer),
    Column("ext4", Integer),
    Column("ext5", Integer),
    Column("ext6", Integer),
    Column("ext7", Integer),
    Column("ext8", Integer),
    Column("ext9", Integer),
    Column("ext10", Integer),
    Column("ext11", Integer),
    Column("ext12", Integer),
    Column("ext13", Integer),
    Column("ext14", Integer),
    Column("ext15", Integer),
    Column("ext16", Integer),
    Column("ext17", Integer),
    Column("ext18", Integer),
    Column("ext19", Integer),
    Column("ext20", Integer),
    Column("medal", Integer),
    Column("extStr1", String(255)),
    Column("extStr2", String(255)),
    Column("extStr3", String(255)),
    Column("extStr4", String(255)),
    Column("extStr5", String(255)),
    Column("voiceId", Integer),
    Column("extLong1", Integer),
    Column("extLong2", Integer),
    Column("extLong3", Integer),
    Column("extLong4", Integer),
    Column("extLong5", Integer),
    Column("mapIconId", Integer),
    Column("compatibleCmVersion", String(25)),
    UniqueConstraint("user", "version", name="chuni_profile_data_ex_uk"),
    mysql_charset="utf8mb4",
)

option = Table(
    "chuni_profile_option",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("speed", Integer),
    Column("bgInfo", Integer),
    Column("rating", Integer),
    Column("privacy", Integer),
    Column("judgePos", Integer),
    Column("matching", Integer),
    Column("guideLine", Integer),
    Column("headphone", Integer),
    Column("optionSet", Integer),
    Column("fieldColor", Integer),
    Column("guideSound", Integer),
    Column("successAir", Integer),
    Column("successTap", Integer),
    Column("judgeAttack", Integer),
    Column("playerLevel", Integer),
    Column("soundEffect", Integer),
    Column("judgeJustice", Integer),
    Column("successExTap", Integer),
    Column("successFlick", Integer),
    Column("successSkill", Integer),
    Column("successSlideHold", Integer),
    Column("successTapTimbre", Integer),
    Column("ext1", Integer),  # Added in chunew
    Column("ext2", Integer),
    Column("ext3", Integer),
    Column("ext4", Integer),
    Column("ext5", Integer),
    Column("ext6", Integer),
    Column("ext7", Integer),
    Column("ext8", Integer),
    Column("ext9", Integer),
    Column("ext10", Integer),
    Column("categoryDetail", Integer, server_default="0"),
    Column("judgeTimingOffset_120", Integer, server_default="0"),
    Column("resultVoiceShort", Integer, server_default="0"),
    Column("judgeAppendSe", Integer, server_default="0"),
    Column("judgeCritical", Integer, server_default="0"),
    Column("trackSkip", Integer, server_default="0"),
    Column("selectMusicFilterLv", Integer, server_default="0"),
    Column("sortMusicFilterLv", Integer, server_default="0"),
    Column("sortMusicGenre", Integer, server_default="0"),
    Column("speed_120", Integer, server_default="0"),
    Column("judgeTimingOffset", Integer, server_default="0"),
    Column("mirrorFumen", Integer, server_default="0"),
    Column("playTimingOffset_120", Integer, server_default="0"),
    Column("hardJudge", Integer, server_default="0"),
    Column("notesThickness", Integer, server_default="0"),
    Column("fieldWallPosition", Integer, server_default="0"),
    Column("playTimingOffset", Integer, server_default="0"),
    Column("fieldWallPosition_120", Integer, server_default="0"),
    UniqueConstraint("user", name="chuni_profile_option_uk"),
    mysql_charset="utf8mb4",
)

option_ex = Table(
    "chuni_profile_option_ex",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("ext1", Integer),
    Column("ext2", Integer),
    Column("ext3", Integer),
    Column("ext4", Integer),
    Column("ext5", Integer),
    Column("ext6", Integer),
    Column("ext7", Integer),
    Column("ext8", Integer),
    Column("ext9", Integer),
    Column("ext10", Integer),
    Column("ext11", Integer),
    Column("ext12", Integer),
    Column("ext13", Integer),
    Column("ext14", Integer),
    Column("ext15", Integer),
    Column("ext16", Integer),
    Column("ext17", Integer),
    Column("ext18", Integer),
    Column("ext19", Integer),
    Column("ext20", Integer),
    UniqueConstraint("user", name="chuni_profile_option_ex_uk"),
    mysql_charset="utf8mb4",
)

recent_rating = Table(
    "chuni_profile_recent_rating",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("recentRating", JSON),
    UniqueConstraint("user", name="chuni_profile_recent_rating_uk"),
    mysql_charset="utf8mb4",
)

region = Table(
    "chuni_profile_region",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("regionId", Integer),
    Column("playCount", Integer),
    UniqueConstraint("user", "regionId", name="chuni_profile_region_uk"),
    mysql_charset="utf8mb4",
)

activity = Table(
    "chuni_profile_activity",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("kind", Integer),
    Column(
        "activityId", Integer
    ),  # Reminder: Change this to ID in base.py or the game will be sad
    Column("sortNumber", Integer),
    Column("param1", Integer),
    Column("param2", Integer),
    Column("param3", Integer),
    Column("param4", Integer),
    UniqueConstraint("user", "kind", "activityId", name="chuni_profile_activity_uk"),
    mysql_charset="utf8mb4",
)

charge = Table(
    "chuni_profile_charge",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("chargeId", Integer),
    Column("stock", Integer),
    Column("purchaseDate", String(25)),
    Column("validDate", String(25)),
    Column("param1", Integer),
    Column("param2", Integer),
    Column("paramDate", String(25)),
    UniqueConstraint("user", "chargeId", name="chuni_profile_charge_uk"),
    mysql_charset="utf8mb4",
)

emoney = Table(
    "chuni_profile_emoney",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("ext1", Integer),
    Column("ext2", Integer),
    Column("ext3", Integer),
    Column("type", Integer),
    Column("emoneyBrand", Integer),
    Column("emoneyCredit", Integer),
    UniqueConstraint("user", "emoneyBrand", name="chuni_profile_emoney_uk"),
    mysql_charset="utf8mb4",
)

overpower = Table(
    "chuni_profile_overpower",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("genreId", Integer),
    Column("difficulty", Integer),
    Column("rate", Integer),
    Column("point", Integer),
    UniqueConstraint("user", "genreId", "difficulty", name="chuni_profile_emoney_uk"),
    mysql_charset="utf8mb4",
)

team = Table(
    "chuni_profile_team",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("teamName", String(255)),
    Column("teamPoint", Integer),
    mysql_charset="utf8mb4",
)


class ChuniProfileData(BaseData):
    def put_profile_data(
        self, aime_id: int, version: int, profile_data: Dict
    ) -> Optional[int]:
        profile_data["user"] = aime_id
        profile_data["version"] = version
        if "accessCode" in profile_data:
            profile_data.pop("accessCode")

        profile_data = self.fix_bools(profile_data)

        sql = insert(profile).values(**profile_data)
        conflict = sql.on_duplicate_key_update(**profile_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_profile_data: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def get_profile_preview(self, aime_id: int, version: int) -> Optional[Row]:
        sql = (
            select([profile, option])
            .join(option, profile.c.user == option.c.user)
            .filter(and_(profile.c.user == aime_id, profile.c.version <= version))
        ).order_by(profile.c.version.desc())

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_profile_data(self, aime_id: int, version: int) -> Optional[Row]:
        sql = select(profile).where(
            and_(
                profile.c.user == aime_id,
                profile.c.version <= version,
            )
        ).order_by(profile.c.version.desc())

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_profile_data_ex(
        self, aime_id: int, version: int, profile_ex_data: Dict
    ) -> Optional[int]:
        profile_ex_data["user"] = aime_id
        profile_ex_data["version"] = version
        if "accessCode" in profile_ex_data:
            profile_ex_data.pop("accessCode")

        sql = insert(profile_ex).values(**profile_ex_data)
        conflict = sql.on_duplicate_key_update(**profile_ex_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warning(
                f"put_profile_data_ex: Failed to update! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid

    def get_profile_data_ex(self, aime_id: int, version: int) -> Optional[Row]:
        sql = select(profile_ex).where(
            and_(
                profile_ex.c.user == aime_id,
                profile_ex.c.version <= version,
            )
        ).order_by(profile_ex.c.version.desc())

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_profile_option(self, aime_id: int, option_data: Dict) -> Optional[int]:
        option_data["user"] = aime_id

        sql = insert(option).values(**option_data)
        conflict = sql.on_duplicate_key_update(**option_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warning(
                f"put_profile_option: Failed to update! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid

    def get_profile_option(self, aime_id: int) -> Optional[Row]:
        sql = select(option).where(option.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_profile_option_ex(
        self, aime_id: int, option_ex_data: Dict
    ) -> Optional[int]:
        option_ex_data["user"] = aime_id

        sql = insert(option_ex).values(**option_ex_data)
        conflict = sql.on_duplicate_key_update(**option_ex_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warning(
                f"put_profile_option_ex: Failed to update! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid

    def get_profile_option_ex(self, aime_id: int) -> Optional[Row]:
        sql = select(option_ex).where(option_ex.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_profile_recent_rating(
        self, aime_id: int, recent_rating_data: List[Dict]
    ) -> Optional[int]:
        sql = insert(recent_rating).values(
            user=aime_id, recentRating=recent_rating_data
        )
        conflict = sql.on_duplicate_key_update(recentRating=recent_rating_data)

        result = self.execute(conflict)
        if result is None:
            self.logger.warning(
                f"put_profile_recent_rating: Failed to update! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid

    def get_profile_recent_rating(self, aime_id: int) -> Optional[Row]:
        sql = select(recent_rating).where(recent_rating.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_profile_activity(self, aime_id: int, activity_data: Dict) -> Optional[int]:
        # The game just uses "id" but we need to distinguish that from the db column "id"
        activity_data["user"] = aime_id
        activity_data["activityId"] = activity_data["id"]
        activity_data.pop("id")

        sql = insert(activity).values(**activity_data)
        conflict = sql.on_duplicate_key_update(**activity_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warning(
                f"put_profile_activity: Failed to update! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid

    def get_profile_activity(self, aime_id: int, kind: int) -> Optional[List[Row]]:
        sql = (
            select(activity)
            .where(and_(activity.c.user == aime_id, activity.c.kind == kind))
            .order_by(activity.c.sortNumber.desc())  # to get the last played track
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_profile_charge(self, aime_id: int, charge_data: Dict) -> Optional[int]:
        charge_data["user"] = aime_id

        sql = insert(charge).values(**charge_data)
        conflict = sql.on_duplicate_key_update(**charge_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warning(
                f"put_profile_charge: Failed to update! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid

    def get_profile_charge(self, aime_id: int) -> Optional[List[Row]]:
        sql = select(charge).where(charge.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def add_profile_region(self, aime_id: int, region_id: int) -> Optional[int]:
        pass

    def get_profile_regions(self, aime_id: int) -> Optional[List[Row]]:
        pass

    def put_profile_emoney(self, aime_id: int, emoney_data: Dict) -> Optional[int]:
        emoney_data["user"] = aime_id

        sql = insert(emoney).values(**emoney_data)
        conflict = sql.on_duplicate_key_update(**emoney_data)

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid

    def get_profile_emoney(self, aime_id: int) -> Optional[List[Row]]:
        sql = select(emoney).where(emoney.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_profile_overpower(
        self, aime_id: int, overpower_data: Dict
    ) -> Optional[int]:
        overpower_data["user"] = aime_id

        sql = insert(overpower).values(**overpower_data)
        conflict = sql.on_duplicate_key_update(**overpower_data)

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid

    def get_profile_overpower(self, aime_id: int) -> Optional[List[Row]]:
        sql = select(overpower).where(overpower.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()
