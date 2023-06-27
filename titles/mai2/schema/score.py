from typing import Dict, List, Optional
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON, BigInteger
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select
from sqlalchemy.engine import Row
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata
from core.data import cached

best_score = Table(
    "mai2_score_best",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("musicId", Integer),
    Column("level", Integer),
    Column("playCount", Integer),
    Column("achievement", Integer),
    Column("comboStatus", Integer),
    Column("syncStatus", Integer),
    Column("deluxscoreMax", Integer),
    Column("scoreRank", Integer),
    Column("extNum1", Integer, server_default="0"),
    UniqueConstraint("user", "musicId", "level", name="mai2_score_best_uk"),
    mysql_charset="utf8mb4",
)

playlog = Table(
    "mai2_playlog",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("userId", BigInteger),
    Column("orderId", Integer),
    Column("playlogId", BigInteger),
    Column("version", Integer),
    Column("placeId", Integer),
    Column("placeName", String(255)),
    Column("loginDate", BigInteger),
    Column("playDate", String(255)),
    Column("userPlayDate", String(255)),
    Column("type", Integer),
    Column("musicId", Integer),
    Column("level", Integer),
    Column("trackNo", Integer),
    Column("vsMode", Integer),
    Column("vsUserName", String(255)),
    Column("vsStatus", Integer),
    Column("vsUserRating", Integer),
    Column("vsUserAchievement", Integer),
    Column("vsUserGradeRank", Integer),
    Column("vsRank", Integer),
    Column("playerNum", Integer),
    Column("playedUserId1", BigInteger),
    Column("playedUserName1", String(255)),
    Column("playedMusicLevel1", Integer),
    Column("playedUserId2", BigInteger),
    Column("playedUserName2", String(255)),
    Column("playedMusicLevel2", Integer),
    Column("playedUserId3", BigInteger),
    Column("playedUserName3", String(255)),
    Column("playedMusicLevel3", Integer),
    Column("characterId1", Integer),
    Column("characterLevel1", Integer),
    Column("characterAwakening1", Integer),
    Column("characterId2", Integer),
    Column("characterLevel2", Integer),
    Column("characterAwakening2", Integer),
    Column("characterId3", Integer),
    Column("characterLevel3", Integer),
    Column("characterAwakening3", Integer),
    Column("characterId4", Integer),
    Column("characterLevel4", Integer),
    Column("characterAwakening4", Integer),
    Column("characterId5", Integer),
    Column("characterLevel5", Integer),
    Column("characterAwakening5", Integer),
    Column("achievement", Integer),
    Column("deluxscore", Integer),
    Column("scoreRank", Integer),
    Column("maxCombo", Integer),
    Column("totalCombo", Integer),
    Column("maxSync", Integer),
    Column("totalSync", Integer),
    Column("tapCriticalPerfect", Integer),
    Column("tapPerfect", Integer),
    Column("tapGreat", Integer),
    Column("tapGood", Integer),
    Column("tapMiss", Integer),
    Column("holdCriticalPerfect", Integer),
    Column("holdPerfect", Integer),
    Column("holdGreat", Integer),
    Column("holdGood", Integer),
    Column("holdMiss", Integer),
    Column("slideCriticalPerfect", Integer),
    Column("slidePerfect", Integer),
    Column("slideGreat", Integer),
    Column("slideGood", Integer),
    Column("slideMiss", Integer),
    Column("touchCriticalPerfect", Integer),
    Column("touchPerfect", Integer),
    Column("touchGreat", Integer),
    Column("touchGood", Integer),
    Column("touchMiss", Integer),
    Column("breakCriticalPerfect", Integer),
    Column("breakPerfect", Integer),
    Column("breakGreat", Integer),
    Column("breakGood", Integer),
    Column("breakMiss", Integer),
    Column("isTap", Boolean),
    Column("isHold", Boolean),
    Column("isSlide", Boolean),
    Column("isTouch", Boolean),
    Column("isBreak", Boolean),
    Column("isCriticalDisp", Boolean),
    Column("isFastLateDisp", Boolean),
    Column("fastCount", Integer),
    Column("lateCount", Integer),
    Column("isAchieveNewRecord", Boolean),
    Column("isDeluxscoreNewRecord", Boolean),
    Column("comboStatus", Integer),
    Column("syncStatus", Integer),
    Column("isClear", Boolean),
    Column("beforeRating", Integer),
    Column("afterRating", Integer),
    Column("beforeGrade", Integer),
    Column("afterGrade", Integer),
    Column("afterGradeRank", Integer),
    Column("beforeDeluxRating", Integer),
    Column("afterDeluxRating", Integer),
    Column("isPlayTutorial", Boolean),
    Column("isEventMode", Boolean),
    Column("isFreedomMode", Boolean),
    Column("playMode", Integer),
    Column("isNewFree", Boolean),
    Column("extNum1", Integer),
    Column("extNum2", Integer),
    Column("extNum4", Integer, server_default="0"),
    Column("trialPlayAchievement", Integer),
    mysql_charset="utf8mb4",
)

course = Table(
    "mai2_score_course",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("courseId", Integer),
    Column("isLastClear", Boolean),
    Column("totalRestlife", Integer),
    Column("totalAchievement", Integer),
    Column("totalDeluxscore", Integer),
    Column("playCount", Integer),
    Column("clearDate", String(25)),
    Column("lastPlayDate", String(25)),
    Column("bestAchievement", Integer),
    Column("bestAchievementDate", String(25)),
    Column("bestDeluxscore", Integer),
    Column("bestDeluxscoreDate", String(25)),
    UniqueConstraint("user", "courseId", name="mai2_score_best_uk"),
    mysql_charset="utf8mb4",
)

playlog_old = Table(
    "maimai_playlog",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer),
    # Pop access code
    Column("orderId", Integer),
    Column("sortNumber", Integer),
    Column("placeId", Integer),
    Column("placeName", String(255)),
    Column("country", String(255)),
    Column("regionId", Integer),
    Column("playDate", String(255)),
    Column("userPlayDate", String(255)),
    Column("musicId", Integer),
    Column("level", Integer),
    Column("gameMode", Integer),
    Column("rivalNum", Integer),
    Column("track", Integer),
    Column("eventId", Integer),
    Column("isFreeToPlay", Boolean),
    Column("playerRating", Integer),
    Column("playedUserId1", Integer),
    Column("playedUserId2", Integer),
    Column("playedUserId3", Integer),
    Column("playedUserName1", String(255)),
    Column("playedUserName2", String(255)),
    Column("playedUserName3", String(255)),
    Column("playedMusicLevel1", Integer),
    Column("playedMusicLevel2", Integer),
    Column("playedMusicLevel3", Integer),
    Column("achievement", Integer),
    Column("score", Integer),
    Column("tapScore", Integer),
    Column("holdScore", Integer),
    Column("slideScore", Integer),
    Column("breakScore", Integer),
    Column("syncRate", Integer),
    Column("vsWin", Integer),
    Column("isAllPerfect", Boolean),
    Column("fullCombo", Integer),
    Column("maxFever", Integer),
    Column("maxCombo", Integer),
    Column("tapPerfect", Integer),
    Column("tapGreat", Integer),
    Column("tapGood", Integer),
    Column("tapBad", Integer),
    Column("holdPerfect", Integer),
    Column("holdGreat", Integer),
    Column("holdGood", Integer),
    Column("holdBad", Integer),
    Column("slidePerfect", Integer),
    Column("slideGreat", Integer),
    Column("slideGood", Integer),
    Column("slideBad", Integer),
    Column("breakPerfect", Integer),
    Column("breakGreat", Integer),
    Column("breakGood", Integer),
    Column("breakBad", Integer),
    Column("judgeStyle", Integer),
    Column("isTrackSkip", Boolean),
    Column("isHighScore", Boolean),
    Column("isChallengeTrack", Boolean),
    Column("challengeLife", Integer),
    Column("challengeRemain", Integer),
    Column("isAllPerfectPlus", Integer),
    mysql_charset="utf8mb4",
)

best_score_old = Table(
    "maimai_score_best",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("musicId", Integer),
    Column("level", Integer),
    Column("playCount", Integer),
    Column("achievement", Integer),
    Column("scoreMax", Integer),
    Column("syncRateMax", Integer),
    Column("isAllPerfect", Boolean),
    Column("isAllPerfectPlus", Integer),
    Column("fullCombo", Integer),
    Column("maxFever", Integer),
    UniqueConstraint("user", "musicId", "level", name="maimai_score_best_uk"),
    mysql_charset="utf8mb4",
)

class Mai2ScoreData(BaseData):
    def put_best_score(self, user_id: int, score_data: Dict) -> Optional[int]:
        score_data["user"] = user_id
        sql = insert(best_score).values(**score_data)

        conflict = sql.on_duplicate_key_update(**score_data)

        result = self.execute(conflict)
        if result is None:
            self.logger.error(
                f"put_best_score:  Failed to insert best score! user_id {user_id}"
            )
            return None
        return result.lastrowid

    @cached(2)
    def get_best_scores(self, user_id: int, song_id: int = None) -> Optional[List[Row]]:
        sql = best_score.select(
            and_(
                best_score.c.user == user_id,
                (best_score.c.song_id == song_id) if song_id is not None else True,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_best_score(
        self, user_id: int, song_id: int, chart_id: int
    ) -> Optional[Row]:
        sql = best_score.select(
            and_(
                best_score.c.user == user_id,
                best_score.c.song_id == song_id,
                best_score.c.chart_id == chart_id,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_playlog(self, user_id: int, playlog_data: Dict) -> Optional[int]:
        playlog_data["user"] = user_id
        sql = insert(playlog).values(**playlog_data)

        conflict = sql.on_duplicate_key_update(**playlog_data)

        result = self.execute(conflict)
        if result is None:
            self.logger.error(f"put_playlog:  Failed to insert! user_id {user_id}")
            return None
        return result.lastrowid

    def put_course(self, user_id: int, course_data: Dict) -> Optional[int]:
        course_data["user"] = user_id
        sql = insert(course).values(**course_data)

        conflict = sql.on_duplicate_key_update(**course_data)

        result = self.execute(conflict)
        if result is None:
            self.logger.error(f"put_course:  Failed to insert! user_id {user_id}")
            return None
        return result.lastrowid

    def get_courses(self, user_id: int) -> Optional[List[Row]]:
        sql = course.select(course.c.user == user_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()
