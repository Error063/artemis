from typing import Optional, Dict, List
from sqlalchemy import Table, Column, UniqueConstraint, and_
from sqlalchemy.types import Integer
from sqlalchemy.schema import ForeignKey
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

customize = Table(
    "diva_profile_customize_item",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "user",
        ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    ),
    Column("version", Integer, nullable=False),
    Column("item_id", Integer, nullable=False),
    UniqueConstraint(
        "user", "version", "item_id", name="diva_profile_customize_item_uk"
    ),
    mysql_charset="utf8mb4",
)


class DivaCustomizeItemData(BaseData):
    def put_customize_item(self, aime_id: int, version: int, item_id: int) -> None:
        sql = insert(customize).values(version=version, user=aime_id, item_id=item_id)

        result = self.execute(sql)
        if result is None:
            self.logger.error(
                f"{__name__} Failed to insert diva profile customize item! aime id: {aime_id} item: {item_id}"
            )
            return None
        return result.lastrowid

    def get_customize_items(self, aime_id: int, version: int) -> Optional[List[Dict]]:
        """
        Given a game version and an aime id, return all the customize items, not used directly
        """
        sql = customize.select(
            and_(customize.c.version == version, customize.c.user == aime_id)
        )

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_customize_items_have_string(self, aime_id: int, version: int) -> str:
        """
        Given a game version and an aime id, return the cstmz_itm_have hex string
        required for diva directly
        """
        items_list = self.get_customize_items(aime_id, version)
        if items_list is None:
            items_list = []
        item_have = 0

        for item in items_list:
            item_have |= 1 << item["item_id"]

        # convert the int to a 250 digit long hex string
        return "{0:0>250}".format(hex(item_have).upper()[2:])
