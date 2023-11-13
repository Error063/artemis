from typing import Dict, List, Optional
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON, BigInteger
from sqlalchemy.engine.base import Connection
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select
from sqlalchemy.engine import Row
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata
from core.config import CoreConfig

profile = Table(
    "idac_profile",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("username", String(8)),
    Column("country", Integer),
    Column("store", Integer),
    Column("team_id", Integer, server_default="0"),
    Column("total_play", Integer, server_default="0"),
    Column("daily_play", Integer, server_default="0"),
    Column("day_play", Integer, server_default="0"),
    Column("mileage", Integer, server_default="0"),
    Column("asset_version", Integer, server_default="1"),
    Column("last_play_date", TIMESTAMP, server_default=func.now()),
    Column("mytitle_id", Integer, server_default="0"),
    Column("mytitle_efffect_id", Integer, server_default="0"),
    Column("sticker_id", Integer, server_default="0"),
    Column("sticker_effect_id", Integer, server_default="0"),
    Column("papercup_id", Integer, server_default="0"),
    Column("tachometer_id", Integer, server_default="0"),
    Column("aura_id", Integer, server_default="0"),
    Column("aura_color_id", Integer, server_default="0"),
    Column("aura_line_id", Integer, server_default="0"),
    Column("bgm_id", Integer, server_default="0"),
    Column("keyholder_id", Integer, server_default="0"),
    Column("start_menu_bg_id", Integer, server_default="0"),
    Column("use_car_id", Integer, server_default="1"),
    Column("use_style_car_id", Integer, server_default="1"),
    Column("bothwin_count", Integer, server_default="0"),
    Column("bothwin_score", Integer, server_default="0"),
    Column("subcard_count", Integer, server_default="0"),
    Column("vs_history", Integer, server_default="0"),
    Column("stamp_key_assign_0", Integer),
    Column("stamp_key_assign_1", Integer),
    Column("stamp_key_assign_2", Integer),
    Column("stamp_key_assign_3", Integer),
    Column("name_change_category", Integer, server_default="0"),
    Column("factory_disp", Integer, server_default="0"),
    Column("create_date", TIMESTAMP, server_default=func.now()),
    Column("cash", Integer, server_default="0"),
    Column("dressup_point", Integer, server_default="0"),
    Column("avatar_point", Integer, server_default="0"),
    Column("total_cash", Integer, server_default="0"),
    UniqueConstraint("user", "version", name="idac_profile_uk"),
    mysql_charset="utf8mb4",
)

# No point setting defaults since the game sends everything on profile creation anyway
config = Table(
    "idac_profile_config",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("config_id", Integer),
    Column("steering_intensity", Integer),
    Column("transmission_type", Integer),
    Column("default_viewpoint", Integer),
    Column("favorite_bgm", Integer),
    Column("bgm_volume", Integer),
    Column("se_volume", Integer),
    Column("master_volume", Integer),
    Column("store_battle_policy", Integer),
    Column("battle_onomatope_display", Integer),
    Column("cornering_guide", Integer),
    Column("minimap", Integer),
    Column("line_guide", Integer),
    Column("ghost", Integer),
    Column("race_exit", Integer),
    Column("result_skip", Integer),
    Column("stamp_select_skip", Integer),
    UniqueConstraint("user", name="idac_profile_config_uk"),
    mysql_charset="utf8mb4",
)

# No point setting defaults since the game sends everything on profile creation anyway
avatar = Table(
    "idac_profile_avatar",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("sex", Integer),
    Column("face", Integer),
    Column("eye", Integer),
    Column("mouth", Integer),
    Column("hair", Integer),
    Column("glasses", Integer),
    Column("face_accessory", Integer),
    Column("body", Integer),
    Column("body_accessory", Integer),
    Column("behind", Integer),
    Column("bg", Integer),
    Column("effect", Integer),
    Column("special", Integer),
    UniqueConstraint("user", name="idac_profile_avatar_uk"),
    mysql_charset="utf8mb4",
)

rank = Table(
    "idac_profile_rank",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("story_rank_exp", Integer, server_default="0"),
    Column("story_rank", Integer, server_default="1"),
    Column("time_trial_rank_exp", Integer, server_default="0"),
    Column("time_trial_rank", Integer, server_default="1"),
    Column("online_battle_rank_exp", Integer, server_default="0"),
    Column("online_battle_rank", Integer, server_default="1"),
    Column("store_battle_rank_exp", Integer, server_default="0"),
    Column("store_battle_rank", Integer, server_default="1"),
    Column("theory_exp", Integer, server_default="0"),
    Column("theory_rank", Integer, server_default="1"),
    Column("pride_group_id", Integer, server_default="0"),
    Column("pride_point", Integer, server_default="0"),
    Column("grade_exp", Integer, server_default="0"),
    Column("grade", Integer, server_default="1"),
    Column("grade_reward_dist", Integer, server_default="0"),
    Column("story_rank_reward_dist", Integer, server_default="0"),
    Column("time_trial_rank_reward_dist", Integer, server_default="0"),
    Column("online_battle_rank_reward_dist", Integer, server_default="0"),
    Column("store_battle_rank_reward_dist", Integer, server_default="0"),
    Column("theory_rank_reward_dist", Integer, server_default="0"),
    Column("max_attained_online_battle_rank", Integer, server_default="1"),
    Column("max_attained_pride_point", Integer, server_default="0"),
    Column("is_last_max", Integer, server_default="0"),
    UniqueConstraint("user", "version", name="idac_profile_rank_uk"),
    mysql_charset="utf8mb4",
)

stock = Table(
    "idac_profile_stock",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("mytitle_list", String(1024), server_default=""),
    Column("mytitle_new_list", String(1024), server_default=""),
    Column("avatar_face_list", String(255), server_default=""),
    Column("avatar_face_new_list", String(255), server_default=""),
    Column("avatar_eye_list", String(255), server_default=""),
    Column("avatar_eye_new_list", String(255), server_default=""),
    Column("avatar_hair_list", String(255), server_default=""),
    Column("avatar_hair_new_list", String(255), server_default=""),
    Column("avatar_body_list", String(255), server_default=""),
    Column("avatar_body_new_list", String(255), server_default=""),
    Column("avatar_mouth_list", String(255), server_default=""),
    Column("avatar_mouth_new_list", String(255), server_default=""),
    Column("avatar_glasses_list", String(255), server_default=""),
    Column("avatar_glasses_new_list", String(255), server_default=""),
    Column("avatar_face_accessory_list", String(255), server_default=""),
    Column("avatar_face_accessory_new_list", String(255), server_default=""),
    Column("avatar_body_accessory_list", String(255), server_default=""),
    Column("avatar_body_accessory_new_list", String(255), server_default=""),
    Column("avatar_behind_list", String(255), server_default=""),
    Column("avatar_behind_new_list", String(255), server_default=""),
    Column("avatar_bg_list", String(255), server_default=""),
    Column("avatar_bg_new_list", String(255), server_default=""),
    Column("avatar_effect_list", String(255), server_default=""),
    Column("avatar_effect_new_list", String(255), server_default=""),
    Column("avatar_special_list", String(255), server_default=""),
    Column("avatar_special_new_list", String(255), server_default=""),
    Column("stamp_list", String(255), server_default=""),
    Column("stamp_new_list", String(255), server_default=""),
    Column("keyholder_list", String(256), server_default=""),
    Column("keyholder_new_list", String(256), server_default=""),
    Column("papercup_list", String(255), server_default=""),
    Column("papercup_new_list", String(255), server_default=""),
    Column("tachometer_list", String(255), server_default=""),
    Column("tachometer_new_list", String(255), server_default=""),
    Column("aura_list", String(255), server_default=""),
    Column("aura_new_list", String(255), server_default=""),
    Column("aura_color_list", String(255), server_default=""),
    Column("aura_color_new_list", String(255), server_default=""),
    Column("aura_line_list", String(255), server_default=""),
    Column("aura_line_new_list", String(255), server_default=""),
    Column("bgm_list", String(255), server_default=""),
    Column("bgm_new_list", String(255), server_default=""),
    Column("dx_color_list", String(255), server_default=""),
    Column("dx_color_new_list", String(255), server_default=""),
    Column("start_menu_bg_list", String(255), server_default=""),
    Column("start_menu_bg_new_list", String(255), server_default=""),
    Column("under_neon_list", String(255), server_default=""),
    UniqueConstraint("user", "version", name="idac_profile_stock_uk"),
    mysql_charset="utf8mb4",
)

theory = Table(
    "idac_profile_theory",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("play_count", Integer, server_default="0"),
    Column("play_count_multi", Integer, server_default="0"),
    Column("partner_id", Integer),
    Column("partner_progress", Integer),
    Column("partner_progress_score", Integer),
    Column("practice_start_rank", Integer, server_default="0"),
    Column("general_flag", Integer, server_default="0"),
    Column("vs_history", Integer, server_default="0"),
    Column("vs_history_multi", Integer, server_default="0"),
    Column("win_count", Integer, server_default="0"),
    Column("win_count_multi", Integer, server_default="0"),
    UniqueConstraint("user", "version", name="idac_profile_theory_uk"),
    mysql_charset="utf8mb4",
)


class IDACProfileData(BaseData):
    def __init__(self, cfg: CoreConfig, conn: Connection) -> None:
        super().__init__(cfg, conn)
        self.date_time_format_ext = (
            "%Y-%m-%d %H:%M:%S.%f"  # needs to be lopped off at [:-5]
        )
        self.date_time_format_short = "%Y-%m-%d"

    def get_profile(self, aime_id: int, version: int) -> Optional[Row]:
        sql = select(profile).where(
            and_(
                profile.c.user == aime_id,
                profile.c.version == version,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_different_random_profiles(
        self, aime_id: int, version: int, count: int = 9
    ) -> Optional[Row]:
        sql = (
            select(profile)
            .where(
                and_(
                    profile.c.user != aime_id,
                    profile.c.version == version,
                )
            )
            .order_by(func.rand())
            .limit(count)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_profile_config(self, aime_id: int) -> Optional[Row]:
        sql = select(config).where(
            and_(
                config.c.user == aime_id,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_profile_avatar(self, aime_id: int) -> Optional[Row]:
        sql = select(avatar).where(
            and_(
                avatar.c.user == aime_id,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_profile_rank(self, aime_id: int, version: int) -> Optional[Row]:
        sql = select(rank).where(
            and_(
                rank.c.user == aime_id,
                rank.c.version == version,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_profile_stock(self, aime_id: int, version: int) -> Optional[Row]:
        sql = select(stock).where(
            and_(
                stock.c.user == aime_id,
                stock.c.version == version,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_profile_theory(self, aime_id: int, version: int) -> Optional[Row]:
        sql = select(theory).where(
            and_(
                theory.c.user == aime_id,
                theory.c.version == version,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_profile(
        self, aime_id: int, version: int, profile_data: Dict
    ) -> Optional[int]:
        profile_data["user"] = aime_id
        profile_data["version"] = version

        sql = insert(profile).values(**profile_data)
        conflict = sql.on_duplicate_key_update(**profile_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_profile: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def put_profile_config(self, aime_id: int, config_data: Dict) -> Optional[int]:
        config_data["user"] = aime_id

        sql = insert(config).values(**config_data)
        conflict = sql.on_duplicate_key_update(**config_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(
                f"put_profile_config: Failed to update! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid

    def put_profile_avatar(self, aime_id: int, avatar_data: Dict) -> Optional[int]:
        avatar_data["user"] = aime_id

        sql = insert(avatar).values(**avatar_data)
        conflict = sql.on_duplicate_key_update(**avatar_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(
                f"put_profile_avatar: Failed to update! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid

    def put_profile_rank(
        self, aime_id: int, version: int, rank_data: Dict
    ) -> Optional[int]:
        rank_data["user"] = aime_id
        rank_data["version"] = version

        sql = insert(rank).values(**rank_data)
        conflict = sql.on_duplicate_key_update(**rank_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_profile_rank: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def put_profile_stock(
        self, aime_id: int, version: int, stock_data: Dict
    ) -> Optional[int]:
        stock_data["user"] = aime_id
        stock_data["version"] = version

        sql = insert(stock).values(**stock_data)
        conflict = sql.on_duplicate_key_update(**stock_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_profile_stock: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def put_profile_theory(
        self, aime_id: int, version: int, theory_data: Dict
    ) -> Optional[int]:
        theory_data["user"] = aime_id
        theory_data["version"] = version

        sql = insert(theory).values(**theory_data)
        conflict = sql.on_duplicate_key_update(**theory_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(
                f"put_profile_theory: Failed to update! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid
