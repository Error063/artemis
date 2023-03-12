from typing import Dict, List, Optional
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON, Float
from sqlalchemy.engine.base import Connection
from sqlalchemy.engine import Row
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

music = Table(
    "diva_static_music",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer, nullable=False),
    Column("songId", Integer),
    Column("chartId", Integer),
    Column("title", String(255)),
    Column("vocaloid_arranger", String(255)),
    Column("pv_illustrator", String(255)),
    Column("lyrics", String(255)),
    Column("bg_music", String(255)),
    Column("level", Float),
    Column("bpm", Integer),
    Column("date", String(255)),
    UniqueConstraint("version", "songId", "chartId", name="diva_static_music_uk"),
    mysql_charset="utf8mb4",
)

quests = Table(
    "diva_static_quests",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer, nullable=False),
    Column("questId", Integer),
    Column("name", String(255)),
    Column("quest_enable", Boolean, server_default="1"),
    Column("kind", Integer),
    Column("unknown_0", Integer),
    Column("unknown_1", Integer),
    Column("unknown_2", Integer),
    Column("quest_order", Integer),
    Column("start_datetime", String(255)),
    Column("end_datetime", String(255)),
    UniqueConstraint("version", "questId", name="diva_static_quests_uk"),
    mysql_charset="utf8mb4",
)

shop = Table(
    "diva_static_shop",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer, nullable=False),
    Column("shopId", Integer),
    Column("name", String(255)),
    Column("type", Integer),
    Column("points", Integer),
    Column("unknown_0", Integer),
    Column("start_date", String(255)),
    Column("end_date", String(255)),
    Column("enabled", Boolean, server_default="1"),
    UniqueConstraint("version", "shopId", name="diva_static_shop_uk"),
    mysql_charset="utf8mb4",
)

items = Table(
    "diva_static_items",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer, nullable=False),
    Column("itemId", Integer),
    Column("name", String(255)),
    Column("type", Integer),
    Column("points", Integer),
    Column("unknown_0", Integer),
    Column("start_date", String(255)),
    Column("end_date", String(255)),
    Column("enabled", Boolean, server_default="1"),
    UniqueConstraint("version", "itemId", name="diva_static_items_uk"),
    mysql_charset="utf8mb4",
)


class DivaStaticData(BaseData):
    def put_quests(
        self,
        version: int,
        questId: int,
        name: str,
        kind: int,
        unknown_0: int,
        unknown_1: int,
        unknown_2: int,
        quest_order: int,
        start_datetime: str,
        end_datetime: str,
    ) -> Optional[int]:
        sql = insert(quests).values(
            version=version,
            questId=questId,
            name=name,
            kind=kind,
            unknown_0=unknown_0,
            unknown_1=unknown_1,
            unknown_2=unknown_2,
            quest_order=quest_order,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )

        conflict = sql.on_duplicate_key_update(name=name)

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid

    def get_enabled_quests(self, version: int) -> Optional[List[Row]]:
        sql = select(quests).where(
            and_(quests.c.version == version, quests.c.quest_enable == True)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_shop(
        self,
        version: int,
        shopId: int,
        name: str,
        type: int,
        points: int,
        unknown_0: int,
        start_date: str,
        end_date: str,
    ) -> Optional[int]:
        sql = insert(shop).values(
            version=version,
            shopId=shopId,
            name=name,
            type=type,
            points=points,
            unknown_0=unknown_0,
            start_date=start_date,
            end_date=end_date,
        )

        conflict = sql.on_duplicate_key_update(name=name)

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid

    def get_enabled_shop(self, version: int, shopId: int) -> Optional[Row]:
        sql = select(shop).where(
            and_(
                shop.c.version == version,
                shop.c.shopId == shopId,
                shop.c.enabled == True,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_enabled_shops(self, version: int) -> Optional[List[Row]]:
        sql = select(shop).where(
            and_(shop.c.version == version, shop.c.enabled == True)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_items(
        self,
        version: int,
        itemId: int,
        name: str,
        type: int,
        points: int,
        unknown_0: int,
        start_date: str,
        end_date: str,
    ) -> Optional[int]:
        sql = insert(items).values(
            version=version,
            itemId=itemId,
            name=name,
            type=type,
            points=points,
            unknown_0=unknown_0,
            start_date=start_date,
            end_date=end_date,
        )

        conflict = sql.on_duplicate_key_update(name=name)

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid

    def get_enabled_item(self, version: int, itemId: int) -> Optional[Row]:
        sql = select(items).where(
            and_(
                items.c.version == version,
                items.c.itemId == itemId,
                items.c.enabled == True,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_enabled_items(self, version: int) -> Optional[List[Row]]:
        sql = select(items).where(
            and_(items.c.version == version, items.c.enabled == True)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_music(
        self,
        version: int,
        song: int,
        chart: int,
        title: str,
        arranger: str,
        illustrator: str,
        lyrics: str,
        music_comp: str,
        level: float,
        bpm: int,
        date: str,
    ) -> Optional[int]:
        sql = insert(music).values(
            version=version,
            songId=song,
            chartId=chart,
            title=title,
            vocaloid_arranger=arranger,
            pv_illustrator=illustrator,
            lyrics=lyrics,
            bg_music=music_comp,
            level=level,
            bpm=bpm,
            date=date,
        )

        conflict = sql.on_duplicate_key_update(
            title=title,
            vocaloid_arranger=arranger,
            pv_illustrator=illustrator,
            lyrics=lyrics,
            bg_music=music_comp,
            level=level,
            bpm=bpm,
            date=date,
        )

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid

    def get_music(
        self, version: int, song_id: Optional[int] = None
    ) -> Optional[List[Row]]:
        if song_id is None:
            sql = select(music).where(music.c.version == version)
        else:
            sql = select(music).where(
                and_(
                    music.c.version == version,
                    music.c.songId == song_id,
                )
            )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_music_chart(
        self, version: int, song_id: int, chart_id: int
    ) -> Optional[List[Row]]:
        sql = select(music).where(
            and_(
                music.c.version == version,
                music.c.songId == song_id,
                music.c.chartId == chart_id,
            )
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()
