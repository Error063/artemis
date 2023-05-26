from typing import Optional, Dict, List
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_, case
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select, update, delete
from sqlalchemy.engine import Row
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata
from ..const import SaoConstants

profile = Table(
    "sao_profile",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
        unique=True,
    ),
    Column("user_type", Integer, server_default="1"),
    Column("nick_name", String(16), server_default="PLAYER"),
    Column("rank_num", Integer, server_default="1"),
    Column("rank_exp", Integer, server_default="0"),
    Column("own_col", Integer, server_default="0"),
    Column("own_vp", Integer, server_default="0"),
    Column("own_yui_medal", Integer, server_default="0"),
    Column("setting_title_id", Integer, server_default="20005"),
)

class SaoProfileData(BaseData):
    def create_profile(self, user_id: int) -> Optional[int]:
        sql = insert(profile).values(user=user_id)
        conflict = sql.on_duplicate_key_update(user=user_id)

        result = self.execute(conflict)
        if result is None:
            self.logger.error(f"Failed to create SAO profile for user {user_id}!")
            return None
        return result.lastrowid

    def get_profile(self, user_id: int) -> Optional[Row]:
        sql = profile.select(profile.c.user == user_id)
        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()