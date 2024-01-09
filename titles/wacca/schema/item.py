from typing import Optional, Dict, List
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_, case
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select, update, delete
from sqlalchemy.engine import Row
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

item = Table(
    "wacca_item",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("item_id", Integer, nullable=False),
    Column("type", Integer, nullable=False),
    Column("acquire_date", TIMESTAMP, nullable=False, server_default=func.now()),
    Column("use_count", Integer, server_default="0"),
    UniqueConstraint("user", "item_id", "type", name="wacca_item_uk"),
    mysql_charset="utf8mb4",
)

ticket = Table(
    "wacca_ticket",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("ticket_id", Integer, nullable=False),
    Column("acquire_date", TIMESTAMP, nullable=False, server_default=func.now()),
    Column("expire_date", TIMESTAMP),
    mysql_charset="utf8mb4",
)

song_unlock = Table(
    "wacca_song_unlock",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("song_id", Integer, nullable=False),
    Column("highest_difficulty", Integer, nullable=False),
    Column("acquire_date", TIMESTAMP, nullable=False, server_default=func.now()),
    UniqueConstraint("user", "song_id", name="wacca_song_unlock_uk"),
    mysql_charset="utf8mb4",
)

trophy = Table(
    "wacca_trophy",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("trophy_id", Integer, nullable=False),
    Column("season", Integer, nullable=False),
    Column("progress", Integer, nullable=False, server_default="0"),
    Column("badge_type", Integer, nullable=False, server_default="0"),
    UniqueConstraint("user", "trophy_id", "season", name="wacca_trophy_uk"),
    mysql_charset="utf8mb4",
)


class WaccaItemData(BaseData):
    async def get_song_unlocks(self, user_id: int) -> Optional[List[Row]]:
        sql = song_unlock.select(song_unlock.c.user == user_id)

        result = await self.execute(sql)
        if result is None:
            return None

        return result.fetchall()

    async def unlock_song(self, user_id: int, song_id: int, difficulty: int) -> Optional[int]:
        sql = insert(song_unlock).values(
            user=user_id, song_id=song_id, highest_difficulty=difficulty
        )

        conflict = sql.on_duplicate_key_update(
            highest_difficulty=case(
                (
                    song_unlock.c.highest_difficulty >= difficulty,
                    song_unlock.c.highest_difficulty,
                ),
                (song_unlock.c.highest_difficulty < difficulty, difficulty),
            )
        )

        result = await self.execute(conflict)
        if result is None:
            self.logger.error(
                f"{__name__} failed to unlock song! user: {user_id}, song_id: {song_id}, difficulty: {difficulty}"
            )
            return None

        return result.lastrowid

    async def put_item(self, user_id: int, item_type: int, item_id: int) -> Optional[int]:
        sql = insert(item).values(
            user=user_id,
            item_id=item_id,
            type=item_type,
        )

        conflict = sql.on_duplicate_key_update(use_count=item.c.use_count + 1)

        result = await self.execute(conflict)
        if result is None:
            self.logger.error(
                f"{__name__} failed to insert item! user: {user_id}, item_id: {item_id}, item_type: {item_type}"
            )
            return None

        return result.lastrowid

    async def get_items(
        self, user_id: int, item_type: int = None, item_id: int = None
    ) -> Optional[List[Row]]:
        """
        A catch-all item lookup given a profile and option item type and ID specifiers
        """
        sql = item.select(
            and_(
                item.c.user == user_id,
                item.c.type == item_type if item_type is not None else True,
                item.c.item_id == item_id if item_id is not None else True,
            )
        )

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    async def get_tickets(self, user_id: int) -> Optional[List[Row]]:
        sql = select(ticket).where(ticket.c.user == user_id)

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    async def add_ticket(self, user_id: int, ticket_id: int) -> None:
        sql = insert(ticket).values(user=user_id, ticket_id=ticket_id)

        result = await self.execute(sql)
        if result is None:
            self.logger.error(
                f"add_ticket: Failed to insert wacca ticket! user_id: {user_id} ticket_id {ticket_id}"
            )
            return None
        return result.lastrowid

    async def spend_ticket(self, id: int) -> None:
        sql = delete(ticket).where(ticket.c.id == id)

        result = await self.execute(sql)
        if result is None:
            self.logger.warning(f"Failed to delete ticket id {id}")
            return None

    async def get_trophies(self, user_id: int, season: int = None) -> Optional[List[Row]]:
        if season is None:
            sql = select(trophy).where(trophy.c.user == user_id)
        else:
            sql = select(trophy).where(
                and_(trophy.c.user == user_id, trophy.c.season == season)
            )

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    async def update_trophy(
        self, user_id: int, trophy_id: int, season: int, progress: int, badge_type: int
    ) -> Optional[int]:
        sql = insert(trophy).values(
            user=user_id,
            trophy_id=trophy_id,
            season=season,
            progress=progress,
            badge_type=badge_type,
        )

        conflict = sql.on_duplicate_key_update(progress=progress)

        result = await self.execute(conflict)
        if result is None:
            self.logger.error(
                f"update_trophy: Failed to insert wacca trophy! user_id: {user_id} trophy_id: {trophy_id} progress {progress}"
            )
            return None
        return result.lastrowid
