from typing import Dict, List, Optional
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON, Float
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select
from sqlalchemy.engine import Row
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

events = Table(
    "ongeki_static_events",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer),
    Column("eventId", Integer),
    Column("type", Integer),
    Column("name", String(255)),
    Column("enabled", Boolean, server_default="1"),
    UniqueConstraint("version", "eventId", "type", name="ongeki_static_events_uk"),
    mysql_charset='utf8mb4'
)


music = Table(
    "ongeki_static_music",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer),
    Column("songId", Integer),
    Column("chartId", Integer),
    Column("title", String(255)),
    Column("artist", String(255)),
    Column("genre", String(255)),
    Column("level", Float),
    UniqueConstraint("version", "songId", "chartId", name="ongeki_static_music_uk"),
    mysql_charset='utf8mb4'
)

class OngekiStaticData(BaseData):
    def put_event(self, version: int, event_id: int, event_type: int, event_name: str) -> Optional[int]:
        sql = insert(events).values(
            version = version,
            eventId = event_id,
            type = event_type,
            name = event_name,
        )

        conflict = sql.on_duplicate_key_update(
            name = event_name,
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(f"Failed to insert event! event_id {event_id}")
            return None
        return result.lastrowid

    def get_event(self, version: int, event_id: int) -> Optional[List[Dict]]:
        sql = select(events).where(and_(events.c.version == version, events.c.eventId == event_id))
        
        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()

    def get_events(self, version: int) -> Optional[List[Dict]]:
        sql = select(events).where(events.c.version == version)
        
        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()
    
    def get_enabled_events(self, version: int) -> Optional[List[Dict]]:
        sql = select(events).where(and_(events.c.version == version, events.c.enabled == True))
        
        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()

    def put_chart(self, version: int, song_id: int, chart_id: int, title: str, artist: str, genre: str, level: float) -> Optional[int]:
        sql = insert(music).values(
            version = version,
            songId = song_id,
            chartId = chart_id,
            title = title,
            artist = artist,
            genre = genre,
            level = level,
        )

        conflict = sql.on_duplicate_key_update(
            title = title,
            artist = artist,
            genre = genre,
            level = level,
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(f"Failed to insert chart! song_id: {song_id}, chart_id: {chart_id}")
            return None
        return result.lastrowid

    def get_chart(self, version: int, song_id: int, chart_id: int = None) -> Optional[List[Dict]]:
        pass

    def get_music(self, version: int) -> Optional[List[Dict]]:
        pass

    def get_music_chart(self, version: int, song_id: int, chart_id: int) -> Optional[List[Row]]:
        sql = select(music).where(and_(
            music.c.version == version,
            music.c.songId == song_id,
            music.c.chartId == chart_id
            ))

        result = self.execute(sql)
        if result is None: return None
        return result.fetchone()
