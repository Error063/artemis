from typing import Optional, Dict, List
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_, case
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

energy = Table(
    "cxb_rev_energy",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade"), nullable=False),
    Column("energy", Integer, nullable=False, server_default="0"),
    UniqueConstraint("user", name="cxb_rev_energy_uk"),
    mysql_charset='utf8mb4'
)

class CxbItemData(BaseData):    
    def put_energy(self, user_id: int, rev_energy: int) -> Optional[int]:
        sql = insert(energy).values(
            user = user_id,
            energy = rev_energy 
        )

        conflict = sql.on_duplicate_key_update(
            energy = rev_energy
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.error(f"{__name__} failed to insert item! user: {user_id}, energy: {rev_energy}")
            return None
        
        return result.lastrowid
    
    def get_energy(self, user_id: int) -> Optional[Dict]:
        sql = energy.select(
            and_(energy.c.user == user_id)
        )

        result = self.execute(sql)
        if result is None: return None
        return result.fetchone()
