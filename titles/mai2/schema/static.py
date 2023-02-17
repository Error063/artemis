from core.data.schema.base import BaseData, metadata

from typing import Optional, Dict, List
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON, Float
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select
from sqlalchemy.engine import Row
from sqlalchemy.dialects.mysql import insert

event = Table(
    "mai2_static_event",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer,nullable=False),
    Column("eventId", Integer),
    Column("type", Integer),
    Column("name", String(255)),
    Column("enabled", Boolean, server_default="1"),
    UniqueConstraint("version", "eventId", "type", name="mai2_static_event_uk"),
    mysql_charset='utf8mb4'
)

music = Table(
    "mai2_static_music",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),    
    Column("version", Integer,nullable=False),
    Column("songId", Integer),
    Column("chartId", Integer),
    Column("title", String(255)),
    Column("artist", String(255)),
    Column("genre", String(255)),
    Column("bpm", Integer),
    Column("addedVersion", String(255)),
    Column("difficulty", Float),
    Column("noteDesigner", String(255)),
    UniqueConstraint("songId", "chartId", "version", name="mai2_static_music_uk"),
    mysql_charset='utf8mb4'
)

ticket = Table(
    "mai2_static_ticket",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer,nullable=False),
    Column("ticketId", Integer),
    Column("kind", Integer),
    Column("name", String(255)),
    Column("price", Integer, server_default="1"),
    Column("enabled", Boolean, server_default="1"),
    UniqueConstraint("version","ticketId", name="mai2_static_ticket_uk"),
    mysql_charset='utf8mb4'
)

class Mai2StaticData(BaseData):
    def put_game_event(self, version: int, type: int, event_id: int, name: str) -> Optional[int]:
        sql = insert(event).values(
            version = version,
            type = type,
            eventId = event_id,
            name = name,
        )

        conflict = sql.on_duplicate_key_update(
            eventId = event_id
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.warning(f"put_game_event: Failed to insert event! event_id {event_id} type {type} name {name}")
        return result.lastrowid

    def get_game_events(self, version: int) -> Optional[List[Row]]:
        sql = event.select(event.c.version == version)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()
    
    def get_enabled_events(self, version: int) -> Optional[List[Row]]:
        sql = select(event).where(and_(
            event.c.version == version,
            event.c.enabled == True
        ))

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()

    def toggle_game_events(self, version: int, event_id: int, toggle: bool) -> Optional[List]:
        sql = event.update(and_(event.c.version == version, event.c.event_id == event_id)).values(
            enabled = int(toggle)
        )

        result = self.execute(sql)
        if result is None:
            self.logger.warning(f"toggle_game_events: Failed to update event! event_id {event_id} toggle {toggle}")
        return result.last_updated_params()
    
    def put_game_music(self, version: int, song_id: int, chart_id: int, title: str, artist: str,
        genre: str, bpm: str, added_version: str, difficulty: float, note_designer: str) -> None:
        sql = insert(music).values(
            version = version,
            songId = song_id,
            chartId = chart_id,
            title = title,
            artist = artist,
            genre = genre,
            bpm = bpm,
            addedVersion = added_version,
            difficulty = difficulty,
            noteDesigner = note_designer,
        )

        conflict = sql.on_duplicate_key_update(
            title = title,
            artist = artist,
            genre = genre,
            bpm = bpm,
            addedVersion = added_version,
            difficulty = difficulty,
            noteDesigner = note_designer,
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(f"Failed to insert song {song_id} chart {chart_id}")
            return None
        return result.lastrowid
    
    def put_game_ticket(self, version: int, ticket_id: int, ticket_type: int, ticket_price: int, name: str) -> Optional[int]:
        sql = insert(ticket).values(
            version = version,
            ticketId = ticket_id,
            kind = ticket_type,
            price = ticket_price,
            name = name
        )
        
        conflict = sql.on_duplicate_key_update(
            price = ticket_price
            )

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(f"Failed to insert charge {ticket_id} type {ticket_type}")
            return None
        return result.lastrowid
    
    def get_enabled_tickets(self, version: int, kind: int = None) -> Optional[List[Row]]:
        if kind is not None:
            sql = select(ticket).where(and_(
                ticket.c.version == version,
                ticket.c.enabled == True,                
                ticket.c.kind == kind
            ))
        else:
            sql = select(ticket).where(and_(
                ticket.c.version == version,
                ticket.c.enabled == True
            ))

        result = self.execute(sql)
        if result is None:return None
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
