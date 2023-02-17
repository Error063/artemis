from typing import Dict, Optional, List
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

card = Table(
    "ongeki_user_card",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("cardId", Integer),
    Column("digitalStock", Integer),
    Column("analogStock", Integer),
    Column("level", Integer),
    Column("maxLevel", Integer),
    Column("exp", Integer),
    Column("printCount", Integer),
    Column("useCount", Integer),
    Column("isNew", Boolean),
    Column("kaikaDate", String(25)),
    Column("choKaikaDate", String(25)),
    Column("skillId", Integer),
    Column("isAcquired", Boolean),
    Column("created", String(25)),
    UniqueConstraint("user", "cardId", name="ongeki_user_card_uk"),
    mysql_charset='utf8mb4'
)

deck = Table(
    "ongeki_user_deck",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("deckId", Integer),
    Column("cardId1", Integer),
    Column("cardId2", Integer),
    Column("cardId3", Integer),
    UniqueConstraint("user", "deckId", name="ongeki_user_deck_uk"),
    mysql_charset='utf8mb4'
)

character = Table(
    "ongeki_user_character",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("characterId", Integer),
    Column("costumeId", Integer),
    Column("attachmentId", Integer),
    Column("playCount", Integer),
    Column("intimateLevel", Integer),
    Column("intimateCount", Integer),
    Column("intimateCountRewarded", Integer),
    Column("intimateCountDate", String(25)),
    Column("isNew", Boolean),
    UniqueConstraint("user", "characterId", name="ongeki_user_character_uk"),
    mysql_charset='utf8mb4'
)

boss = Table (
    "ongeki_user_boss",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("musicId", Integer),
    Column("damage", Integer),
    Column("isClear", Boolean),
    Column("eventId", Integer),
    UniqueConstraint("user", "musicId", "eventId", name="ongeki_user_boss_uk"),
    mysql_charset='utf8mb4'
)

story = Table (
    "ongeki_user_story",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("storyId", Integer),
    Column("jewelCount", Integer),
    Column("lastChapterId", Integer),
    Column("lastPlayMusicId", Integer),
    Column("lastPlayMusicCategory", Integer),
    Column("lastPlayMusicLevel", Integer),
    UniqueConstraint("user", "storyId", name="ongeki_user_story_uk"),
    mysql_charset='utf8mb4'
)

chapter = Table(
    "ongeki_user_chapter",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("chapterId", Integer),
    Column("jewelCount", Integer),
    Column("isStoryWatched", Boolean),
    Column("isClear", Boolean),
    Column("lastPlayMusicId", Integer),
    Column("lastPlayMusicCategory", Integer),
    Column("lastPlayMusicLevel", Integer),
    Column("skipTiming1", Integer),
    Column("skipTiming2", Integer),
    UniqueConstraint("user", "chapterId", name="ongeki_user_chapter_uk"),
    mysql_charset='utf8mb4'
)

item = Table(
    "ongeki_user_item",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("itemKind", Integer),
    Column("itemId", Integer),
    Column("stock", Integer),
    Column("isValid", Boolean),
    UniqueConstraint("user", "itemKind", "itemId", name="ongeki_user_item_uk"),
    mysql_charset='utf8mb4'
)

music_item = Table(
    "ongeki_user_music_item",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("musicId", Integer),
    Column("status", Integer),
    UniqueConstraint("user", "musicId", name="ongeki_user_music_item_uk"),
    mysql_charset='utf8mb4'
)

login_bonus = Table(
    "ongeki_user_login_bonus",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("bonusId", Integer),
    Column("bonusCount", Integer),
    Column("lastUpdateDate", String(25)),
    UniqueConstraint("user", "bonusId", name="ongeki_user_login_bonus_uk"),
    mysql_charset='utf8mb4'
)

event_point = Table(
    "ongeki_user_event_point",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("eventId", Integer),
    Column("point", Integer),
    Column("isRankingRewarded", Boolean),
    UniqueConstraint("user", "eventId", name="ongeki_user_event_point_uk"),
    mysql_charset='utf8mb4'
)

mission_point = Table(
    "ongeki_user_mission_point",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("eventId", Integer),
    Column("point", Integer),
    UniqueConstraint("user", "eventId", name="ongeki_user_mission_point_uk"),
    mysql_charset='utf8mb4'
)

scenerio = Table(
    "ongeki_user_scenerio",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("scenarioId", Integer),
    Column("playCount", Integer),
    UniqueConstraint("user", "scenarioId", name="ongeki_user_scenerio_uk"),
    mysql_charset='utf8mb4'
)

trade_item = Table(
    "ongeki_user_trade_item",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("chapterId", Integer),
    Column("tradeItemId", Integer),
    Column("tradeCount", Integer),
    UniqueConstraint("user", "chapterId", "tradeItemId", name="ongeki_user_trade_item_uk"),
    mysql_charset='utf8mb4'
)

event_music = Table(
    "ongeki_user_event_music",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("eventId", Integer),
    Column("type", Integer),
    Column("musicId", Integer),
    Column("level", Integer),
    Column("techScoreMax", Integer),
    Column("platinumScoreMax", Integer),
    Column("techRecordDate", String(25)),
    Column("isTechNewRecord", Boolean),
    UniqueConstraint("user", "eventId", "type", "musicId", "level", name="ongeki_user_event_music"),
    mysql_charset='utf8mb4'
)

tech_event = Table(
    "ongeki_user_tech_event",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("eventId", Integer),
    Column("totalTechScore", Integer),
    Column("totalPlatinumScore", Integer),
    Column("techRecordDate", String(25)),
    Column("isRankingRewarded", Boolean),
    Column("isTotalTechNewRecord", Boolean),
    UniqueConstraint("user", "eventId", name="ongeki_user_tech_event_uk"),
    mysql_charset='utf8mb4'
)


class OngekiItemData(BaseData):    
    def put_card(self, aime_id: int, card_data: Dict) -> Optional[int]:
        card_data["user"] = aime_id

        sql = insert(card).values(**card_data)
        conflict = sql.on_duplicate_key_update(**card_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_card: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    def get_cards(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(card).where(card.c.user == aime_id)

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()

    def put_character(self, aime_id: int, character_data: Dict) -> Optional[int]:
        character_data["user"] = aime_id

        sql = insert(character).values(**character_data)
        conflict = sql.on_duplicate_key_update(**character_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_character: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid
    
    def get_characters(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(character).where(character.c.user == aime_id)

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()

    def put_deck(self, aime_id: int, deck_data: Dict) -> Optional[int]:
        deck_data["user"] = aime_id

        sql = insert(deck).values(**deck_data)
        conflict = sql.on_duplicate_key_update(**deck_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_deck: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid
    
    def get_deck(self, aime_id: int, deck_id: int) -> Optional[Dict]:
        sql = select(deck).where(and_(deck.c.user == aime_id, deck.c.deckId == deck_id))

        result = self.execute(sql)
        if result is None: return None
        return result.fetchone()
    
    def get_decks(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(deck).where(deck.c.user == aime_id)

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()

    def put_boss(self, aime_id: int, boss_data: Dict) -> Optional[int]:
        boss_data["user"] = aime_id

        sql = insert(boss).values(**boss_data)
        conflict = sql.on_duplicate_key_update(**boss_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_boss: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid
    
    def put_story(self, aime_id: int, story_data: Dict) -> Optional[int]:
        story_data["user"] = aime_id

        sql = insert(story).values(**story_data)
        conflict = sql.on_duplicate_key_update(**story_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_story: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid
    
    def get_stories(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(story).where(story.c.user == aime_id)

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()

    def put_chapter(self, aime_id: int, chapter_data: Dict) -> Optional[int]:
        chapter_data["user"] = aime_id

        sql = insert(chapter).values(**chapter_data)
        conflict = sql.on_duplicate_key_update(**chapter_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_chapter: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid
    
    def get_chapters(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(chapter).where(chapter.c.user == aime_id)

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()

    def put_item(self, aime_id: int, item_data: Dict) -> Optional[int]:
        item_data["user"] = aime_id

        sql = insert(item).values(**item_data)
        conflict = sql.on_duplicate_key_update(**item_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_item: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid
    
    def get_item(self, aime_id: int, item_id: int, item_kind: int) -> Optional[Dict]:
        sql = select(item).where(and_(item.c.user == aime_id, item.c.itemId == item_id))

        result = self.execute(sql)
        if result is None: return None
        return result.fetchone()

    def get_items(self, aime_id: int, item_kind: int = None) -> Optional[List[Dict]]:
        if item_kind is None:
            sql = select(item).where(item.c.user == aime_id)
        else:
            sql = select(item).where(and_(item.c.user == aime_id, item.c.itemKind == item_kind))

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()

    def put_music_item(self, aime_id: int, music_item_data: Dict) -> Optional[int]:
        music_item_data["user"] = aime_id

        sql = insert(music_item).values(**music_item_data)
        conflict = sql.on_duplicate_key_update(**music_item_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_music_item: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid
    
    def get_music_items(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(music_item).where(music_item.c.user == aime_id)
        result = self.execute(sql)

        if result is None: return None
        return result.fetchall()

    def put_login_bonus(self, aime_id: int, login_bonus_data: Dict) -> Optional[int]:
        login_bonus_data["user"] = aime_id

        sql = insert(login_bonus).values(**login_bonus_data)
        conflict = sql.on_duplicate_key_update(**login_bonus_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_login_bonus: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid
    
    def get_login_bonuses(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(login_bonus).where(login_bonus.c.user == aime_id)
        result = self.execute(sql)

        if result is None: return None
        return result.fetchall()

    def put_mission_point(self, aime_id: int, mission_point_data: Dict) -> Optional[int]:
        mission_point_data["user"] = aime_id

        sql = insert(mission_point).values(**mission_point_data)
        conflict = sql.on_duplicate_key_update(**mission_point_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_mission_point: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid
    
    def get_mission_points(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(mission_point).where(mission_point.c.user == aime_id)
        result = self.execute(sql)

        if result is None: return None
        return result.fetchall()
    
    def put_event_point(self, aime_id: int, event_point_data: Dict) -> Optional[int]:
        event_point_data["user"] = aime_id

        sql = insert(event_point).values(**event_point_data)
        conflict = sql.on_duplicate_key_update(**event_point_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_event_point: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid
    
    def get_event_points(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(event_point).where(event_point.c.user == aime_id)
        result = self.execute(sql)

        if result is None: return None
        return result.fetchall()

    def put_scenerio(self, aime_id: int, scenerio_data: Dict) -> Optional[int]:
        scenerio_data["user"] = aime_id

        sql = insert(scenerio).values(**scenerio_data)
        conflict = sql.on_duplicate_key_update(**scenerio_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_scenerio: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid
    
    def get_scenerios(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(scenerio).where(scenerio.c.user == aime_id)
        result = self.execute(sql)

        if result is None: return None
        return result.fetchall()

    def put_trade_item(self, aime_id: int, trade_item_data: Dict) -> Optional[int]:
        trade_item_data["user"] = aime_id

        sql = insert(trade_item).values(**trade_item_data)
        conflict = sql.on_duplicate_key_update(**trade_item_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_trade_item: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid
    
    def get_trade_items(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(trade_item).where(trade_item.c.user == aime_id)
        result = self.execute(sql)

        if result is None: return None
        return result.fetchall()
    
    def put_event_music(self, aime_id: int, event_music_data: Dict) -> Optional[int]:
        event_music_data["user"] = aime_id

        sql = insert(event_music).values(**event_music_data)
        conflict = sql.on_duplicate_key_update(**event_music_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_event_music: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid
    
    def get_event_music(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(event_music).where(event_music.c.user == aime_id)
        result = self.execute(sql)

        if result is None: return None
        return result.fetchall()

    def put_tech_event(self, aime_id: int, tech_event_data: Dict) -> Optional[int]:
        tech_event_data["user"] = aime_id

        sql = insert(tech_event).values(**tech_event_data)
        conflict = sql.on_duplicate_key_update(**tech_event_data)
        result = self.execute(conflict)

        if result is None:
            self.logger.warn(f"put_tech_event: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid
    
    def get_tech_event(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(tech_event).where(tech_event.c.user == aime_id)
        result = self.execute(sql)

        if result is None: return None
        return result.fetchall()

    def get_bosses(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(boss).where(boss.c.user == aime_id)
        result = self.execute(sql)

        if result is None: return None
        return result.fetchall()