from typing import Optional, Dict, List
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_, case
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

shop = Table(
    "diva_profile_shop",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("mdl_eqp_ary", String(32)),
    Column("c_itm_eqp_ary", String(59)),
    Column("ms_itm_flg_ary", String(59)),
    UniqueConstraint("user", "version", name="diva_profile_shop_uk"),
    mysql_charset="utf8mb4",
)


class DivaItemData(BaseData):
    async def put_shop(
        self,
        aime_id: int,
        version: int,
        mdl_eqp_ary: str,
        c_itm_eqp_ary: str,
        ms_itm_flg_ary: str,
    ) -> None:
        sql = insert(shop).values(
            version=version,
            user=aime_id,
            mdl_eqp_ary=mdl_eqp_ary,
            c_itm_eqp_ary=c_itm_eqp_ary,
            ms_itm_flg_ary=ms_itm_flg_ary,
        )

        conflict = sql.on_duplicate_key_update(
            mdl_eqp_ary=mdl_eqp_ary,
            c_itm_eqp_ary=c_itm_eqp_ary,
            ms_itm_flg_ary=ms_itm_flg_ary,
        )

        result = await self.execute(conflict)
        if result is None:
            self.logger.error(
                f"{__name__} Failed to insert diva profile! aime id: {aime_id} array: {mdl_eqp_ary}"
            )
            return None
        return result.lastrowid

    async def get_shop(self, aime_id: int, version: int) -> Optional[List[Dict]]:
        """
        Given a game version and either a profile or aime id, return the profile
        """
        sql = shop.select(and_(shop.c.version == version, shop.c.user == aime_id))

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()
