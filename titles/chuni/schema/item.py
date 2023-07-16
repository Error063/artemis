from typing import Dict, List, Optional
from sqlalchemy import (
    Table,
    Column,
    UniqueConstraint,
    PrimaryKeyConstraint,
    and_,
    delete,
)
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

gacha = Table(
    "chuni_item_gacha",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("gachaId", Integer, nullable=False),
    Column("totalGachaCnt", Integer, server_default="0"),
    Column("ceilingGachaCnt", Integer, server_default="0"),
    Column("dailyGachaCnt", Integer, server_default="0"),
    Column("fiveGachaCnt", Integer, server_default="0"),
    Column("elevenGachaCnt", Integer, server_default="0"),
    Column("dailyGachaDate", TIMESTAMP, nullable=False, server_default=func.now()),
    UniqueConstraint("user", "gachaId", name="chuni_item_gacha_uk"),
    mysql_charset="utf8mb4",
)

print_state = Table(
    "chuni_item_print_state",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("hasCompleted", Boolean, nullable=False, server_default="0"),
    Column(
        "limitDate", TIMESTAMP, nullable=False, server_default="2038-01-01 00:00:00.0"
    ),
    Column("placeId", Integer),
    Column("cardId", Integer),
    Column("gachaId", Integer),
    UniqueConstraint("id", "user", name="chuni_item_print_state_uk"),
    mysql_charset="utf8mb4",
)

print_detail = Table(
    "chuni_item_print_detail",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("cardId", Integer, nullable=False),
    Column("printDate", TIMESTAMP, nullable=False),
    Column("serialId", String(20), nullable=False),
    Column("placeId", Integer, nullable=False),
    Column("clientId", String(11), nullable=False),
    Column("printerSerialId", String(20), nullable=False),
    Column("printOption1", Boolean, server_default="0"),
    Column("printOption2", Boolean, server_default="0"),
    Column("printOption3", Boolean, server_default="0"),
    Column("printOption4", Boolean, server_default="0"),
    Column("printOption5", Boolean, server_default="0"),
    Column("printOption6", Boolean, server_default="0"),
    Column("printOption7", Boolean, server_default="0"),
    Column("printOption8", Boolean, server_default="0"),
    Column("printOption9", Boolean, server_default="0"),
    Column("printOption10", Boolean, server_default="0"),
    Column("created", String(255), server_default=""),
    UniqueConstraint("serialId", name="chuni_item_print_detail_uk"),
    mysql_charset="utf8mb4",
)

login_bonus = Table(
    "chuni_item_login_bonus",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("presetId", Integer, nullable=False),
    Column("bonusCount", Integer, nullable=False, server_default="0"),
    Column("lastUpdateDate", TIMESTAMP, server_default="2018-01-01 00:00:00.0"),
    Column("isWatched", Boolean, server_default="0"),
    Column("isFinished", Boolean, server_default="0"),
    UniqueConstraint("version", "user", "presetId", name="chuni_item_login_bonus_uk"),
    mysql_charset="utf8mb4",
)

favorite = Table(
    "chuni_item_favorite",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("favId", Integer, nullable=False),
    Column("favKind", Integer, nullable=False, server_default="1"),
    UniqueConstraint("version", "user", "favId", name="chuni_item_favorite_uk"),
    mysql_charset="utf8mb4",
)

matching = Table(
    "chuni_item_matching",
    metadata,
    Column("roomId", Integer, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("restMSec", Integer, nullable=False, server_default="60"),
    Column("isFull", Boolean, nullable=False, server_default="0"),
    PrimaryKeyConstraint("roomId", "version", name="chuni_item_matching_pk"),
    Column("matchingMemberInfoList", JSON, nullable=False),
    mysql_charset="utf8mb4",
)


class ChuniItemData(BaseData):
    def get_oldest_free_matching(self, version: int) -> Optional[Row]:
        sql = matching.select(
            and_(
                matching.c.version == version,
                matching.c.isFull == False
            )
        ).order_by(matching.c.roomId.asc())

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_newest_matching(self, version: int) -> Optional[Row]:
        sql = matching.select(
            and_(
                matching.c.version == version
            )
        ).order_by(matching.c.roomId.desc())

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_all_matchings(self, version: int) -> Optional[List[Row]]:
        sql = matching.select(
            and_(
                matching.c.version == version
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_matching(self, version: int, room_id: int) -> Optional[Row]:
        sql = matching.select(
            and_(matching.c.version == version, matching.c.roomId == room_id)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def put_matching(
        self,
        version: int,
        room_id: int,
        matching_member_info_list: List,
        user_id: int = None,
        rest_sec: int = 60,
        is_full: bool = False
    ) -> Optional[int]:
        sql = insert(matching).values(
            roomId=room_id,
            version=version,
            restMSec=rest_sec,
            user=user_id,
            isFull=is_full,
            matchingMemberInfoList=matching_member_info_list,
        )

        conflict = sql.on_duplicate_key_update(
            restMSec=rest_sec, matchingMemberInfoList=matching_member_info_list
        )

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid

    def delete_matching(self, version: int, room_id: int):
        sql = delete(matching).where(
            and_(matching.c.roomId == room_id, matching.c.version == version)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.lastrowid

    def get_all_favorites(
        self, user_id: int, version: int, fav_kind: int = 1
    ) -> Optional[List[Row]]:
        sql = favorite.select(
            and_(
                favorite.c.version == version,
                favorite.c.user == user_id,
                favorite.c.favKind == fav_kind,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_login_bonus(
        self, user_id: int, version: int, preset_id: int, **login_bonus_data
    ) -> Optional[int]:
        sql = insert(login_bonus).values(
            version=version, user=user_id, presetId=preset_id, **login_bonus_data
        )

        conflict = sql.on_duplicate_key_update(presetId=preset_id, **login_bonus_data)

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid

    def get_all_login_bonus(
        self, user_id: int, version: int, is_finished: bool = False
    ) -> Optional[List[Row]]:
        sql = login_bonus.select(
            and_(
                login_bonus.c.version == version,
                login_bonus.c.user == user_id,
                login_bonus.c.isFinished == is_finished,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_login_bonus(
        self, user_id: int, version: int, preset_id: int
    ) -> Optional[Row]:
        sql = login_bonus.select(
            and_(
                login_bonus.c.version == version,
                login_bonus.c.user == user_id,
                login_bonus.c.presetId == preset_id,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

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

    def get_user_gachas(self, aime_id: int) -> Optional[List[Row]]:
        sql = gacha.select(gacha.c.user == aime_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_user_gacha(
        self, aime_id: int, gacha_id: int, gacha_data: Dict
    ) -> Optional[int]:
        sql = insert(gacha).values(user=aime_id, gachaId=gacha_id, **gacha_data)

        conflict = sql.on_duplicate_key_update(
            user=aime_id, gachaId=gacha_id, **gacha_data
        )
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_user_gacha: Failed to insert! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def get_user_print_states(
        self, aime_id: int, has_completed: bool = False
    ) -> Optional[List[Row]]:
        sql = print_state.select(
            and_(
                print_state.c.user == aime_id,
                print_state.c.hasCompleted == has_completed,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_user_print_states_by_gacha(
        self, aime_id: int, gacha_id: int, has_completed: bool = False
    ) -> Optional[List[Row]]:
        sql = print_state.select(
            and_(
                print_state.c.user == aime_id,
                print_state.c.gachaId == gacha_id,
                print_state.c.hasCompleted == has_completed,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_user_print_state(self, aime_id: int, **print_data) -> Optional[int]:
        sql = insert(print_state).values(user=aime_id, **print_data)

        conflict = sql.on_duplicate_key_update(user=aime_id, **print_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(
                f"put_user_print_state: Failed to insert! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid

    def put_user_print_detail(
        self, aime_id: int, serial_id: str, user_print_data: Dict
    ) -> Optional[int]:
        sql = insert(print_detail).values(
            user=aime_id, serialId=serial_id, **user_print_data
        )

        conflict = sql.on_duplicate_key_update(user=aime_id, **user_print_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(
                f"put_user_print_detail: Failed to insert! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid
