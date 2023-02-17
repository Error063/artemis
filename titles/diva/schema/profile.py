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
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"), nullable=False),
    Column("version", Integer, nullable=False),
    Column("player_name", String(8), nullable=False),
    Column("lv_str", String(24), nullable=False, server_default="Dab on 'em"),
    Column("lv_num", Integer, nullable=False, server_default="0"),
    Column("lv_pnt", Integer, nullable=False, server_default="0"),
    Column("vcld_pts", Integer, nullable=False, server_default="0"),
    Column("hp_vol", Integer, nullable=False, server_default="100"),
    Column("btn_se_vol", Integer, nullable=False, server_default="100"),
    Column("btn_se_vol2", Integer, nullable=False, server_default="100"),
    Column("sldr_se_vol2", Integer, nullable=False, server_default="100"),
    Column("sort_kind", Integer, nullable=False, server_default="2"),
    Column("use_pv_mdl_eqp", String(8), nullable=False, server_default="true"),
    Column("use_pv_btn_se_eqp", String(8), nullable=False, server_default="true"),
    Column("use_pv_sld_se_eqp", String(8), nullable=False, server_default="false"),
    Column("use_pv_chn_sld_se_eqp", String(8), nullable=False, server_default="false"),
    Column("use_pv_sldr_tch_se_eqp", String(8), nullable=False, server_default="false"),
    Column("nxt_pv_id", Integer, nullable=False, server_default="708"),
    Column("nxt_dffclty", Integer, nullable=False, server_default="2"),
    Column("nxt_edtn", Integer, nullable=False, server_default="0"),
    Column("dsp_clr_brdr", Integer, nullable=False, server_default="7"),
    Column("dsp_intrm_rnk", Integer, nullable=False, server_default="1"),
    Column("dsp_clr_sts", Integer, nullable=False, server_default="1"),
    Column("rgo_sts", Integer, nullable=False, server_default="1"),
    Column("lv_efct_id", Integer, nullable=False, server_default="0"),
    Column("lv_plt_id", Integer, nullable=False, server_default="1"),
    Column("my_qst_id", String(128), server_default="-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"),
    Column("my_qst_sts", String(128), server_default="-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"),
    UniqueConstraint("user", "version", name="diva_profile_uk"),
    mysql_charset='utf8mb4'
)

class DivaProfileData(BaseData):
    def create_profile(self, version: int, aime_id: int, player_name: str) -> Optional[int]:
        """
        Given a game version, aime id, and player_name, create a profile and return it's ID
        """
        sql = insert(profile).values(
            version=version,
            user=aime_id,
            player_name=player_name
        )

        conflict = sql.on_duplicate_key_update(
            player_name = sql.inserted.player_name
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.error(f"{__name__} Failed to insert diva profile! aime id: {aime_id} username: {player_name}")
            return None
        return result.lastrowid

    def update_profile(self, profile_id: int, lv_num: int, lv_pnt: int, vcld_pts: int, hp_vol: int, btn_se_vol: int, btn_se_vol2: int, sldr_se_vol2: int, sort_kind: int, use_pv_mdl_eqp: str, use_pv_btn_se_eqp: str, use_pv_sld_se_eqp: str, use_pv_chn_sld_se_eqp: str, use_pv_sldr_tch_se_eqp: str, nxt_pv_id: int, nxt_dffclty: int, nxt_edtn: int, dsp_clr_brdr: int, dsp_intrm_rnk: int, dsp_clr_sts: int, rgo_sts: int, lv_efct_id: int, lv_plt_id: int, my_qst_id: str, my_qst_sts: str) -> None:
        sql = profile.update(profile.c.user == profile_id).values(

            lv_num = lv_num,
            lv_pnt = lv_pnt,
            vcld_pts = vcld_pts,
            hp_vol = hp_vol,
            btn_se_vol = btn_se_vol,
            btn_se_vol2 = btn_se_vol2,
            sldr_se_vol2 = sldr_se_vol2,
            sort_kind = sort_kind,
            use_pv_mdl_eqp = use_pv_mdl_eqp,
            use_pv_btn_se_eqp = use_pv_btn_se_eqp,
            use_pv_sld_se_eqp = use_pv_sld_se_eqp,
            use_pv_chn_sld_se_eqp = use_pv_chn_sld_se_eqp,
            use_pv_sldr_tch_se_eqp = use_pv_sldr_tch_se_eqp,
            nxt_pv_id = nxt_pv_id,
            nxt_dffclty = nxt_dffclty,
            nxt_edtn = nxt_edtn,
            dsp_clr_brdr = dsp_clr_brdr,
            dsp_intrm_rnk = dsp_intrm_rnk,
            dsp_clr_sts = dsp_clr_sts,
            rgo_sts = rgo_sts,
            lv_efct_id = lv_efct_id,
            lv_plt_id = lv_plt_id,
            my_qst_id = my_qst_id,
            my_qst_sts = my_qst_sts

        )

        result = self.execute(sql)
        if result is None: 
            self.logger.error(f"update_profile: failed to update profile! profile: {profile_id}")
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
        if result is None: return None
        return result.fetchone()
