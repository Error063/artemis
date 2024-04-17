from typing import Optional, Dict, List
from sqlalchemy import Table, Column, UniqueConstraint, and_
from sqlalchemy.types import Integer, String
from sqlalchemy.schema import ForeignKey
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

pv_customize = Table(
    "diva_profile_pv_customize",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("pv_id", Integer, nullable=False),
    Column("mdl_eqp_ary", String(14), server_default="-999,-999,-999"),
    Column(
        "c_itm_eqp_ary",
        String(59),
        server_default="-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999",
    ),
    Column(
        "ms_itm_flg_ary",
        String(59),
        server_default="-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1",
    ),
    Column("skin", Integer, server_default="-1"),
    Column("btn_se", Integer, server_default="-1"),
    Column("sld_se", Integer, server_default="-1"),
    Column("chsld_se", Integer, server_default="-1"),
    Column("sldtch_se", Integer, server_default="-1"),
    UniqueConstraint("user", "version", "pv_id", name="diva_profile_pv_customize_uk"),
    mysql_charset="utf8mb4",
)


class DivaPvCustomizeData(BaseData):
    async def put_pv_customize(
        self,
        aime_id: int,
        version: int,
        pv_id: int,
        mdl_eqp_ary: str,
        c_itm_eqp_ary: str,
        ms_itm_flg_ary: str,
    ) -> Optional[int]:
        sql = insert(pv_customize).values(
            version=version,
            user=aime_id,
            pv_id=pv_id,
            mdl_eqp_ary=mdl_eqp_ary,
            c_itm_eqp_ary=c_itm_eqp_ary,
            ms_itm_flg_ary=ms_itm_flg_ary,
        )

        conflict = sql.on_duplicate_key_update(
            pv_id=pv_id,
            mdl_eqp_ary=mdl_eqp_ary,
            c_itm_eqp_ary=c_itm_eqp_ary,
            ms_itm_flg_ary=ms_itm_flg_ary,
        )

        result = await self.execute(conflict)
        if result is None:
            self.logger.error(
                f"{__name__} Failed to insert diva pv customize! aime id: {aime_id}"
            )
            return None
        return result.lastrowid

    async def get_pv_customize(self, aime_id: int, pv_id: int) -> Optional[List[Dict]]:
        """
        Given either a profile or aime id, return a Pv Customize row
        """
        sql = pv_customize.select(
            and_(pv_customize.c.user == aime_id, pv_customize.c.pv_id == pv_id)
        )

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()
