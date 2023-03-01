from typing import Dict, List, Optional
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON, Float
from sqlalchemy.engine.base import Connection
from sqlalchemy.engine import Row
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

events = Table(
    "chuni_static_events",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer, nullable=False),
    Column("eventId", Integer),
    Column("type", Integer),
    Column("name", String(255)),
    Column("enabled", Boolean, server_default="1"),
    UniqueConstraint("version", "eventId", name="chuni_static_events_uk"),
    mysql_charset='utf8mb4'
)

music = Table(
    "chuni_static_music",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer, nullable=False),
    Column("songId", Integer),
    Column("chartId", Integer),
    Column("title", String(255)),
    Column("artist", String(255)),    
    Column("level", Float),
    Column("genre", String(255)),
    Column("jacketPath", String(255)),
    Column("worldsEndTag", String(7)),
    UniqueConstraint("version", "songId", "chartId", name="chuni_static_music_uk"),
    mysql_charset='utf8mb4'
)

charge = Table(
    "chuni_static_charge",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer, nullable=False),
    Column("chargeId", Integer),
    Column("name", String(255)),
    Column("expirationDays", Integer),
    Column("consumeType", Integer),
    Column("sellingAppeal", Boolean),
    Column("enabled", Boolean, server_default="1"),
    UniqueConstraint("version", "chargeId", name="chuni_static_charge_uk"),
    mysql_charset='utf8mb4'
)

avatar = Table(
    "chuni_static_avatar",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer, nullable=False),
    Column("avatarAccessoryId", Integer),
    Column("name", String(255)),
    Column("category", Integer),
    Column("iconPath", String(255)),
    Column("texturePath", String(255)),
    UniqueConstraint("version", "avatarAccessoryId", name="chuni_static_avatar_uk"),
    mysql_charset='utf8mb4'
)

class ChuniStaticData(BaseData):
    def put_event(self, version: int, event_id: int, type: int, name: str) -> Optional[int]:
        sql = insert(events).values(
            version = version,
            eventId = event_id,
            type = type,
            name = name
        )

        conflict = sql.on_duplicate_key_update(
            name = name
        )

        result = self.execute(conflict)
        if result is None: return None
        return result.lastrowid
    
    def update_event(self, version: int, event_id: int, enabled: bool) -> Optional[bool]:
        sql = events.update(and_(events.c.version == version, events.c.eventId == event_id)).values(
            enabled = enabled
        )

        result = self.execute(sql)
        if result is None: 
            self.logger.warn(f"update_event: failed to update event! version: {version}, event_id: {event_id}, enabled: {enabled}")
            return None

        event = self.get_event(version, event_id)
        if event is None:
            self.logger.warn(f"update_event: failed to fetch event {event_id} after updating")
            return None
        return event["enabled"]

    def get_event(self, version: int, event_id: int) -> Optional[Row]:
        sql = select(events).where(and_(events.c.version == version, events.c.eventId == event_id))
        
        result = self.execute(sql)
        if result is None: return None
        return result.fetchone()

    def get_enabled_events(self, version: int) -> Optional[List[Row]]:
        sql = select(events).where(and_(events.c.version == version, events.c.enabled == True))

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()

    def get_events(self, version: int) -> Optional[List[Row]]:
        sql = select(events).where(events.c.version == version)

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()
    
    def put_music(self, version: int, song_id: int, chart_id: int, title: int, artist: str, 
        level: float, genre: str, jacketPath: str, we_tag: str) -> Optional[int]:

        sql = insert(music).values(
            version = version,
            songId = song_id,
            chartId = chart_id,
            title = title,
            artist = artist,
            level = level,
            genre = genre,
            jacketPath = jacketPath,
            worldsEndTag = we_tag,
        )

        conflict = sql.on_duplicate_key_update(
            title = title,
            artist = artist,
            level = level,
            genre = genre,
            jacketPath = jacketPath,
            worldsEndTag = we_tag,
        )

        result = self.execute(conflict)
        if result is None: return None
        return result.lastrowid
    
    def put_charge(self, version: int, charge_id: int, name: str, expiration_days: int, 
        consume_type: int, selling_appeal: bool) -> Optional[int]:
        sql = insert(charge).values(
            version = version,
            chargeId = charge_id,
            name = name,
            expirationDays = expiration_days,
            consumeType = consume_type,
            sellingAppeal = selling_appeal,
        )

        conflict = sql.on_duplicate_key_update(
            name = name,
            expirationDays = expiration_days,
            consumeType = consume_type,
            sellingAppeal = selling_appeal,
        )

        result = self.execute(conflict)
        if result is None: return None
        return result.lastrowid
    
    def get_enabled_charges(self, version: int) -> Optional[List[Row]]:
        sql = select(charge).where(and_(
            charge.c.version == version,
            charge.c.enabled == True
        ))

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()
    
    def get_charges(self, version: int) -> Optional[List[Row]]:
        sql = select(charge).where(charge.c.version == version)

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

    def put_avatar(self, version: int, avatarAccessoryId: int, name: str, category: int, iconPath: str, texturePath: str) -> Optional[int]:
        sql = insert(avatar).values(
            version = version,
            avatarAccessoryId = avatarAccessoryId,
            name = name,
            category = category,
            iconPath = iconPath,
            texturePath = texturePath,
        )

        conflict = sql.on_duplicate_key_update(
            name = name,
            category = category,
            iconPath = iconPath,
            texturePath = texturePath,
        )

        result = self.execute(conflict)
        if result is None: return None
        return result.lastrowid
    
