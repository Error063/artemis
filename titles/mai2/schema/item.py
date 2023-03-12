from core.data.schema import BaseData, metadata

from typing import Optional, Dict, List
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.engine import Row

character = Table(
    "mai2_item_character",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("character_id", Integer, nullable=False),
    Column("level", Integer, nullable=False, server_default="1"),
    Column("awakening", Integer, nullable=False, server_default="0"),
    Column("use_count", Integer, nullable=False, server_default="0"),
    UniqueConstraint("user", "character_id", name="mai2_item_character_uk"),
    mysql_charset="utf8mb4",
)

card = Table(
    "mai2_item_card",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("card_kind", Integer, nullable=False),
    Column("card_id", Integer, nullable=False),
    Column("chara_id", Integer, nullable=False),
    Column("map_id", Integer, nullable=False),
    Column("start_date", String(255), nullable=False),
    Column("end_date", String(255), nullable=False),
    UniqueConstraint("user", "card_kind", "card_id", name="mai2_item_card_uk"),
    mysql_charset="utf8mb4",
)

item = Table(
    "mai2_item_item",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("item_kind", Integer, nullable=False),
    Column("item_id", Integer, nullable=False),
    Column("stock", Integer, nullable=False, server_default="1"),
    Column("is_valid", Boolean, nullable=False, server_default="1"),
    UniqueConstraint("user", "item_kind", "item_id", name="mai2_item_item_uk"),
    mysql_charset="utf8mb4",
)

map = Table(
    "mai2_item_map",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("map_id", Integer, nullable=False),
    Column("distance", Integer, nullable=False),
    Column("is_lock", Boolean, nullable=False, server_default="0"),
    Column("is_clear", Boolean, nullable=False, server_default="0"),
    Column("is_complete", Boolean, nullable=False, server_default="0"),
    UniqueConstraint("user", "map_id", name="mai2_item_map_uk"),
    mysql_charset="utf8mb4",
)

login_bonus = Table(
    "mai2_item_login_bonus",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("bonus_id", Integer, nullable=False),
    Column("point", Integer, nullable=False),
    Column("is_current", Boolean, nullable=False, server_default="0"),
    Column("is_complete", Boolean, nullable=False, server_default="0"),
    UniqueConstraint("user", "bonus_id", name="mai2_item_login_bonus_uk"),
    mysql_charset="utf8mb4",
)

friend_season_ranking = Table(
    "mai2_item_friend_season_ranking",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("season_id", Integer, nullable=False),
    Column("point", Integer, nullable=False),
    Column("rank", Integer, nullable=False),
    Column("reward_get", Boolean, nullable=False),
    Column("user_name", String(8), nullable=False),
    Column("record_date", String(255), nullable=False),
    UniqueConstraint("user", "season_id", "user_name", name="mai2_item_login_bonus_uk"),
    mysql_charset="utf8mb4",
)

favorite = Table(
    "mai2_item_favorite",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("itemKind", Integer, nullable=False),
    Column("itemIdList", JSON),
    UniqueConstraint("user", "itemKind", name="mai2_item_favorite_uk"),
    mysql_charset="utf8mb4",
)

charge = Table(
    "mai2_item_charge",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("charge_id", Integer, nullable=False),
    Column("stock", Integer, nullable=False),
    Column("purchase_date", String(255), nullable=False),
    Column("valid_date", String(255), nullable=False),
    UniqueConstraint("user", "charge_id", name="mai2_item_charge_uk"),
    mysql_charset="utf8mb4",
)


class Mai2ItemData(BaseData):
    def put_item(
        self, user_id: int, item_kind: int, item_id: int, stock: int, is_valid: bool
    ) -> None:
        sql = insert(item).values(
            user=user_id,
            item_kind=item_kind,
            item_id=item_id,
            stock=stock,
            is_valid=is_valid,
        )

        conflict = sql.on_duplicate_key_update(
            stock=stock,
            is_valid=is_valid,
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(
                f"put_item: failed to insert item! user_id: {user_id}, item_kind: {item_kind}, item_id: {item_id}"
            )
            return None
        return result.lastrowid

    def get_items(self, user_id: int, item_kind: int = None) -> Optional[List[Row]]:
        if item_kind is None:
            sql = item.select(item.c.user == user_id)
        else:
            sql = item.select(
                and_(item.c.user == user_id, item.c.item_kind == item_kind)
            )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_item(self, user_id: int, item_kind: int, item_id: int) -> Optional[Row]:
        sql = item.select(
            and_(
                item.c.user == user_id,
                item.c.item_kind == item_kind,
                item.c.item_id == item_id,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_login_bonus(
        self,
        user_id: int,
        bonus_id: int,
        point: int,
        is_current: bool,
        is_complete: bool,
    ) -> None:
        sql = insert(login_bonus).values(
            user=user_id,
            bonus_id=bonus_id,
            point=point,
            is_current=is_current,
            is_complete=is_complete,
        )

        conflict = sql.on_duplicate_key_update(
            point=point,
            is_current=is_current,
            is_complete=is_complete,
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(
                f"put_login_bonus: failed to insert item! user_id: {user_id}, bonus_id: {bonus_id}, point: {point}"
            )
            return None
        return result.lastrowid

    def get_login_bonuses(self, user_id: int) -> Optional[List[Row]]:
        sql = login_bonus.select(login_bonus.c.user == user_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_login_bonus(self, user_id: int, bonus_id: int) -> Optional[Row]:
        sql = login_bonus.select(
            and_(login_bonus.c.user == user_id, login_bonus.c.bonus_id == bonus_id)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_map(
        self,
        user_id: int,
        map_id: int,
        distance: int,
        is_lock: bool,
        is_clear: bool,
        is_complete: bool,
    ) -> None:
        sql = insert(map).values(
            user=user_id,
            map_id=map_id,
            distance=distance,
            is_lock=is_lock,
            is_clear=is_clear,
            is_complete=is_complete,
        )

        conflict = sql.on_duplicate_key_update(
            distance=distance,
            is_lock=is_lock,
            is_clear=is_clear,
            is_complete=is_complete,
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(
                f"put_map: failed to insert item! user_id: {user_id}, map_id: {map_id}, distance: {distance}"
            )
            return None
        return result.lastrowid

    def get_maps(self, user_id: int) -> Optional[List[Row]]:
        sql = map.select(map.c.user == user_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_map(self, user_id: int, map_id: int) -> Optional[Row]:
        sql = map.select(and_(map.c.user == user_id, map.c.map_id == map_id))

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_character(
        self,
        user_id: int,
        character_id: int,
        level: int,
        awakening: int,
        use_count: int,
    ) -> None:
        sql = insert(character).values(
            user=user_id,
            character_id=character_id,
            level=level,
            awakening=awakening,
            use_count=use_count,
        )

        conflict = sql.on_duplicate_key_update(
            level=level,
            awakening=awakening,
            use_count=use_count,
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(
                f"put_character: failed to insert item! user_id: {user_id}, character_id: {character_id}, level: {level}"
            )
            return None
        return result.lastrowid

    def get_characters(self, user_id: int) -> Optional[List[Row]]:
        sql = character.select(character.c.user == user_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_character(self, user_id: int, character_id: int) -> Optional[Row]:
        sql = character.select(
            and_(character.c.user == user_id, character.c.character_id == character_id)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_friend_season_ranking(self, user_id: int) -> Optional[Row]:
        sql = friend_season_ranking.select(friend_season_ranking.c.user == user_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_favorite(
        self, user_id: int, kind: int, item_id_list: List[int]
    ) -> Optional[int]:
        sql = insert(favorite).values(
            user=user_id, kind=kind, item_id_list=item_id_list
        )

        conflict = sql.on_duplicate_key_update(item_id_list=item_id_list)

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(
                f"put_favorite: failed to insert item! user_id: {user_id}, kind: {kind}"
            )
            return None
        return result.lastrowid

    def get_favorites(self, user_id: int, kind: int = None) -> Optional[Row]:
        if kind is None:
            sql = favorite.select(favorite.c.user == user_id)
        else:
            sql = favorite.select(
                and_(favorite.c.user == user_id, favorite.c.itemKind == kind)
            )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()
