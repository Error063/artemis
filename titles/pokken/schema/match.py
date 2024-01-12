from typing import Optional, Dict, List
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_, case
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select, update, delete
from sqlalchemy.engine import Row
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

# Pokken sends depressingly little match data...
match_data = Table(
    "pokken_match_data",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("num_games", Integer),
    Column("play_modes", JSON),
    Column("results", JSON),
    Column("ex_ko_num", Integer),
    Column("wko_num", Integer),
    Column("timeup_win_num", Integer),
    Column("cool_ko_num", Integer),
    Column("perfect_ko_num", Integer),
    Column("use_navi", Integer),
    Column("use_navi_cloth", Integer),
    Column("use_aid_skill", Integer),
    Column("play_date", TIMESTAMP),
    mysql_charset="utf8mb4",
)


class PokkenMatchData(BaseData):
    """
    Match logs
    """

    async def save_match(self, user_id: int, match_data: Dict) -> Optional[int]:
        pass

    async def get_match(self, match_id: int) -> Optional[Row]:
        pass

    async def get_matches_by_user(self, user_id: int) -> Optional[List[Row]]:
        pass

    async def get_matches(self, limit: int = 20) -> Optional[List[Row]]:
        pass
