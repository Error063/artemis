from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, JSON, Boolean
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import insert
from typing import Optional, List, Dict, Any

from core.data.schema import BaseData, metadata
from core.data import cached

score = Table(
    "cxb_score",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade"), nullable=False),
    Column("game_version", Integer),
    Column("song_mcode", String(7)),
    Column("song_index", Integer),
    Column("data", JSON),
    UniqueConstraint("user", "song_mcode", "song_index", name="cxb_score_uk"),
    mysql_charset="utf8mb4",
)

playlog = Table(
    "cxb_playlog",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade"), nullable=False),
    Column("song_mcode", String(7)),
    Column("chart_id", Integer),
    Column("score", Integer),
    Column("clear", Integer),
    Column("flawless", Integer),
    Column("super", Integer),
    Column("cool", Integer),
    Column("fast", Integer),
    Column("fast2", Integer),
    Column("slow", Integer),
    Column("slow2", Integer),
    Column("fail", Integer),
    Column("combo", Integer),
    Column("date_scored", TIMESTAMP, server_default=func.now()),
    mysql_charset="utf8mb4",
)

ranking = Table(
    "cxb_ranking",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade"), nullable=False),
    Column("rev_id", Integer),
    Column("song_id", Integer),
    Column("score", Integer),
    Column("clear", Integer),
    UniqueConstraint("user", "rev_id", name="cxb_ranking_uk"),
    mysql_charset="utf8mb4",
)


class CxbScoreData(BaseData):
    def put_best_score(
        self,
        user_id: int,
        song_mcode: str,
        game_version: int,
        song_index: int,
        data: JSON,
    ) -> Optional[int]:
        """
        Update the user's best score for a chart
        """
        sql = insert(score).values(
            user=user_id,
            song_mcode=song_mcode,
            game_version=game_version,
            song_index=song_index,
            data=data,
        )

        conflict = sql.on_duplicate_key_update(data=sql.inserted.data)

        result = self.execute(conflict)
        if result is None:
            self.logger.error(
                f"{__name__} failed to insert best score! profile: {user_id}, song: {song_mcode}, data: {data}"
            )
            return None

        return result.lastrowid

    def put_playlog(
        self,
        user_id: int,
        song_mcode: str,
        chart_id: int,
        score: int,
        clear: int,
        flawless: int,
        this_super: int,
        cool: int,
        this_fast: int,
        this_fast2: int,
        this_slow: int,
        this_slow2: int,
        fail: int,
        combo: int,
    ) -> Optional[int]:
        """
        Add an entry to the user's play log
        """
        sql = playlog.insert().values(
            user=user_id,
            song_mcode=song_mcode,
            chart_id=chart_id,
            score=score,
            clear=clear,
            flawless=flawless,
            super=this_super,
            cool=cool,
            fast=this_fast,
            fast2=this_fast2,
            slow=this_slow,
            slow2=this_slow2,
            fail=fail,
            combo=combo,
        )

        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"{__name__} failed to insert playlog! profile: {user_id}, song: {song_mcode}, chart: {chart_id}"
            )
            return None

        return result.lastrowid

    def put_ranking(
        self, user_id: int, rev_id: int, song_id: int, score: int, clear: int
    ) -> Optional[int]:
        """
        Add an entry to the user's ranking logs
        """
        if song_id == 0:
            sql = insert(ranking).values(
                user=user_id, rev_id=rev_id, score=score, clear=clear
            )
        else:
            sql = insert(ranking).values(
                user=user_id, rev_id=rev_id, song_id=song_id, score=score, clear=clear
            )

        conflict = sql.on_duplicate_key_update(score=score)

        result = self.execute(conflict)
        if result is None:
            self.logger.error(
                f"{__name__} failed to insert ranking log! profile: {user_id}, score: {score}, clear: {clear}"
            )
            return None

        return result.lastrowid

    def get_best_score(self, user_id: int, song_mcode: int) -> Optional[Dict]:
        sql = score.select(
            and_(score.c.user == user_id, score.c.song_mcode == song_mcode)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_best_scores(self, user_id: int) -> Optional[Dict]:
        sql = score.select(score.c.user == user_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_best_rankings(self, user_id: int) -> Optional[List[Dict]]:
        sql = ranking.select(ranking.c.user == user_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()
