from typing import Optional, Dict, List
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_, case
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select, update, delete
from sqlalchemy.engine import Row
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

hero_log_data = Table(
    "sao_hero_log_data",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("user_hero_log_id", Integer, nullable=False),
    Column("log_level", Integer, nullable=False),
    Column("log_exp", Integer, nullable=False),
    Column("main_weapon", Integer, nullable=False),
    Column("sub_equipment", Integer, nullable=False),
    Column("skill_slot1_skill_id", Integer, nullable=False),
    Column("skill_slot2_skill_id", Integer, nullable=False),
    Column("skill_slot3_skill_id", Integer, nullable=False),
    Column("skill_slot4_skill_id", Integer, nullable=False),
    Column("skill_slot5_skill_id", Integer, nullable=False),
    Column("get_date", TIMESTAMP, nullable=False, server_default=func.now()),
    UniqueConstraint("user", "user_hero_log_id", name="sao_hero_log_data_uk"),
    mysql_charset="utf8mb4",
)

hero_party = Table(
    "sao_hero_party",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("user_party_team_id", Integer, nullable=False),
    Column("user_hero_log_id_1", Integer, nullable=False),
    Column("user_hero_log_id_2", Integer, nullable=False),
    Column("user_hero_log_id_3", Integer, nullable=False),
    UniqueConstraint("user", "user_party_team_id", name="sao_hero_party_uk"),
    mysql_charset="utf8mb4",
)

sessions = Table(
    "sao_play_sessions",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("user_party_team_id", Integer, nullable=False),
    Column("episode_id", Integer, nullable=False),
    Column("play_mode", Integer, nullable=False),
    Column("quest_drop_boost_apply_flag", Integer, nullable=False),
    Column("play_date", TIMESTAMP, nullable=False, server_default=func.now()),
    UniqueConstraint("user", "user_party_team_id", "play_date", name="sao_play_sessions_uk"),
    mysql_charset="utf8mb4",
)

class SaoItemData(BaseData):
    def create_session(self, user_id: int, user_party_team_id: int, episode_id: int, play_mode: int, quest_drop_boost_apply_flag: int) -> Optional[int]:
        sql = insert(sessions).values(
            user=user_id,
            user_party_team_id=user_party_team_id,
            episode_id=episode_id,
            play_mode=play_mode,
            quest_drop_boost_apply_flag=quest_drop_boost_apply_flag
            )

        conflict = sql.on_duplicate_key_update(user=user_id)

        result = self.execute(conflict)
        if result is None:
            self.logger.error(f"Failed to create SAO session for user {user_id}!")
            return None
        return result.lastrowid

    def put_hero_log(self, user_id: int, user_hero_log_id: int, log_level: int, log_exp: int, main_weapon: int, sub_equipment: int, skill_slot1_skill_id: int, skill_slot2_skill_id: int, skill_slot3_skill_id: int, skill_slot4_skill_id: int, skill_slot5_skill_id: int) -> Optional[int]:
        sql = insert(hero_log_data).values(
            user=user_id,
            user_hero_log_id=user_hero_log_id,
            log_level=log_level,
            log_exp=log_exp,
            main_weapon=main_weapon,
            sub_equipment=sub_equipment,
            skill_slot1_skill_id=skill_slot1_skill_id,
            skill_slot2_skill_id=skill_slot2_skill_id,
            skill_slot3_skill_id=skill_slot3_skill_id,
            skill_slot4_skill_id=skill_slot4_skill_id,
            skill_slot5_skill_id=skill_slot5_skill_id,
        )

        conflict = sql.on_duplicate_key_update(
            log_level=log_level,
            log_exp=log_exp,
            main_weapon=main_weapon,
            sub_equipment=sub_equipment,
            skill_slot1_skill_id=skill_slot1_skill_id,
            skill_slot2_skill_id=skill_slot2_skill_id,
            skill_slot3_skill_id=skill_slot3_skill_id,
            skill_slot4_skill_id=skill_slot4_skill_id,
            skill_slot5_skill_id=skill_slot5_skill_id,
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.error(
                f"{__name__} failed to insert hero! user: {user_id}, user_hero_log_id: {user_hero_log_id}"
            )
            return None

        return result.lastrowid

    def put_hero_party(self, user_id: int, user_party_team_id: int, user_hero_log_id_1: int, user_hero_log_id_2: int, user_hero_log_id_3: int) -> Optional[int]:
        sql = insert(hero_party).values(
            user=user_id,
            user_party_team_id=user_party_team_id,
            user_hero_log_id_1=user_hero_log_id_1,
            user_hero_log_id_2=user_hero_log_id_2,
            user_hero_log_id_3=user_hero_log_id_3,
        )

        conflict = sql.on_duplicate_key_update(
            user_hero_log_id_1=user_hero_log_id_1,
            user_hero_log_id_2=user_hero_log_id_2,
            user_hero_log_id_3=user_hero_log_id_3,
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.error(
                f"{__name__} failed to insert hero party! user: {user_id}, user_party_team_id: {user_party_team_id}"
            )
            return None

        return result.lastrowid

    def get_hero_log(
        self, user_id: int, user_hero_log_id: int = None
    ) -> Optional[List[Row]]:
        """
        A catch-all hero lookup given a profile and user_party_team_id and ID specifiers
        """
        sql = hero_log_data.select(
            and_(
                hero_log_data.c.user == user_id,
                hero_log_data.c.user_hero_log_id == user_hero_log_id if user_hero_log_id is not None else True,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_hero_logs(
        self, user_id: int
    ) -> Optional[List[Row]]:
        """
        A catch-all hero lookup given a profile and user_party_team_id and ID specifiers
        """
        sql = hero_log_data.select(
            and_(
                hero_log_data.c.user == user_id,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_hero_party(
        self, user_id: int, user_party_team_id: int = None
    ) -> Optional[List[Row]]:
        sql = hero_party.select(
            and_(
                hero_party.c.user == user_id,
                hero_party.c.user_party_team_id == user_party_team_id if user_party_team_id is not None else True,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_session(
        self, user_id: int = None
    ) -> Optional[List[Row]]:
        sql = sessions.select(
            and_(
                sessions.c.user == user_id,
            )
        ).order_by(
            sessions.c.play_date.asc()
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()