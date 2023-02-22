from typing import Optional, Dict, List
from sqlalchemy import Table, Column, UniqueConstraint, and_
from sqlalchemy.types import Integer
from sqlalchemy.schema import ForeignKey
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

module = Table(
    "diva_profile_module",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"), nullable=False),
    Column("version", Integer, nullable=False),
    Column("module_id", Integer, nullable=False),
    UniqueConstraint("user", "version", "module_id", name="diva_profile_module_uk"),
    mysql_charset='utf8mb4'
)


class DivaModuleData(BaseData):
    def put_module(self, aime_id: int, version: int, module_id: int) -> None:
        sql = insert(module).values(
            version=version,
            user=aime_id,
            module_id=module_id
        )

        result = self.execute(sql)
        if result is None:
            self.logger.error(f"{__name__} Failed to insert diva profile module! aime id: {aime_id} module: {module_id}")
            return None
        return result.lastrowid

    def get_modules(self, aime_id: int, version: int) -> Optional[List[Dict]]:
        """
        Given a game version and an aime id, return all the modules, not used directly
        """
        sql = module.select(and_(
                module.c.version == version,
                module.c.user == aime_id
            ))

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def get_modules_have_string(self, aime_id: int, version: int) -> str:
        """
        Given a game version and an aime id, return the mdl_have hex string
        required for diva directly
        """
        module_list = self.get_modules(aime_id, version)
        if module_list is None:
            module_list = []
        module_have = 0

        for module in module_list:
            module_have |= 1 << module["module_id"]

        # convert the int to a 250 digit long hex string
        return "{0:0>250}".format(hex(module_have).upper()[2:])
