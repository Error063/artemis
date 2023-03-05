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

gachas = Table(
    "ongeki_static_gachas",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer, nullable=False),
    Column("gachaId", Integer, nullable=False),
    Column("gachaName", String(255), nullable=False),
    Column("type", Integer, nullable=False, server_default="0"),
    Column("kind", Integer, nullable=False, server_default="0"),
    Column("isCeiling", Boolean, server_default="0"),
    Column("maxSelectPoint", Integer, server_default="0"),
    Column("ceilingCnt", Integer, server_default="10"),
    Column("changeRateCnt1", Integer, server_default="0"),
    Column("changeRateCnt2", Integer, server_default="0"),
    Column("startDate", TIMESTAMP, server_default="2018-01-01 00:00:00.0"),
    Column("endDate", TIMESTAMP, server_default="2038-01-01 00:00:00.0"),
    Column("noticeStartDate", TIMESTAMP, server_default="2018-01-01 00:00:00.0"),
    Column("noticeEndDate", TIMESTAMP, server_default="2038-01-01 00:00:00.0"),
    Column("convertEndDate", TIMESTAMP, server_default="2038-01-01 00:00:00.0"),
    UniqueConstraint("version", "gachaId", "gachaName", name="ongeki_static_gachas_uk"),
    mysql_charset='utf8mb4'
)

gacha_cards = Table(
    "ongeki_static_gacha_cards",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("gachaId", Integer, nullable=False),
    Column("cardId", Integer, nullable=False),
    Column("rarity", Integer, nullable=False),
    Column("weight", Integer, server_default="1"),
    Column("isPickup", Boolean, server_default="0"),
    Column("isSelect", Boolean, server_default="0"),
    UniqueConstraint("gachaId", "cardId", name="ongeki_static_gacha_cards_uk"),
    mysql_charset='utf8mb4'
)

cards = Table(
    "ongeki_static_cards",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer, nullable=False),
    Column("cardId", Integer, nullable=False),
    Column("name", String(255), nullable=False),
    Column("charaId", Integer, nullable=False),
    Column("nickName", String(255)),
    Column("school", String(255), nullable=False),
    Column("attribute", String(5), nullable=False),
    Column("gakunen", String(255), nullable=False),
    Column("rarity", Integer, nullable=False),
    Column("levelParam", String(255), nullable=False),
    Column("skillId", Integer, nullable=False),
    Column("choKaikaSkillId", Integer, nullable=False),
    Column("cardNumber", String(255)),
    UniqueConstraint("version", "cardId", name="ongeki_static_cards_uk"),
    mysql_charset='utf8mb4'
)


class OngekiStaticData(BaseData):
    def put_card(self, version: int, card_id: int, **card_data) -> Optional[int]:
        sql = insert(cards).values(
            version=version,
            cardId=card_id,
            **card_data)

        conflict = sql.on_duplicate_key_update(**card_data)

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(f"Failed to insert card! card_id {card_id}")
            return None
        return result.lastrowid

    def get_card(self, version: int, card_id: int) -> Optional[Dict]:
        sql = cards.select(and_(
            cards.c.version <= version,
            cards.c.cardId == card_id
        ))

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_card_by_card_number(self, version: int, card_number: str) -> Optional[Dict]:
        if not card_number.startswith("[O.N.G.E.K.I.]"):
            card_number = f"[O.N.G.E.K.I.]{card_number}"

        sql = cards.select(and_(
            cards.c.version <= version,
            cards.c.cardNumber == card_number
        ))

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_card_by_name(self, version: int, name: str) -> Optional[Dict]:
        sql = cards.select(and_(
            cards.c.version <= version,
            cards.c.name == name
        ))

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_cards(self, version: int) -> Optional[List[Dict]]:
        sql = cards.select(cards.c.version <= version)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_cards_by_rarity(self, version: int, rarity: int) -> Optional[List[Dict]]:
        sql = cards.select(and_(
            cards.c.version <= version,
            cards.c.rarity == rarity
        ))

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_gacha(self, version: int, gacha_id: int, gacha_name: int,
                  gacha_kind: int, **gacha_data) -> Optional[int]:
        sql = insert(gachas).values(
            version=version,
            gachaId=gacha_id,
            gachaName=gacha_name,
            kind=gacha_kind,
            **gacha_data
        )

        conflict = sql.on_duplicate_key_update(
            version=version,
            gachaId=gacha_id,
            gachaName=gacha_name,
            kind=gacha_kind,
            **gacha_data
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(f"Failed to insert gacha! gacha_id {gacha_id}")
            return None
        return result.lastrowid

    def get_gacha(self, version: int, gacha_id: int) -> Optional[Dict]:
        sql = gachas.select(and_(
            gachas.c.version <= version,
            gachas.c.gachaId == gacha_id
        ))

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_gachas(self, version: int) -> Optional[List[Dict]]:
        sql = gachas.select(
            gachas.c.version == version).order_by(
            gachas.c.gachaId.asc()
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def put_gacha_card(self, gacha_id: int, card_id: int, **gacha_card) -> Optional[int]:
        sql = insert(gacha_cards).values(
            gachaId=gacha_id,
            cardId=card_id,
            **gacha_card
        )

        conflict = sql.on_duplicate_key_update(
            gachaId=gacha_id,
            cardId=card_id,
            **gacha_card
        )

        result = self.execute(conflict)
        if result is None:
            self.logger.warn(f"Failed to insert gacha card! gacha_id {gacha_id}")
            return None
        return result.lastrowid

    def get_gacha_cards(self, gacha_id: int) -> Optional[List[Dict]]:
        sql = gacha_cards.select(
            gacha_cards.c.gachaId == gacha_id
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

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
