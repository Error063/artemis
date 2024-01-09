from typing import Dict, List, Optional
from sqlalchemy import Table, Column, UniqueConstraint
from sqlalchemy.types import Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.engine import Row

from core.data.schema.base import BaseData, metadata

aime_card = Table(
    "aime_card",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("access_code", String(20)),
    Column("created_date", TIMESTAMP, server_default=func.now()),
    Column("last_login_date", TIMESTAMP, onupdate=func.now()),
    Column("is_locked", Boolean, server_default="0"),
    Column("is_banned", Boolean, server_default="0"),
    UniqueConstraint("user", "access_code", name="aime_card_uk"),
    mysql_charset="utf8mb4",
)


class CardData(BaseData):
    async def get_card_by_access_code(self, access_code: str) -> Optional[Row]:
        sql = aime_card.select(aime_card.c.access_code == access_code)

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    async def get_card_by_id(self, card_id: int) -> Optional[Row]:
        sql = aime_card.select(aime_card.c.id == card_id)

        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    async def update_access_code(self, old_ac: str, new_ac: str) -> None:
        sql = aime_card.update(aime_card.c.access_code == old_ac).values(
            access_code=new_ac
        )

        result = await self.execute(sql)
        if result is None:
            self.logger.error(
                f"Failed to change card access code from {old_ac} to {new_ac}"
            )

    async def get_user_id_from_card(self, access_code: str) -> Optional[int]:
        """
        Given a 20 digit access code as a string, get the user id associated with that card
        """
        card = self.get_card_by_access_code(access_code)
        if card is None:
            return None

        return int(card["user"])

    async def get_card_banned(self, access_code: str) -> Optional[bool]:
        """
        Given a 20 digit access code as a string, check if the card is banned
        """
        card = self.get_card_by_access_code(access_code)
        if card is None:
            return None
        if card["is_banned"]:
            return True
        return False
    async def get_card_locked(self, access_code: str) -> Optional[bool]:
        """
        Given a 20 digit access code as a string, check if the card is locked
        """
        card = self.get_card_by_access_code(access_code)
        if card is None:
            return None
        if card["is_locked"]:
            return True
        return False

    async def delete_card(self, card_id: int) -> None:
        sql = aime_card.delete(aime_card.c.id == card_id)

        result = await self.execute(sql)
        if result is None:
            self.logger.error(f"Failed to delete card with id {card_id}")

    async def get_user_cards(self, aime_id: int) -> Optional[List[Row]]:
        """
        Returns all cards owned by a user
        """
        sql = aime_card.select(aime_card.c.user == aime_id)
        result = await self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    async def create_card(self, user_id: int, access_code: str) -> Optional[int]:
        """
        Given a aime_user id and a 20 digit access code as a string, create a card and return the ID if successful
        """
        sql = aime_card.insert().values(user=user_id, access_code=access_code)
        result = await self.execute(sql)
        if result is None:
            return None
        return result.lastrowid

    def to_access_code(self, luid: str) -> str:
        """
        Given a felica cards internal 16 hex character luid, convert it to a 0-padded 20 digit access code as a string
        """
        return f"{int(luid, base=16):0{20}}"

    def to_idm(self, access_code: str) -> str:
        """
        Given a 20 digit access code as a string, return the 16 hex character luid
        """
        return f"{int(access_code):0{16}x}"
