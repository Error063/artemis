from typing import Optional, Dict, List
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

profile = Table(
    "diva_profile",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("player_name", String(10), nullable=False),
    Column("lv_str", String(24), nullable=False, server_default="Dab on 'em"),
    Column("lv_num", Integer, nullable=False, server_default="0"),
    Column("lv_pnt", Integer, nullable=False, server_default="0"),
    Column("vcld_pts", Integer, nullable=False, server_default="0"),
    Column("hp_vol", Integer, nullable=False, server_default="100"),
    Column("btn_se_vol", Integer, nullable=False, server_default="100"),
    Column("btn_se_vol2", Integer, nullable=False, server_default="100"),
    Column("sldr_se_vol2", Integer, nullable=False, server_default="100"),
    Column("sort_kind", Integer, nullable=False, server_default="2"),
    Column("use_pv_mdl_eqp", Boolean, nullable=False, server_default="1"),
    Column("use_mdl_pri", Boolean, nullable=False, server_default="0"),
    Column("use_pv_skn_eqp", Boolean, nullable=False, server_default="0"),
    Column("use_pv_btn_se_eqp", Boolean, nullable=False, server_default="1"),
    Column("use_pv_sld_se_eqp", Boolean, nullable=False, server_default="0"),
    Column("use_pv_chn_sld_se_eqp", Boolean, nullable=False, server_default="0"),
    Column("use_pv_sldr_tch_se_eqp", Boolean, nullable=False, server_default="0"),
    Column("nxt_pv_id", Integer, nullable=False, server_default="708"),
    Column("nxt_dffclty", Integer, nullable=False, server_default="2"),
    Column("nxt_edtn", Integer, nullable=False, server_default="0"),
    Column("dsp_clr_brdr", Integer, nullable=False, server_default="7"),
    Column("dsp_intrm_rnk", Integer, nullable=False, server_default="1"),
    Column("dsp_clr_sts", Integer, nullable=False, server_default="1"),
    Column("rgo_sts", Integer, nullable=False, server_default="1"),
    Column("lv_efct_id", Integer, nullable=False, server_default="0"),
    Column("lv_plt_id", Integer, nullable=False, server_default="1"),
    Column("passwd_stat", Integer, nullable=False, server_default="0"),
    Column("passwd", String(12), nullable=False, server_default="**********"),
    Column(
        "my_qst_id",
        String(128),
        server_default="-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1",
    ),
    Column(
        "my_qst_sts",
        String(128),
        server_default="-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1",
    ),
    UniqueConstraint("user", "version", name="diva_profile_uk"),
    mysql_charset="utf8mb4",
)


class DivaProfileData(BaseData):
    def create_profile(
        self, version: int, aime_id: int, player_name: str
    ) -> Optional[int]:
        """
        Given a game version, aime id, and player_name, create a profile and return it's ID
        """
        sql = insert(profile).values(
            version=version, user=aime_id, player_name=player_name
        )

        conflict = sql.on_duplicate_key_update(player_name=sql.inserted.player_name)

        result = self.execute(conflict)
        if result is None:
            self.logger.error(
                f"{__name__} Failed to insert diva profile! aime id: {aime_id} username: {player_name}"
            )
            return None
        return result.lastrowid

    def update_profile(self, aime_id: int, **profile_args) -> None:
        """
        Given an aime_id update the profile corresponding to the arguments
        which are the diva_profile Columns
        """
        sql = profile.update(profile.c.user == aime_id).values(**profile_args)

        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"update_profile: failed to update profile! profile: {aime_id}"
            )
        return None

    def get_profile(self, aime_id: int, version: int) -> Optional[List[Dict]]:
        """
        Given a game version and either a profile or aime id, return the profile
        """
        sql = profile.select(
            and_(profile.c.version == version, profile.c.user == aime_id)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()
