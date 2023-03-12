from typing import Dict, List, Optional
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON
from sqlalchemy.engine.base import Connection
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.engine import Row

from core.data.schema import BaseData, metadata

character = Table(
    "chuni_item_character",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("characterId", Integer),
    Column("level", Integer),
    Column("param1", Integer),
    Column("param2", Integer),
    Column("isValid", Boolean),
    Column("skillId", Integer),
    Column("isNewMark", Boolean),
    Column("playCount", Integer),
    Column("friendshipExp", Integer),
    Column("assignIllust", Integer),
    Column("exMaxLv", Integer),
    UniqueConstraint("user", "characterId", name="chuni_item_character_uk"),
    mysql_charset="utf8mb4",
)

item = Table(
    "chuni_item_item",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("itemId", Integer),
    Column("itemKind", Integer),
    Column("stock", Integer),
    Column("isValid", Boolean),
    UniqueConstraint("user", "itemId", "itemKind", name="chuni_item_item_uk"),
    mysql_charset="utf8mb4",
)

duel = Table(
    "chuni_item_duel",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("duelId", Integer),
    Column("progress", Integer),
    Column("point", Integer),
    Column("isClear", Boolean),
    Column("lastPlayDate", String(25)),
    Column("param1", Integer),
    Column("param2", Integer),
    Column("param3", Integer),
    Column("param4", Integer),
    UniqueConstraint("user", "duelId", name="chuni_item_duel_uk"),
    mysql_charset="utf8mb4",
)

map = Table(
    "chuni_item_map",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("mapId", Integer),
    Column("position", Integer),
    Column("isClear", Boolean),
    Column("areaId", Integer),
    Column("routeNumber", Integer),
    Column("eventId", Integer),
    Column("rate", Integer),
    Column("statusCount", Integer),
    Column("isValid", Boolean),
    UniqueConstraint("user", "mapId", name="chuni_item_map_uk"),
    mysql_charset="utf8mb4",
)

map_area = Table(
    "chuni_item_map_area",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("mapAreaId", Integer),
    Column("rate", Integer),
    Column("isClear", Boolean),
    Column("isLocked", Boolean),
    Column("position", Integer),
    Column("statusCount", Integer),
    Column("remainGridCount", Integer),
    UniqueConstraint("user", "mapAreaId", name="chuni_item_map_area_uk"),
    mysql_charset="utf8mb4",
)


class ChuniItemData(BaseData):
    def put_character(self, user_id: int, character_data: Dict) -> Optional[int]:
        character_data["user"] = user_id

        character_data = self.fix_bools(character_data)

        sql = insert(character).values(**character_data)
        conflict = sql.on_duplicate_key_update(**character_data)

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid

    def get_character(self, user_id: int, character_id: int) -> Optional[Dict]:
        sql = select(character).where(
            and_(character.c.user == user_id, character.c.characterId == character_id)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_characters(self, user_id: int) -> Optional[List[Row]]:
        sql = select(character).where(character.c.user == user_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_item(self, user_id: int, item_data: Dict) -> Optional[int]:
        item_data["user"] = user_id

        item_data = self.fix_bools(item_data)

        sql = insert(item).values(**item_data)
        conflict = sql.on_duplicate_key_update(**item_data)

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid

    def get_items(self, user_id: int, kind: int = None) -> Optional[List[Row]]:
        if kind is None:
            sql = select(item).where(item.c.user == user_id)
        else:
            sql = select(item).where(
                and_(item.c.user == user_id, item.c.itemKind == kind)
            )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_duel(self, user_id: int, duel_data: Dict) -> Optional[int]:
        duel_data["user"] = user_id

        duel_data = self.fix_bools(duel_data)

        sql = insert(duel).values(**duel_data)
        conflict = sql.on_duplicate_key_update(**duel_data)

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid

    def get_duels(self, user_id: int) -> Optional[List[Row]]:
        sql = select(duel).where(duel.c.user == user_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_map(self, user_id: int, map_data: Dict) -> Optional[int]:
        map_data["user"] = user_id

        map_data = self.fix_bools(map_data)

        sql = insert(map).values(**map_data)
        conflict = sql.on_duplicate_key_update(**map_data)

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid

    def get_maps(self, user_id: int) -> Optional[List[Row]]:
        sql = select(map).where(map.c.user == user_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_map_area(self, user_id: int, map_area_data: Dict) -> Optional[int]:
        map_area_data["user"] = user_id

        map_area_data = self.fix_bools(map_area_data)

        sql = insert(map_area).values(**map_area_data)
        conflict = sql.on_duplicate_key_update(**map_area_data)

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid

    def get_map_areas(self, user_id: int) -> Optional[List[Row]]:
        sql = select(map_area).where(map_area.c.user == user_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()
