from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, JSON, Boolean
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select
from sqlalchemy.engine import Row
from sqlalchemy.dialects.mysql import insert
from typing import Optional, List, Dict, Any

from core.data.schema import BaseData, metadata
from core.data import cached

best_score = Table(
    "wacca_score_best",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"), nullable=False),
    Column("song_id", Integer),
    Column("chart_id", Integer),    
    Column("score", Integer),
    Column("play_ct", Integer),
    Column("clear_ct", Integer),
    Column("missless_ct", Integer),
    Column("fullcombo_ct", Integer),
    Column("allmarv_ct", Integer),
    Column("grade_d_ct", Integer),
    Column("grade_c_ct", Integer),
    Column("grade_b_ct", Integer),
    Column("grade_a_ct", Integer),
    Column("grade_aa_ct", Integer),
    Column("grade_aaa_ct", Integer),
    Column("grade_s_ct", Integer),
    Column("grade_ss_ct", Integer),
    Column("grade_sss_ct", Integer),
    Column("grade_master_ct", Integer),
    Column("grade_sp_ct", Integer),
    Column("grade_ssp_ct", Integer),
    Column("grade_sssp_ct", Integer),
    Column("best_combo", Integer),
    Column("lowest_miss_ct", Integer),
    Column("rating", Integer),
    UniqueConstraint("user", "song_id", "chart_id", name="wacca_score_uk"),
    mysql_charset='utf8mb4'
)

playlog = Table(
    "wacca_score_playlog",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"), nullable=False),
    Column("song_id", Integer),
    Column("chart_id", Integer),
    Column("score", Integer),
    Column("clear", Integer),
    Column("grade", Integer),
    Column("max_combo", Integer),
    Column("marv_ct", Integer),
    Column("great_ct", Integer),
    Column("good_ct", Integer),
    Column("miss_ct", Integer),
    Column("fast_ct", Integer),
    Column("late_ct", Integer),
    Column("season", Integer),
    Column("date_scored", TIMESTAMP, server_default=func.now()),
    mysql_charset='utf8mb4'
)

stageup = Table(
    "wacca_score_stageup",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"), nullable=False),
    Column("version", Integer),
    Column("stage_id", Integer),
    Column("clear_status", Integer),
    Column("clear_song_ct", Integer),
    Column("song1_score", Integer),
    Column("song2_score", Integer),
    Column("song3_score", Integer),
    Column("play_ct", Integer, server_default="1"),
    UniqueConstraint("user", "stage_id",  name="wacca_score_stageup_uk"),
    mysql_charset='utf8mb4'
)

class WaccaScoreData(BaseData):
    def put_best_score(self, user_id: int, song_id: int, chart_id: int, score: int, clear: List[int], 
        grade: List[int], best_combo: int, lowest_miss_ct: int) -> Optional[int]:
        """
        Update the user's best score for a chart
        """
        while len(grade) < 13:
            grade.append(0)
        
        sql = insert(best_score).values(
            user=user_id,
            song_id=song_id,
            chart_id=chart_id,
            score=score,
            play_ct=clear[0],
            clear_ct=clear[1],
            missless_ct=clear[2],
            fullcombo_ct=clear[3],
            allmarv_ct=clear[4],
            grade_d_ct=grade[0],
            grade_c_ct=grade[1],
            grade_b_ct=grade[2],
            grade_a_ct=grade[3],
            grade_aa_ct=grade[4],
            grade_aaa_ct=grade[5],
            grade_s_ct=grade[6],
            grade_ss_ct=grade[7],
            grade_sss_ct=grade[8],
            grade_master_ct=grade[9],
            grade_sp_ct=grade[10],
            grade_ssp_ct=grade[11],
            grade_sssp_ct=grade[12],
            best_combo=best_combo,
            lowest_miss_ct=lowest_miss_ct,
            rating=0
        )

        conflict = sql.on_duplicate_key_update(
            score=score,
            play_ct=clear[0],
            clear_ct=clear[1],
            missless_ct=clear[2],
            fullcombo_ct=clear[3],
            allmarv_ct=clear[4],
            grade_d_ct=grade[0],
            grade_c_ct=grade[1],
            grade_b_ct=grade[2],
            grade_a_ct=grade[3],
            grade_aa_ct=grade[4],
            grade_aaa_ct=grade[5],
            grade_s_ct=grade[6],
            grade_ss_ct=grade[7],
            grade_sss_ct=grade[8],
            grade_master_ct=grade[9],
            grade_sp_ct=grade[10],
            grade_ssp_ct=grade[11],
            grade_sssp_ct=grade[12],
            best_combo=best_combo,
            lowest_miss_ct=lowest_miss_ct,
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.error(f"{__name__}: failed to insert best score! profile: {user_id}, song: {song_id}, chart: {chart_id}")
            return None
        
        return result.lastrowid
    
    def put_playlog(self, user_id: int, song_id: int, chart_id: int, this_score: int, clear: int, grade: int, max_combo: int, 
        marv_ct: int, great_ct: int, good_ct: int, miss_ct: int, fast_ct: int, late_ct: int, season: int) -> Optional[int]:
        """
        Add an entry to the user's play log
        """
        sql = playlog.insert().values(
            user=user_id,
            song_id=song_id,
            chart_id=chart_id,
            score=this_score,
            clear=clear,
            grade=grade,
            max_combo=max_combo,
            marv_ct=marv_ct,
            great_ct=great_ct,
            good_ct=good_ct,
            miss_ct=miss_ct,
            fast_ct=fast_ct,
            late_ct=late_ct,
            season=season
        )

        result = self.execute(sql)
        if result is None:
            self.logger.error(f"{__name__} failed to insert playlog! profile: {user_id}, song: {song_id}, chart: {chart_id}")
            return None
        
        return result.lastrowid

    def get_best_score(self, user_id: int, song_id: int, chart_id: int) -> Optional[Row]:
        sql = best_score.select(
            and_(best_score.c.user == user_id, best_score.c.song_id == song_id, best_score.c.chart_id == chart_id)
        )

        result = self.execute(sql)
        if result is None: return None
        return result.fetchone()

    def get_best_scores(self, user_id: int) -> Optional[List[Row]]:
        sql = best_score.select(
            best_score.c.user == user_id
        )

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()

    def update_song_rating(self, user_id: int, song_id: int, chart_id: int, new_rating: int) -> None:
        sql = best_score.update(
            and_(
                best_score.c.user == user_id, 
                best_score.c.song_id == song_id, 
                best_score.c.chart_id == chart_id
                )).values(
                rating = new_rating
            )

        result = self.execute(sql)
        if result is None: 
            self.logger.error(f"update_song_rating: failed to update rating! user_id: {user_id} song_id: {song_id} chart_id {chart_id} new_rating {new_rating}")
        return None

    def put_stageup(self, user_id: int, version: int, stage_id: int, clear_status: int, clear_song_ct: int, score1: int, 
        score2: int, score3: int) -> Optional[int]:
        sql = insert(stageup).values(
            user = user_id,
            version = version,
            stage_id = stage_id,
            clear_status = clear_status,
            clear_song_ct = clear_song_ct,
            song1_score = score1,
            song2_score = score2,
            song3_score = score3,
        )

        conflict = sql.on_duplicate_key_update(
            clear_status = clear_status,
            clear_song_ct = clear_song_ct,
            song1_score = score1,
            song2_score = score2,
            song3_score = score3,
            play_ct = stageup.c.play_ct + 1
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(f"put_stageup: failed to update! user_id: {user_id} version: {version} stage_id: {stage_id}")
            return None
        return result.lastrowid

    def get_stageup(self, user_id: int, version: int) -> Optional[List[Row]]:
        sql = select(stageup).where(and_(stageup.c.user==user_id, stageup.c.version==version))

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()
    
    def get_stageup_stage(self, user_id: int, version: int, stage_id: int) -> Optional[Row]:
        sql = select(stageup).where(
            and_(
                stageup.c.user == user_id,
                stageup.c.version == version,
                stageup.c.stage_id == stage_id,
            )
        )

        result = self.execute(sql)
        if result is None: return None
        return result.fetchone()
