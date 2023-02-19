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
    Column("user", ForeignKey("aime_user.id", ondelete="cascade",
           onupdate="cascade"), nullable=False),
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
    Column("use_pv_chn_sld_se_eqp", Boolean,
           nullable=False, server_default="0"),
    Column("use_pv_sldr_tch_se_eqp", Boolean,
           nullable=False, server_default="0"),
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
    Column("my_qst_id", String(
        128), server_default="-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"),
    Column("my_qst_sts", String(
        128), server_default="-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"),
    UniqueConstraint("user", "version", name="diva_profile_uk"),
    mysql_charset='utf8mb4'
)


class DivaProfileData(BaseData):
    def create_profile(self, version: int, aime_id: int,
                       player_name: str) -> Optional[int]:
        """
        Given a game version, aime id, and player_name, create a profile and return it's ID
        """
        sql = insert(profile).values(
            version=version,
            user=aime_id,
            player_name=player_name
        )

        conflict = sql.on_duplicate_key_update(
            player_name=sql.inserted.player_name
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.error(
                f"{__name__} Failed to insert diva profile! aime id: {aime_id} username: {player_name}")
            return None
        return result.lastrowid

    def update_profile(self, profile_updated: Dict) -> None:
        sql = profile.update(profile.c.user == profile_updated["user"]).values(
            player_name=profile_updated["player_name"],
            lv_num=profile_updated["lv_num"],
            lv_pnt=profile_updated["lv_pnt"],
            vcld_pts=profile_updated["vcld_pts"],
            hp_vol=profile_updated["hp_vol"],
            btn_se_vol=profile_updated["btn_se_vol"],
            btn_se_vol2=profile_updated["btn_se_vol2"],
            sldr_se_vol2=profile_updated["sldr_se_vol2"],
            sort_kind=profile_updated["sort_kind"],
            nxt_pv_id=profile_updated["nxt_pv_id"],
            nxt_dffclty=profile_updated["nxt_dffclty"],
            nxt_edtn=profile_updated["nxt_edtn"],
            dsp_clr_brdr=profile_updated["dsp_clr_brdr"],
            dsp_intrm_rnk=profile_updated["dsp_intrm_rnk"],
            dsp_clr_sts=profile_updated["dsp_clr_sts"],
            rgo_sts=profile_updated["rgo_sts"],
            lv_efct_id=profile_updated["lv_efct_id"],
            lv_plt_id=profile_updated["lv_plt_id"],
            my_qst_id=profile_updated["my_qst_id"],
            my_qst_sts=profile_updated["my_qst_sts"],
            passwd_stat=profile_updated["passwd_stat"],
            passwd=profile_updated["passwd"]
        )

        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"update_profile: failed to update profile! profile: {profile_id}")
        return None

    def get_profile(self, aime_id: int, version: int) -> Optional[List[Dict]]:
        """
        Given a game version and either a profile or aime id, return the profile
        """
        sql = profile.select(and_(
            profile.c.version == version,
            profile.c.user == aime_id
        ))

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()
