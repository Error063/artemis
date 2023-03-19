from typing import Dict, List, Optional
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON, BigInteger
from sqlalchemy.engine.base import Connection
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select
from sqlalchemy.engine import Row
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata
from core.config import CoreConfig

# Cammel case column names technically don't follow the other games but
# it makes it way easier on me to not fuck with what the games has
profile = Table(
    "ongeki_profile_data",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("userName", String(8)),
    Column("level", Integer),
    Column("reincarnationNum", Integer),
    Column("exp", Integer),
    Column("point", Integer),
    Column("totalPoint", Integer),
    Column("playCount", Integer),
    Column("jewelCount", Integer),
    Column("totalJewelCount", Integer),
    Column("medalCount", Integer),
    Column("playerRating", Integer),
    Column("highestRating", Integer),
    Column("battlePoint", Integer),
    Column("nameplateId", Integer),
    Column("trophyId", Integer),
    Column("cardId", Integer),
    Column("characterId", Integer),
    Column("characterVoiceNo", Integer),
    Column("tabSetting", Integer),
    Column("tabSortSetting", Integer),
    Column("cardCategorySetting", Integer),
    Column("cardSortSetting", Integer),
    Column("playedTutorialBit", Integer),
    Column("firstTutorialCancelNum", Integer),
    Column("sumTechHighScore", BigInteger),
    Column("sumTechBasicHighScore", BigInteger),
    Column("sumTechAdvancedHighScore", BigInteger),
    Column("sumTechExpertHighScore", BigInteger),
    Column("sumTechMasterHighScore", BigInteger),
    Column("sumTechLunaticHighScore", BigInteger),
    Column("sumBattleHighScore", BigInteger),
    Column("sumBattleBasicHighScore", BigInteger),
    Column("sumBattleAdvancedHighScore", BigInteger),
    Column("sumBattleExpertHighScore", BigInteger),
    Column("sumBattleMasterHighScore", BigInteger),
    Column("sumBattleLunaticHighScore", BigInteger),
    Column("eventWatchedDate", String(255)),
    Column("cmEventWatchedDate", String(255)),
    Column("firstGameId", String(8)),
    Column("firstRomVersion", String(8)),
    Column("firstDataVersion", String(8)),
    Column("firstPlayDate", String(255)),
    Column("lastGameId", String(8)),
    Column("lastRomVersion", String(8)),
    Column("lastDataVersion", String(8)),
    Column("compatibleCmVersion", String(8)),
    Column("lastPlayDate", String(255)),
    Column("lastPlaceId", Integer),
    Column("lastPlaceName", String(255)),
    Column("lastRegionId", Integer),
    Column("lastRegionName", String(255)),
    Column("lastAllNetId", Integer),
    Column("lastClientId", String(16)),
    Column("lastUsedDeckId", Integer),
    Column("lastPlayMusicLevel", Integer),
    Column("banStatus", Integer, server_default="0"),
    Column("rivalScoreCategorySetting", Integer, server_default="0"),
    Column("overDamageBattlePoint", Integer, server_default="0"),
    Column("bestBattlePoint", Integer, server_default="0"),
    Column("lastEmoneyBrand", Integer, server_default="0"),
    Column("lastEmoneyCredit", Integer, server_default="0"),
    Column("isDialogWatchedSuggestMemory", Boolean, server_default="0"),
    UniqueConstraint("user", "version", name="ongeki_profile_profile_uk"),
    mysql_charset="utf8mb4",
)

# No point setting defaults since the game sends everything on profile creation anyway
option = Table(
    "ongeki_profile_option",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("optionSet", Integer),
    Column("speed", Integer),
    Column("mirror", Integer),
    Column("judgeTiming", Integer),
    Column("judgeAdjustment", Integer),
    Column("abort", Integer),
    Column("tapSound", Integer),
    Column("volGuide", Integer),
    Column("volAll", Integer),
    Column("volTap", Integer),
    Column("volCrTap", Integer),
    Column("volHold", Integer),
    Column("volSide", Integer),
    Column("volFlick", Integer),
    Column("volBell", Integer),
    Column("volEnemy", Integer),
    Column("volSkill", Integer),
    Column("volDamage", Integer),
    Column("colorField", Integer),
    Column("colorLaneBright", Integer),
    Column("colorLane", Integer),
    Column("colorSide", Integer),
    Column("effectDamage", Integer),
    Column("effectPos", Integer),
    Column("judgeDisp", Integer),
    Column("judgePos", Integer),
    Column("judgeBreak", Integer),
    Column("judgeHit", Integer),
    Column("platinumBreakDisp", Integer),
    Column("judgeCriticalBreak", Integer),
    Column("matching", Integer),
    Column("dispPlayerLv", Integer),
    Column("dispRating", Integer),
    Column("dispBP", Integer),
    Column("headphone", Integer),
    Column("stealthField", Integer),
    Column("colorWallBright", Integer),
    UniqueConstraint("user", name="ongeki_profile_option_uk"),
    mysql_charset="utf8mb4",
)

activity = Table(
    "ongeki_profile_activity",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("kind", Integer),
    Column("activityId", Integer),
    Column("sortNumber", Integer),
    Column("param1", Integer),
    Column("param2", Integer),
    Column("param3", Integer),
    Column("param4", Integer),
    UniqueConstraint("user", "kind", "activityId", name="ongeki_profile_activity_uk"),
    mysql_charset="utf8mb4",
)

recent_rating = Table(
    "ongeki_profile_recent_rating",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("recentRating", JSON),
    UniqueConstraint("user", name="ongeki_profile_recent_rating_uk"),
    mysql_charset="utf8mb4",
)

rating_log = Table(
    "ongeki_profile_rating_log",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("highestRating", Integer),
    Column("dataVersion", String(10)),
    UniqueConstraint("user", "dataVersion", name="ongeki_profile_rating_log_uk"),
    mysql_charset="utf8mb4",
)

region = Table(
    "ongeki_profile_region",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("regionId", Integer),
    Column("playCount", Integer),
    Column("created", String(25)),
    UniqueConstraint("user", "regionId", name="ongeki_profile_region_uk"),
    mysql_charset="utf8mb4",
)

training_room = Table(
    "ongeki_profile_training_room",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("roomId", Integer),
    Column("authKey", Integer),
    Column("cardId", Integer),
    Column("valueDate", String(25)),
    UniqueConstraint("user", "roomId", name="ongeki_profile_training_room_uk"),
    mysql_charset="utf8mb4",
)

kop = Table(
    "ongeki_profile_kop",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("authKey", Integer),
    Column("kopId", Integer),
    Column("areaId", Integer),
    Column("totalTechScore", Integer),
    Column("totalPlatinumScore", Integer),
    Column("techRecordDate", String(25)),
    Column("isTotalTechNewRecord", Boolean),
    UniqueConstraint("user", "kopId", name="ongeki_profile_kop_uk"),
    mysql_charset="utf8mb4",
)

rival = Table(
    "ongeki_profile_rival",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column(
        "rivalUserId",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
    ),
    UniqueConstraint("user", "rivalUserId", name="ongeki_profile_rival_uk"),
    mysql_charset="utf8mb4",
)


class OngekiProfileData(BaseData):
    def __init__(self, cfg: CoreConfig, conn: Connection) -> None:
        super().__init__(cfg, conn)
        self.date_time_format_ext = (
            "%Y-%m-%d %H:%M:%S.%f"  # needs to be lopped off at [:-5]
        )
        self.date_time_format_short = "%Y-%m-%d"

    def get_profile_name(self, aime_id: int, version: int) -> Optional[str]:
        sql = select(profile.c.userName).where(
            and_(profile.c.user == aime_id, profile.c.version == version)
        )

        result = self.execute(sql)
        if result is None:
            return None

        row = result.fetchone()
        if row is None:
            return None

        return row["userName"]

    def get_profile_preview(self, aime_id: int, version: int) -> Optional[Row]:
        sql = (
            select([profile, option])
            .join(option, profile.c.user == option.c.user)
            .filter(and_(profile.c.user == aime_id, profile.c.version == version))
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_profile_data(self, aime_id: int, version: int) -> Optional[Row]:
        sql = select(profile).where(
            and_(
                profile.c.user == aime_id,
                profile.c.version == version,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_profile_options(self, aime_id: int) -> Optional[Row]:
        sql = select(option).where(
            and_(
                option.c.user == aime_id,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_profile_recent_rating(self, aime_id: int) -> Optional[List[Row]]:
        sql = select(recent_rating).where(recent_rating.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_profile_rating_log(self, aime_id: int) -> Optional[List[Row]]:
        sql = select(rating_log).where(recent_rating.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_profile_activity(
        self, aime_id: int, kind: int = None
    ) -> Optional[List[Row]]:
        sql = select(activity).where(
            and_(
                activity.c.user == aime_id,
                (activity.c.kind == kind) if kind is not None else True,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_kop(self, aime_id: int) -> Optional[List[Row]]:
        sql = select(kop).where(kop.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_rivals(self, aime_id: int) -> Optional[List[Row]]:
        sql = select(rival.c.rivalUserId).where(rival.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_profile_data(self, aime_id: int, version: int, data: Dict) -> Optional[int]:
        data["user"] = aime_id
        data["version"] = version
        data.pop("accessCode")

        sql = insert(profile).values(**data)
        conflict = sql.on_duplicate_key_update(**data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_profile_data: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def put_profile_options(self, aime_id: int, options_data: Dict) -> Optional[int]:
        options_data["user"] = aime_id

        sql = insert(option).values(**options_data)
        conflict = sql.on_duplicate_key_update(**options_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(
                f"put_profile_options: Failed to update! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid

    def put_profile_recent_rating(
        self, aime_id: int, recent_rating_data: List[Dict]
    ) -> Optional[int]:
        sql = insert(recent_rating).values(
            user=aime_id, recentRating=recent_rating_data
        )

        conflict = sql.on_duplicate_key_update(recentRating=recent_rating_data)

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(
                f"put_profile_recent_rating: failed to update recent rating! aime_id {aime_id}"
            )
            return None
        return result.lastrowid

    def put_profile_bp_list(
        self, aime_id: int, bp_base_list: List[Dict]
    ) -> Optional[int]:
        pass

    def put_profile_rating_log(
        self, aime_id: int, data_version: str, highest_rating: int
    ) -> Optional[int]:
        sql = insert(rating_log).values(
            user=aime_id, dataVersion=data_version, highestRating=highest_rating
        )

        conflict = sql.on_duplicate_key_update(highestRating=highest_rating)

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(
                f"put_profile_rating_log: failed to update rating log! aime_id {aime_id} data_version {data_version} highest_rating {highest_rating}"
            )
            return None
        return result.lastrowid

    def put_profile_activity(
        self,
        aime_id: int,
        kind: int,
        activity_id: int,
        sort_num: int,
        p1: int,
        p2: int,
        p3: int,
        p4: int,
    ) -> Optional[int]:
        sql = insert(activity).values(
            user=aime_id,
            kind=kind,
            activityId=activity_id,
            sortNumber=sort_num,
            param1=p1,
            param2=p2,
            param3=p3,
            param4=p4,
        )

        conflict = sql.on_duplicate_key_update(
            sortNumber=sort_num, param1=p1, param2=p2, param3=p3, param4=p4
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(
                f"put_profile_activity: failed to put activity! aime_id {aime_id} kind {kind} activity_id {activity_id}"
            )
            return None
        return result.lastrowid

    def put_profile_region(self, aime_id: int, region: int, date: str) -> Optional[int]:
        sql = insert(activity).values(
            user=aime_id, region=region, playCount=1, created=date
        )

        conflict = sql.on_duplicate_key_update(
            playCount=activity.c.playCount + 1,
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(
                f"put_profile_region: failed to update! aime_id {aime_id} region {region}"
            )
            return None
        return result.lastrowid

    def put_training_room(self, aime_id: int, room_detail: Dict) -> Optional[int]:
        room_detail["user"] = aime_id

        sql = insert(training_room).values(**room_detail)
        conflict = sql.on_duplicate_key_update(**room_detail)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_best_score: Failed to add score! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def put_kop(self, aime_id: int, kop_data: Dict) -> Optional[int]:
        kop_data["user"] = aime_id

        sql = insert(kop).values(**kop_data)
        conflict = sql.on_duplicate_key_update(**kop_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_kop: Failed to add score! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def put_rival(self, aime_id: int, rival_id: int) -> Optional[int]:
        sql = insert(rival).values(user=aime_id, rivalUserId=rival_id)

        conflict = sql.on_duplicate_key_update(rival=rival_id)

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(
                f"put_rival: failed to update! aime_id: {aime_id}, rival_id: {rival_id}"
            )
            return None
        return result.lastrowid
