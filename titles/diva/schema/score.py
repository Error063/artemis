from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, JSON, Boolean
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import insert
from typing import Optional, List, Dict, Any

from core.data.schema import BaseData, metadata
from core.data import cached

score = Table(
    "diva_score",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade"), nullable=False),
    Column("version", Integer),
    Column("pv_id", Integer),
    Column("difficulty", Integer),
    Column("score", Integer),
    Column("atn_pnt", Integer),
    Column("clr_kind", Integer),
    Column("sort_kind", Integer),
    Column("cool", Integer),
    Column("fine", Integer),
    Column("safe", Integer),
    Column("sad", Integer),
    Column("worst", Integer),
    Column("max_combo", Integer),
    UniqueConstraint("user", "pv_id", "difficulty", name="diva_score_uk"),
    mysql_charset='utf8mb4'
)

playlog = Table(
    "diva_playlog",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade"), nullable=False),
    Column("version", Integer),
    Column("pv_id", Integer),
    Column("difficulty", Integer),
    Column("score", Integer),
    Column("atn_pnt", Integer),
    Column("clr_kind", Integer),
    Column("sort_kind", Integer),
    Column("cool", Integer),
    Column("fine", Integer),
    Column("safe", Integer),
    Column("sad", Integer),
    Column("worst", Integer),
    Column("max_combo", Integer),
    Column("date_scored", TIMESTAMP, server_default=func.now()),
    mysql_charset='utf8mb4'
)

class DivaScoreData(BaseData):
    def put_best_score(self, user_id: int, game_version: int, song_id: int, difficulty: int, song_score: int, atn_pnt: int, 
        clr_kind: int, sort_kind:int, cool: int, fine: int, safe: int, sad: int, worst: int, max_combo: int) -> Optional[int]:
        """
        Update the user's best score for a chart
        """
        sql = insert(score).values(
            user=user_id,
            version=game_version,
            pv_id = song_id,
            difficulty=difficulty,
            score=song_score,
            atn_pnt = atn_pnt,
            clr_kind = clr_kind,
            sort_kind = sort_kind,
            cool = cool,
            fine = fine,
            safe = safe,
            sad = sad,
            worst = worst,
            max_combo = max_combo,
        )

        conflict = sql.on_duplicate_key_update(
            score=song_score,
            atn_pnt = atn_pnt,
            clr_kind = clr_kind,
            sort_kind = sort_kind,
            cool = cool,
            fine = fine,
            safe = safe,
            sad = sad,
            worst = worst,
            max_combo = max_combo,
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.error(f"{__name__} failed to insert best score! profile: {user_id}, song: {song_id}")
            return None
        
        return result.lastrowid
    
    def put_playlog(self, user_id: int, game_version: int, song_id: int, difficulty: int, song_score: int, atn_pnt: int,
        clr_kind: int, sort_kind:int, cool: int, fine: int, safe: int, sad: int, worst: int, max_combo: int) -> Optional[int]:
        """
        Add an entry to the user's play log
        """
        sql = playlog.insert().values(
            user=user_id,
            version=game_version,
            pv_id = song_id,
            difficulty=difficulty,
            score=song_score,
            atn_pnt = atn_pnt,
            clr_kind = clr_kind,
            sort_kind = sort_kind,
            cool = cool,
            fine = fine,
            safe = safe,
            sad = sad,
            worst = worst,
            max_combo = max_combo
        )

        result = self.execute(sql)
        if result is None:
            self.logger.error(f"{__name__} failed to insert playlog! profile: {user_id}, song: {song_id}, chart: {difficulty}")
            return None
        
        return result.lastrowid

    def get_best_score(self, user_id: int, pv_id: int, chart_id: int) -> Optional[Dict]:
        sql = score.select(
            and_(score.c.user == user_id, score.c.pv_id == pv_id, score.c.difficulty == chart_id)
        )

        result = self.execute(sql)
        if result is None: return None
        return result.fetchone()

    def get_best_scores(self, user_id: int) -> Optional[Dict]:
        sql = score.select(score.c.user == user_id)

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()