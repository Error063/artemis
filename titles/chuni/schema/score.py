from typing import Dict, List, Optional
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON, BigInteger
from sqlalchemy.engine.base import Connection
from sqlalchemy.schema import ForeignKey
from sqlalchemy.engine import Row
from sqlalchemy.sql import func, select
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

course = Table(
    "chuni_score_course",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"), nullable=False),
    Column("courseId", Integer),
    Column("classId", Integer),
    Column("playCount", Integer),
    Column("scoreMax", Integer),
    Column("isFullCombo", Boolean),
    Column("isAllJustice", Boolean),
    Column("isSuccess", Boolean),
    Column("scoreRank", Integer),
    Column("eventId", Integer),
    Column("lastPlayDate", String(25)),
    Column("param1", Integer),
    Column("param2", Integer),
    Column("param3", Integer),
    Column("param4", Integer),
    Column("isClear", Boolean),
    Column("theoryCount", Integer),
    Column("orderId", Integer),
    Column("playerRating", Integer),
    UniqueConstraint("user", "courseId", name="chuni_score_course_uk"),
    mysql_charset='utf8mb4'
)

best_score = Table(
    "chuni_score_best",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"), nullable=False),
    Column("musicId", Integer),
    Column("level", Integer),
    Column("playCount", Integer),
    Column("scoreMax", Integer),
    Column("resRequestCount", Integer),
    Column("resAcceptCount", Integer),
    Column("resSuccessCount", Integer),
    Column("missCount", Integer),
    Column("maxComboCount", Integer),
    Column("isFullCombo", Boolean),
    Column("isAllJustice", Boolean),
    Column("isSuccess", Boolean),
    Column("fullChain", Integer),
    Column("maxChain", Integer),
    Column("scoreRank", Integer),
    Column("isLock", Boolean),
    Column("ext1", Integer),
    Column("theoryCount", Integer),
    UniqueConstraint("user", "musicId", "level", name="chuni_score_best_uk"),
    mysql_charset='utf8mb4'
)

playlog = Table(
    "chuni_score_playlog",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"), nullable=False),
    Column("orderId", Integer),
    Column("sortNumber", Integer),
    Column("placeId", Integer),
    Column("playDate", String(20)),
    Column("userPlayDate", String(20)),
    Column("musicId", Integer),
    Column("level", Integer),
    Column("customId", Integer),
    Column("playedUserId1", Integer),
    Column("playedUserId2", Integer),
    Column("playedUserId3", Integer),
    Column("playedUserName1", String(20)),
    Column("playedUserName2", String(20)),
    Column("playedUserName3", String(20)),
    Column("playedMusicLevel1", Integer),
    Column("playedMusicLevel2", Integer),
    Column("playedMusicLevel3", Integer),
    Column("playedCustom1", Integer),
    Column("playedCustom2", Integer),
    Column("playedCustom3", Integer),
    Column("track", Integer),
    Column("score", Integer),
    Column("rank", Integer),
    Column("maxCombo", Integer),
    Column("maxChain", Integer),
    Column("rateTap", Integer),
    Column("rateHold", Integer),
    Column("rateSlide", Integer),
    Column("rateAir", Integer),
    Column("rateFlick", Integer),
    Column("judgeGuilty", Integer),
    Column("judgeAttack", Integer),
    Column("judgeJustice", Integer),
    Column("judgeCritical", Integer),
    Column("eventId", Integer),
    Column("playerRating", Integer),
    Column("isNewRecord", Boolean),
    Column("isFullCombo", Boolean),
    Column("fullChainKind", Integer),
    Column("isAllJustice", Boolean),
    Column("isContinue", Boolean),
    Column("isFreeToPlay", Boolean),
    Column("characterId", Integer),
    Column("skillId", Integer),
    Column("playKind", Integer),
    Column("isClear", Boolean),
    Column("skillLevel", Integer),
    Column("skillEffect", Integer),
    Column("placeName", String(255)),
    Column("isMaimai", Boolean),
    Column("commonId", Integer),
    Column("charaIllustId", Integer),
    Column("romVersion", String(255)),
    Column("judgeHeaven", Integer),
    mysql_charset='utf8mb4'
)

class ChuniScoreData(BaseData):
    def get_courses(self, aime_id: int) -> Optional[Row]:
        sql = select(course).where(course.c.user == aime_id)

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()

    def put_course(self, aime_id: int, course_data: Dict) -> Optional[int]:
        course_data["user"] = aime_id
        course_data = self.fix_bools(course_data)

        sql = insert(course).values(**course_data)
        conflict = sql.on_duplicate_key_update(**course_data)

        result = self.execute(conflict)
        if result is None: return None
        return result.lastrowid
    
    def get_scores(self, aime_id: int) -> Optional[Row]:
        sql = select(best_score).where(best_score.c.user == aime_id)

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()
    
    def put_score(self, aime_id: int, score_data: Dict) -> Optional[int]:
        score_data["user"] = aime_id
        score_data = self.fix_bools(score_data)

        sql = insert(best_score).values(**score_data)
        conflict = sql.on_duplicate_key_update(**score_data)

        result = self.execute(conflict)
        if result is None: return None
        return result.lastrowid

    def get_playlogs(self, aime_id: int) -> Optional[Row]:
        sql = select(playlog).where(playlog.c.user == aime_id)

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()
    
    def put_playlog(self, aime_id: int, playlog_data: Dict) -> Optional[int]:
        playlog_data["user"] = aime_id
        playlog_data = self.fix_bools(playlog_data)

        sql = insert(playlog).values(**playlog_data)
        conflict = sql.on_duplicate_key_update(**playlog_data)

        result = self.execute(conflict)
        if result is None: return None
        return result.lastrowid
