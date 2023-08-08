from typing import Dict, Optional
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

gp_log = Table(
    "ongeki_gp_log",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("usedCredit", Integer),
    Column("placeName", String(255)),
    Column("trxnDate", String(255)),
    Column(
        "placeId", Integer
    ),  # Making this an FK would mess with people playing with default KC
    Column("kind", Integer),
    Column("pattern", Integer),
    Column("currentGP", Integer),
    mysql_charset="utf8mb4",
)

session_log = Table(
    "ongeki_session_log",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("sortNumber", Integer),
    Column("placeId", Integer),
    Column("playDate", String(10)),
    Column("userPlayDate", String(25)),
    Column("isPaid", Boolean),
    mysql_charset="utf8mb4",
)


class OngekiLogData(BaseData):
    def put_gp_log(
        self,
        aime_id: Optional[int],
        used_credit: int,
        place_name: str,
        tx_date: str,
        place_id: int,
        kind: int,
        pattern: int,
        current_gp: int,
    ) -> Optional[int]:
        sql = insert(gp_log).values(
            user=aime_id,
            usedCredit=used_credit,
            placeName=place_name,
            trxnDate=tx_date,
            placeId=place_id,
            kind=kind,
            pattern=pattern,
            currentGP=current_gp,
        )

        result = self.execute(sql)
        if result is None:
            self.logger.warning(
                f"put_gp_log: Failed to insert GP log! aime_id: {aime_id} kind {kind} pattern {pattern} current_gp {current_gp}"
            )
        return result.lastrowid
