from core.data.schema import BaseData, metadata

from datetime import datetime
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
    Column("characterId", Integer, nullable=False),
    Column("level", Integer, nullable=False, server_default="1"),
    Column("awakening", Integer, nullable=False, server_default="0"),
    Column("useCount", Integer, nullable=False, server_default="0"),
    UniqueConstraint("user", "characterId", name="mai2_item_character_uk"),
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
    Column("cardId", Integer, nullable=False),
    Column("cardTypeId", Integer, nullable=False),
    Column("charaId", Integer, nullable=False),
    Column("mapId", Integer, nullable=False),
    Column("startDate", TIMESTAMP, server_default="2018-01-01 00:00:00.0"),
    Column("endDate", TIMESTAMP, server_default="2038-01-01 00:00:00.0"),
    UniqueConstraint("user", "cardId", "cardTypeId", name="mai2_item_card_uk"),
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
    Column("itemId", Integer, nullable=False),
    Column("itemKind", Integer, nullable=False),
    Column("stock", Integer, nullable=False, server_default="1"),
    Column("isValid", Boolean, nullable=False, server_default="1"),
    UniqueConstraint("user", "itemId", "itemKind", name="mai2_item_item_uk"),
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
    Column("mapId", Integer, nullable=False),
    Column("distance", Integer, nullable=False),
    Column("isLock", Boolean, nullable=False, server_default="0"),
    Column("isClear", Boolean, nullable=False, server_default="0"),
    Column("isComplete", Boolean, nullable=False, server_default="0"),
    UniqueConstraint("user", "mapId", name="mai2_item_map_uk"),
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
    Column("bonusId", Integer, nullable=False),
    Column("point", Integer, nullable=False),
    Column("isCurrent", Boolean, nullable=False, server_default="0"),
    Column("isComplete", Boolean, nullable=False, server_default="0"),
    UniqueConstraint("user", "bonusId", name="mai2_item_login_bonus_uk"),
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
    Column("seasonId", Integer, nullable=False),
    Column("point", Integer, nullable=False),
    Column("rank", Integer, nullable=False),
    Column("rewardGet", Boolean, nullable=False),
    Column("userName", String(8), nullable=False),
    Column("recordDate", TIMESTAMP, nullable=False),
    UniqueConstraint(
        "user", "seasonId", "userName", name="mai2_item_friend_season_ranking_uk"
    ),
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
    Column("chargeId", Integer, nullable=False),
    Column("stock", Integer, nullable=False),
    Column("purchaseDate", String(255), nullable=False),
    Column("validDate", String(255), nullable=False),
    UniqueConstraint("user", "chargeId", name="mai2_item_charge_uk"),
    mysql_charset="utf8mb4",
)

print_detail = Table(
    "mai2_item_print_detail",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("orderId", Integer),
    Column("printNumber", Integer),
    Column("printDate", TIMESTAMP, nullable=False, server_default=func.now()),
    Column("serialId", String(20), nullable=False),
    Column("placeId", Integer, nullable=False),
    Column("clientId", String(11), nullable=False),
    Column("printerSerialId", String(20), nullable=False),
    Column("cardRomVersion", Integer),
    Column("isHolograph", Boolean, server_default="1"),
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
    UniqueConstraint("user", "serialId", name="mai2_item_print_detail_uk"),
    mysql_charset="utf8mb4",
)


class Mai2ItemData(BaseData):
    def put_item(
        self, user_id: int, item_kind: int, item_id: int, stock: int, is_valid: bool
    ) -> None:
        sql = insert(item).values(
            user=user_id,
            itemKind=item_kind,
            itemId=item_id,
            stock=stock,
            isValid=is_valid,
        )

        conflict = sql.on_duplicate_key_update(
            stock=stock,
            isValid=is_valid,
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
                and_(item.c.user == user_id, item.c.itemKind == item_kind)
            )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_item(self, user_id: int, item_kind: int, item_id: int) -> Optional[Row]:
        sql = item.select(
            and_(
                item.c.user == user_id,
                item.c.itemKind == item_kind,
                item.c.itemId == item_id,
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
            bonusId=bonus_id,
            point=point,
            isCurrent=is_current,
            isComplete=is_complete,
        )

        conflict = sql.on_duplicate_key_update(
            point=point,
            isCurrent=is_current,
            isComplete=is_complete,
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
            mapId=map_id,
            distance=distance,
            isLock=is_lock,
            isClear=is_clear,
            isComplete=is_complete,
        )

        conflict = sql.on_duplicate_key_update(
            distance=distance,
            isLock=is_lock,
            isClear=is_clear,
            isComplete=is_complete,
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
        sql = map.select(and_(map.c.user == user_id, map.c.mapId == map_id))

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
            characterId=character_id,
            level=level,
            awakening=awakening,
            useCount=use_count,
        )

        conflict = sql.on_duplicate_key_update(
            level=level,
            awakening=awakening,
            useCount=use_count,
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
        return result.fetchall()

    def put_friend_season_ranking(
        self, aime_id: int, friend_season_ranking_data: Dict
    ) -> Optional[int]:
        sql = insert(friend_season_ranking).values(
            user=aime_id, **friend_season_ranking_data
        )

        conflict = sql.on_duplicate_key_update(**friend_season_ranking_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(
                f"put_friend_season_ranking: failed to insert",
                f"friend_season_ranking! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid

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

    def put_card(
        self,
        user_id: int,
        card_type_id: int,
        card_kind: int,
        chara_id: int,
        map_id: int,
    ) -> Optional[Row]:
        sql = insert(card).values(
            user=user_id,
            cardId=card_type_id,
            cardTypeId=card_kind,
            charaId=chara_id,
            mapId=map_id,
        )

        conflict = sql.on_duplicate_key_update(charaId=chara_id, mapId=map_id)

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(
                f"put_card: failed to insert card! user_id: {user_id}, kind: {kind}"
            )
            return None
        return result.lastrowid

    def get_cards(self, user_id: int, kind: int = None) -> Optional[Row]:
        if kind is None:
            sql = card.select(card.c.user == user_id)
        else:
            sql = card.select(and_(card.c.user == user_id, card.c.cardKind == kind))

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_charge(
        self,
        user_id: int,
        charge_id: int,
        stock: int,
        purchase_date: datetime,
        valid_date: datetime,
    ) -> Optional[Row]:
        sql = insert(charge).values(
            user=user_id,
            chargeId=charge_id,
            stock=stock,
            purchaseDate=purchase_date,
            validDate=valid_date,
        )

        conflict = sql.on_duplicate_key_update(
            stock=stock, purchaseDate=purchase_date, validDate=valid_date
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(
                f"put_card: failed to insert charge! user_id: {user_id}, chargeId: {charge_id}"
            )
            return None
        return result.lastrowid

    def get_charges(self, user_id: int) -> Optional[Row]:
        sql = charge.select(charge.c.user == user_id)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_user_print_detail(
        self, aime_id: int, serial_id: str, user_print_data: Dict
    ) -> Optional[int]:
        sql = insert(print_detail).values(
            user=aime_id, serialId=serial_id, **user_print_data
        )

        conflict = sql.on_duplicate_key_update(**user_print_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(
                f"put_user_print_detail: Failed to insert! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid
