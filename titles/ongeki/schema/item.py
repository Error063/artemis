from datetime import date, datetime, timedelta
from typing import Dict, Optional, List
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON
from sqlalchemy.schema import ForeignKey
from sqlalchemy.engine import Row
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
    mysql_charset="utf8mb4",
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
    mysql_charset="utf8mb4",
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
    mysql_charset="utf8mb4",
)

boss = Table(
    "ongeki_user_boss",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("musicId", Integer),
    Column("damage", Integer),
    Column("isClear", Boolean),
    Column("eventId", Integer),
    UniqueConstraint("user", "musicId", "eventId", name="ongeki_user_boss_uk"),
    mysql_charset="utf8mb4",
)

story = Table(
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
    mysql_charset="utf8mb4",
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
    mysql_charset="utf8mb4",
)

memorychapter = Table(
    "ongeki_user_memorychapter",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("chapterId", Integer),
    Column("gaugeId", Integer),
    Column("gaugeNum", Integer),
    Column("jewelCount", Integer),
    Column("isStoryWatched", Boolean),
    Column("isBossWatched", Boolean),
    Column("isDialogWatched", Boolean),
    Column("isEndingWatched", Boolean),
    Column("isClear", Boolean),
    Column("lastPlayMusicId", Integer),
    Column("lastPlayMusicLevel", Integer),
    Column("lastPlayMusicCategory", Integer),
    UniqueConstraint("user", "chapterId", name="ongeki_user_memorychapter_uk"),
    mysql_charset="utf8mb4",
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
    mysql_charset="utf8mb4",
)

music_item = Table(
    "ongeki_user_music_item",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("musicId", Integer),
    Column("status", Integer),
    UniqueConstraint("user", "musicId", name="ongeki_user_music_item_uk"),
    mysql_charset="utf8mb4",
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
    mysql_charset="utf8mb4",
)

event_point = Table(
    "ongeki_user_event_point",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("version", Integer, nullable=False),
    Column("eventId", Integer, nullable=False),
    Column("point", Integer, nullable=False),
    Column("rank", Integer),
    Column("type", Integer, nullable=False),
    Column("date", String(25)),
    Column("isRankingRewarded", Boolean),
    UniqueConstraint("user", "eventId", name="ongeki_user_event_point_uk"),
    mysql_charset="utf8mb4",
)

mission_point = Table(
    "ongeki_user_mission_point",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("version", Integer),
    Column("eventId", Integer),
    Column("point", Integer),
    UniqueConstraint("user", "eventId", name="ongeki_user_mission_point_uk"),
    mysql_charset="utf8mb4",
)

scenerio = Table(
    "ongeki_user_scenerio",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("scenarioId", Integer),
    Column("playCount", Integer),
    UniqueConstraint("user", "scenarioId", name="ongeki_user_scenerio_uk"),
    mysql_charset="utf8mb4",
)

trade_item = Table(
    "ongeki_user_trade_item",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("chapterId", Integer),
    Column("tradeItemId", Integer),
    Column("tradeCount", Integer),
    UniqueConstraint(
        "user", "chapterId", "tradeItemId", name="ongeki_user_trade_item_uk"
    ),
    mysql_charset="utf8mb4",
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
    UniqueConstraint(
        "user", "eventId", "type", "musicId", "level", name="ongeki_user_event_music"
    ),
    mysql_charset="utf8mb4",
)

tech_event = Table(
    "ongeki_user_tech_event",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade")),
    Column("version", Integer, nullable=False),
    Column("eventId", Integer, nullable=False),
    Column("totalTechScore", Integer, nullable=False),
    Column("totalPlatinumScore", Integer, nullable=False),
    Column("techRecordDate", String(25)),
    Column("isRankingRewarded", Boolean),
    Column("isTotalTechNewRecord", Boolean),
    UniqueConstraint("user", "eventId", name="ongeki_user_tech_event_uk"),
    mysql_charset="utf8mb4",
)

tech_ranking = Table(
    "ongeki_tech_event_ranking",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"), nullable=False),
    Column("version", Integer, nullable=False),
    Column("date", String(25)),
    Column("eventId", Integer, nullable=False),
    Column("rank", Integer),
    Column("totalPlatinumScore", Integer, nullable=False),
    Column("totalTechScore", Integer, nullable=False),
    UniqueConstraint("user", "eventId", name="ongeki_tech_event_ranking_uk"),
    mysql_charset="utf8mb4",
)

gacha = Table(
    "ongeki_user_gacha",
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
    Column("selectPoint", Integer, server_default="0"),
    Column("useSelectPoint", Integer, server_default="0"),
    Column("dailyGachaCnt", Integer, server_default="0"),
    Column("fiveGachaCnt", Integer, server_default="0"),
    Column("elevenGachaCnt", Integer, server_default="0"),
    Column("dailyGachaDate", TIMESTAMP, nullable=False, server_default=func.now()),
    UniqueConstraint("user", "gachaId", name="ongeki_user_gacha_uk"),
    mysql_charset="utf8mb4",
)

gacha_supply = Table(
    "ongeki_user_gacha_supply",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("cardId", Integer, nullable=False),
    UniqueConstraint("user", "cardId", name="ongeki_user_gacha_supply_uk"),
    mysql_charset="utf8mb4",
)


print_detail = Table(
    "ongeki_user_print_detail",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("cardId", Integer, nullable=False),
    Column("cardType", Integer, server_default="0"),
    Column("printDate", TIMESTAMP, nullable=False),
    Column("serialId", String(20), nullable=False),
    Column("placeId", Integer, nullable=False),
    Column("clientId", String(11), nullable=False),
    Column("printerSerialId", String(20), nullable=False),
    Column("isHolograph", Boolean, server_default="0"),
    Column("isAutographed", Boolean, server_default="0"),
    Column("printOption1", Boolean, server_default="1"),
    Column("printOption2", Boolean, server_default="1"),
    Column("printOption3", Boolean, server_default="1"),
    Column("printOption4", Boolean, server_default="1"),
    Column("printOption5", Boolean, server_default="1"),
    Column("printOption6", Boolean, server_default="1"),
    Column("printOption7", Boolean, server_default="1"),
    Column("printOption8", Boolean, server_default="1"),
    Column("printOption9", Boolean, server_default="1"),
    Column("printOption10", Boolean, server_default="0"),
    UniqueConstraint("serialId", name="ongeki_user_print_detail_uk"),
    mysql_charset="utf8mb4",
)

class OngekiItemData(BaseData):
    async def put_card(self, aime_id: int, card_data: Dict) -> Optional[int]:
        card_data["user"] = aime_id

        sql = insert(card).values(**card_data)
        conflict = sql.on_duplicate_key_update(**card_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_card: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    async def get_cards(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(card).where(card.c.user == aime_id)

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    async def put_character(self, aime_id: int, character_data: Dict) -> Optional[int]:
        character_data["user"] = aime_id

        sql = insert(character).values(**character_data)
        conflict = sql.on_duplicate_key_update(**character_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_character: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    async def get_characters(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(character).where(character.c.user == aime_id)

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    async def put_deck(self, aime_id: int, deck_data: Dict) -> Optional[int]:
        deck_data["user"] = aime_id

        sql = insert(deck).values(**deck_data)
        conflict = sql.on_duplicate_key_update(**deck_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_deck: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    async def get_deck(self, aime_id: int, deck_id: int) -> Optional[Dict]:
        sql = select(deck).where(and_(deck.c.user == aime_id, deck.c.deckId == deck_id))

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    async def get_decks(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(deck).where(deck.c.user == aime_id)

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    async def put_boss(self, aime_id: int, boss_data: Dict) -> Optional[int]:
        boss_data["user"] = aime_id

        sql = insert(boss).values(**boss_data)
        conflict = sql.on_duplicate_key_update(**boss_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_boss: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    async def put_story(self, aime_id: int, story_data: Dict) -> Optional[int]:
        story_data["user"] = aime_id

        sql = insert(story).values(**story_data)
        conflict = sql.on_duplicate_key_update(**story_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_story: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    async def get_stories(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(story).where(story.c.user == aime_id)

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    async def put_chapter(self, aime_id: int, chapter_data: Dict) -> Optional[int]:
        chapter_data["user"] = aime_id

        sql = insert(chapter).values(**chapter_data)
        conflict = sql.on_duplicate_key_update(**chapter_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_chapter: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    async def get_chapters(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(chapter).where(chapter.c.user == aime_id)

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    async def put_item(self, aime_id: int, item_data: Dict) -> Optional[int]:
        item_data["user"] = aime_id

        sql = insert(item).values(**item_data)
        conflict = sql.on_duplicate_key_update(**item_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_item: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    async def get_item(self, aime_id: int, item_id: int, item_kind: int) -> Optional[Dict]:
        sql = select(item).where(and_(item.c.user == aime_id, item.c.itemId == item_id))

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    async def get_items(self, aime_id: int, item_kind: int = None) -> Optional[List[Dict]]:
        if item_kind is None:
            sql = select(item).where(item.c.user == aime_id)
        else:
            sql = select(item).where(
                and_(item.c.user == aime_id, item.c.itemKind == item_kind)
            )

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    async def put_music_item(self, aime_id: int, music_item_data: Dict) -> Optional[int]:
        music_item_data["user"] = aime_id

        sql = insert(music_item).values(**music_item_data)
        conflict = sql.on_duplicate_key_update(**music_item_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_music_item: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    async def get_music_items(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(music_item).where(music_item.c.user == aime_id)
        result = await self.execute(sql)

        if result is None:
            return None
        return result.fetchall()

    async def put_login_bonus(self, aime_id: int, login_bonus_data: Dict) -> Optional[int]:
        login_bonus_data["user"] = aime_id

        sql = insert(login_bonus).values(**login_bonus_data)
        conflict = sql.on_duplicate_key_update(**login_bonus_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_login_bonus: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    async def get_login_bonuses(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(login_bonus).where(login_bonus.c.user == aime_id)
        result = await self.execute(sql)

        if result is None:
            return None
        return result.fetchall()

    async def put_mission_point(self, aime_id: int, version: int, mission_point_data: Dict) -> Optional[int]:
        mission_point_data["version"] = version
        mission_point_data["user"] = aime_id

        sql = insert(mission_point).values(**mission_point_data)
        conflict = sql.on_duplicate_key_update(**mission_point_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_mission_point: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    async def get_mission_points(self, version: int, aime_id: int) -> Optional[List[Dict]]:
        sql = select(mission_point).where(and_(mission_point.c.user == aime_id, mission_point.c.version == version))
        result = await self.execute(sql)

        if result is None:
            return None
        return result.fetchall()

    async def put_event_point(self, aime_id: int, version: int, event_point_data: Dict) -> Optional[int]:
        # We update only the newest (type: 1) entry, in official spec game watches for both latest(type:1) and previous (type:2) entries to give an additional info how many ranks has player moved up or down
        # This fully featured is on TODO list, at the moment we just update the tables as data comes and give out rank as request comes
        event_point_data["user"] = aime_id
        event_point_data["version"] = version
        event_point_data["type"] = 1
        event_point_time = datetime.now()
        event_point_data["date"] = datetime.strftime(event_point_time, "%Y-%m-%d %H:%M")

        sql = insert(event_point).values(**event_point_data)
        conflict = sql.on_duplicate_key_update(**event_point_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_event_point: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    async def get_event_points(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(event_point).where(event_point.c.user == aime_id)
        result = await self.execute(sql)

        if result is None:
            return None
        return result.fetchall()

    async def put_scenerio(self, aime_id: int, scenerio_data: Dict) -> Optional[int]:
        scenerio_data["user"] = aime_id

        sql = insert(scenerio).values(**scenerio_data)
        conflict = sql.on_duplicate_key_update(**scenerio_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_scenerio: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    async def get_scenerios(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(scenerio).where(scenerio.c.user == aime_id)
        result = await self.execute(sql)

        if result is None:
            return None
        return result.fetchall()

    async def put_trade_item(self, aime_id: int, trade_item_data: Dict) -> Optional[int]:
        trade_item_data["user"] = aime_id

        sql = insert(trade_item).values(**trade_item_data)
        conflict = sql.on_duplicate_key_update(**trade_item_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_trade_item: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    async def get_trade_items(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(trade_item).where(trade_item.c.user == aime_id)
        result = await self.execute(sql)

        if result is None:
            return None
        return result.fetchall()

    async def put_event_music(self, aime_id: int, event_music_data: Dict) -> Optional[int]:
        event_music_data["user"] = aime_id

        sql = insert(event_music).values(**event_music_data)
        conflict = sql.on_duplicate_key_update(**event_music_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_event_music: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    async def get_event_music(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(event_music).where(event_music.c.user == aime_id)
        result = await self.execute(sql)

        if result is None:
            return None
        return result.fetchall()

    async def put_tech_event(self, aime_id: int, version: int, tech_event_data: Dict) -> Optional[int]:
        tech_event_data["user"] = aime_id
        tech_event_data["version"] = version

        sql = insert(tech_event).values(**tech_event_data)
        conflict = sql.on_duplicate_key_update(**tech_event_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_tech_event: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    async def put_tech_event_ranking(self, aime_id: int, version: int, tech_event_data: Dict) -> Optional[int]:
        tech_event_data["user"] = aime_id
        tech_event_data["version"] = version
        tech_event_data.pop("isRankingRewarded")
        tech_event_data.pop("isTotalTechNewRecord")
        tech_event_data["date"] = tech_event_data.pop("techRecordDate")
        tech_event_data["rank"] = 0

        sql = insert(tech_ranking).values(**tech_event_data)
        conflict = sql.on_duplicate_key_update(**tech_event_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_tech_event_ranking: Failed to update ranking! aime_id {aime_id}")
            return None
        return result.lastrowid

    async def get_tech_event(self, version: int, aime_id: int) -> Optional[List[Dict]]:
        sql = select(tech_event).where(and_(tech_event.c.user == aime_id, tech_event.c.version == version))
        result = await self.execute(sql)

        if result is None:
            return None
        return result.fetchall()

    async def get_bosses(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(boss).where(boss.c.user == aime_id)
        result = await self.execute(sql)

        if result is None:
            return None
        return result.fetchall()

    async def put_memorychapter(
        self, aime_id: int, memorychapter_data: Dict
    ) -> Optional[int]:
        memorychapter_data["user"] = aime_id

        sql = insert(memorychapter).values(**memorychapter_data)
        conflict = sql.on_duplicate_key_update(**memorychapter_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_memorychapter: Failed to update! aime_id: {aime_id}")
            return None
        return result.lastrowid

    async def get_memorychapters(self, aime_id: int) -> Optional[List[Dict]]:
        sql = select(memorychapter).where(memorychapter.c.user == aime_id)

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    async def get_user_gacha(self, aime_id: int, gacha_id: int) -> Optional[Row]:
        sql = gacha.select(and_(gacha.c.user == aime_id, gacha.c.gachaId == gacha_id))

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    async def get_user_gachas(self, aime_id: int) -> Optional[List[Row]]:
        sql = gacha.select(gacha.c.user == aime_id)

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    async def get_user_gacha_supplies(self, aime_id: int) -> Optional[List[Row]]:
        sql = gacha_supply.select(gacha_supply.c.user == aime_id)

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    async def put_user_gacha(self, aime_id: int, gacha_id: int, **data) -> Optional[int]:
        sql = insert(gacha).values(user=aime_id, gachaId=gacha_id, **data)

        conflict = sql.on_duplicate_key_update(user=aime_id, gachaId=gacha_id, **data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(f"put_user_gacha: Failed to insert! aime_id: {aime_id}")
            return None
        return result.lastrowid

    async def put_user_print_detail(
        self, aime_id: int, serial_id: str, user_print_data: Dict
    ) -> Optional[int]:
        sql = insert(print_detail).values(
            user=aime_id, serialId=serial_id, **user_print_data
        )

        conflict = sql.on_duplicate_key_update(user=aime_id, **user_print_data)
        result = await self.execute(conflict)

        if result is None:
            self.logger.warning(
                f"put_user_print_detail: Failed to insert! aime_id: {aime_id}"
            )
            return None
        return result.lastrowid


    async def get_ranking_event_ranks(self, version: int, aime_id: int) -> Optional[List[Dict]]:
        # Calculates player rank on GameRequest from server, and sends it back, official spec would rank players in maintenance period, on TODO list
        sql = select(event_point.c.id, event_point.c.user, event_point.c.eventId, event_point.c.type, func.row_number().over(partition_by=event_point.c.eventId, order_by=event_point.c.point.desc()).label('rank'), event_point.c.date, event_point.c.point).where(event_point.c.version == version)
        result = await self.execute(sql)
        if result is None:
            self.logger.error(f"failed to rank aime_id: {aime_id} ranking event positions")
            return None
        return result.fetchall()

    async def get_tech_event_ranking(self, version: int, aime_id: int) -> Optional[List[Dict]]:
        sql = select(tech_ranking.c.id, tech_ranking.c.user, tech_ranking.c.date, tech_ranking.c.eventId, func.row_number().over(partition_by=tech_ranking.c.eventId, order_by=[tech_ranking.c.totalTechScore.desc(),tech_ranking.c.totalPlatinumScore.desc()]).label('rank'), tech_ranking.c.totalTechScore, tech_ranking.c.totalPlatinumScore).where(tech_ranking.c.version == version)
        result = await self.execute(sql)
        if result is None:
            self.logger.warning(f"aime_id: {aime_id} has no tech ranking ranks")
            return None
        return result.fetchall()
