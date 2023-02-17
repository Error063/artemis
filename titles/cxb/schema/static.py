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
    "cxb_static_music",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer, nullable=False),
    Column("songId", String(255)),
    Column("index", Integer),
    Column("chartId", Integer),
    Column("title", String(255)),
    Column("artist", String(255)),
    Column("category", String(255)),
    Column("level", Float),
    UniqueConstraint("version", "songId", "chartId", "index", name="cxb_static_music_uk"),
    mysql_charset='utf8mb4'
)

class CxbStaticData(BaseData):
    def put_music(self, version: int, mcode: str, index: int, chart: int, title: str, artist: str, category: str, level: float ) -> Optional[int]:
        sql = insert(music).values(
            version = version,
            songId = mcode,
            index = index,
            chartId = chart,
            title = title,
            artist = artist,
            category = category,
            level = level
        )

        conflict = sql.on_duplicate_key_update(
            title = title,
            artist = artist,
            category = category,
            level = level
        )

        result = self.execute(conflict)
        if result is None: return None
        return result.lastrowid
    
    def get_music(self, version: int, song_id: Optional[int] = None) -> Optional[List[Row]]:
        if song_id is None:
            sql = select(music).where(music.c.version == version)
        else:
            sql = select(music).where(and_(
            music.c.version == version,
            music.c.songId == song_id,
            ))

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()
    
    def get_music_chart(self, version: int, song_id: int, chart_id: int) -> Optional[List[Row]]:
        sql = select(music).where(and_(
            music.c.version == version,
            music.c.songId == song_id,
            music.c.chartId == chart_id
            ))

        result = self.execute(sql)
        if result is None: return None
        return result.fetchone()
