from typing import Dict, List, Optional
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON, Float
from sqlalchemy.engine.base import Connection
from sqlalchemy.engine import Row
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata

quest = Table(
    "sao_static_quest",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer),
    Column("questSceneId", Integer),
    Column("sortNo", Integer),
    Column("name", String(255)),
    Column("enabled", Boolean),
    UniqueConstraint(
        "version", "questSceneId", name="sao_static_quest_uk"
    ),
    mysql_charset="utf8mb4",
)

hero = Table(
    "sao_static_hero_list",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer),
    Column("heroLogId", Integer),
    Column("name", String(255)),
    Column("nickname", String(255)),
    Column("rarity", Integer),
    Column("skillTableSubId", Integer),
    Column("awakeningExp", Integer),
    Column("flavorText", String(255)),
    Column("enabled", Boolean),
    UniqueConstraint(
        "version", "heroLogId", name="sao_static_hero_list_uk"
    ),
    mysql_charset="utf8mb4",
)

equipment = Table(
    "sao_static_equipment_list",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer),
    Column("equipmentId", Integer),
    Column("equipmentType", Integer),
    Column("weaponTypeId", Integer),
    Column("name", String(255)),
    Column("rarity", Integer),
    Column("flavorText", String(255)),
    Column("enabled", Boolean),
    UniqueConstraint(
        "version", "equipmentId", name="sao_static_equipment_list_uk"
    ),
    mysql_charset="utf8mb4",
)

item = Table(
    "sao_static_item_list",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer),
    Column("itemId", Integer),
    Column("itemTypeId", Integer),
    Column("name", String(255)),
    Column("rarity", Integer),
    Column("flavorText", String(255)),
    Column("enabled", Boolean),
    UniqueConstraint(
        "version", "itemId", name="sao_static_item_list_uk"
    ),
    mysql_charset="utf8mb4",
)

support = Table(
    "sao_static_support_log_list",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer),
    Column("supportLogId", Integer),
    Column("charaId", Integer),
    Column("name", String(255)),
    Column("rarity", Integer),
    Column("salePrice", Integer),
    Column("skillName", String(255)),
    Column("enabled", Boolean),
    UniqueConstraint(
        "version", "supportLogId", name="sao_static_support_log_list_uk"
    ),
    mysql_charset="utf8mb4",
)

rare_drop = Table(
    "sao_static_rare_drop_list",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer),
    Column("questRareDropId", Integer),
    Column("commonRewardId", Integer),
    Column("enabled", Boolean),
    UniqueConstraint(
        "version", "questRareDropId", "commonRewardId", name="sao_static_rare_drop_list_uk"
    ),
    mysql_charset="utf8mb4",
)

title = Table(
    "sao_static_title_list",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("version", Integer),
    Column("titleId", Integer),
    Column("displayName", String(255)),
    Column("requirement", Integer),
    Column("rank", Integer),
    Column("imageFilePath", String(255)),
    Column("enabled", Boolean),
    UniqueConstraint(
        "version", "titleId", name="sao_static_title_list_uk"
    ),
    mysql_charset="utf8mb4",
)

class SaoStaticData(BaseData):
    def put_quest( self, questSceneId: int, version: int, sortNo: int, name: str, enabled: bool ) -> Optional[int]:
        sql = insert(quest).values(
            questSceneId=questSceneId,
            version=version,
            sortNo=sortNo,
            name=name,
            tutorial=tutorial,
        )

        conflict = sql.on_duplicate_key_update(
            name=name, questSceneId=questSceneId, version=version
        )

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid
    
    def put_hero( self, version: int, heroLogId: int, name: str, nickname: str, rarity: int, skillTableSubId: int, awakeningExp: int, flavorText: str, enabled: bool ) -> Optional[int]:
        sql = insert(hero).values(
            version=version,
            heroLogId=heroLogId,
            name=name,
            nickname=nickname,
            rarity=rarity,
            skillTableSubId=skillTableSubId,
            awakeningExp=awakeningExp,
            flavorText=flavorText,
            enabled=enabled
        )

        conflict = sql.on_duplicate_key_update(
            name=name, heroLogId=heroLogId
        )

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid
    
    def put_equipment( self, version: int, equipmentId: int, name: str, equipmentType: int, weaponTypeId:int, rarity: int, flavorText: str, enabled: bool ) -> Optional[int]:
        sql = insert(equipment).values(
            version=version,
            equipmentId=equipmentId,
            name=name,
            equipmentType=equipmentType,
            weaponTypeId=weaponTypeId,
            rarity=rarity,
            flavorText=flavorText,
            enabled=enabled
        )

        conflict = sql.on_duplicate_key_update(
            name=name, equipmentId=equipmentId
        )

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid
    
    def put_item( self, version: int, itemId: int, name: str, itemTypeId: int, rarity: int, flavorText: str, enabled: bool ) -> Optional[int]:
        sql = insert(item).values(
            version=version,
            itemId=itemId,
            name=name,
            itemTypeId=itemTypeId,
            rarity=rarity,
            flavorText=flavorText,
            enabled=enabled
        )

        conflict = sql.on_duplicate_key_update(
            name=name, itemId=itemId
        )

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid
    
    def put_support_log( self, version: int, supportLogId: int, charaId: int, name: str, rarity: int, salePrice: int, skillName: str, enabled: bool ) -> Optional[int]:
        sql = insert(support).values(
            version=version,
            supportLogId=supportLogId,
            charaId=charaId,
            name=name,
            rarity=rarity,
            salePrice=salePrice,
            skillName=skillName,
            enabled=enabled
        )

        conflict = sql.on_duplicate_key_update(
            name=name, supportLogId=supportLogId
        )

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid

    def put_rare_drop( self, version: int, questRareDropId: int, commonRewardId: int, enabled: bool ) -> Optional[int]:
        sql = insert(rare_drop).values(
            version=version,
            questRareDropId=questRareDropId,
            commonRewardId=commonRewardId,
            enabled=enabled,
        )

        conflict = sql.on_duplicate_key_update(
            questRareDropId=questRareDropId, commonRewardId=commonRewardId, version=version
        )

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid
    
    def put_title( self, version: int, titleId: int, displayName: str, requirement: int, rank: int, imageFilePath: str, enabled: bool ) -> Optional[int]:
        sql = insert(title).values(
            version=version,
            titleId=titleId,
            displayName=displayName,
            requirement=requirement,
            rank=rank,
            imageFilePath=imageFilePath,
            enabled=enabled
        )

        conflict = sql.on_duplicate_key_update(
            displayName=displayName, titleId=titleId
        )

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid

    def get_quests_id(self, sortNo: int) -> Optional[Dict]:
        sql = quest.select(quest.c.sortNo == sortNo)
        
        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_quests_ids(self, version: int, enabled: bool) -> Optional[List[Dict]]:
        sql = quest.select(quest.c.version == version and quest.c.enabled == enabled).order_by(
            quest.c.questSceneId.asc()
        )

        result = self.execute(sql)
        if result is None:
            return None
        return [list[2] for list in result.fetchall()]
    
    def get_hero_id(self, heroLogId: int) -> Optional[Dict]:
        sql = hero.select(hero.c.heroLogId == heroLogId)
        
        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()
    
    def get_hero_ids(self, version: int, enabled: bool) -> Optional[List[Dict]]:
        sql = hero.select(hero.c.version == version and hero.c.enabled == enabled).order_by(
            hero.c.heroLogId.asc()
        )

        result = self.execute(sql)
        if result is None:
            return None
        return [list[2] for list in result.fetchall()]
    
    def get_equipment_id(self, equipmentId: int) -> Optional[Dict]:
        sql = equipment.select(equipment.c.equipmentId == equipmentId)
        
        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()
    
    def get_equipment_ids(self, version: int, enabled: bool) -> Optional[List[Dict]]:
        sql = equipment.select(equipment.c.version == version and equipment.c.enabled == enabled).order_by(
            equipment.c.equipmentId.asc()
        )

        result = self.execute(sql)
        if result is None:
            return None
        return [list[2] for list in result.fetchall()]

    def get_item_id(self, itemId: int) -> Optional[Dict]:
        sql = item.select(item.c.itemId == itemId)
        
        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()

    def get_rare_drop_id(self, questRareDropId: int) -> Optional[Dict]:
        sql = rare_drop.select(rare_drop.c.questRareDropId == questRareDropId)
        
        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()
    
    def get_item_ids(self, version: int, enabled: bool) -> Optional[List[Dict]]:
        sql = item.select(item.c.version == version and item.c.enabled == enabled).order_by(
            item.c.itemId.asc()
        )

        result = self.execute(sql)
        if result is None:
            return None
        return [list[2] for list in result.fetchall()]
    
    def get_support_log_ids(self, version: int, enabled: bool) -> Optional[List[Dict]]:
        sql = support.select(support.c.version == version and support.c.enabled == enabled).order_by(
            support.c.supportLogId.asc()
        )

        result = self.execute(sql)
        if result is None:
            return None
        return [list[2] for list in result.fetchall()]
    
    def get_title_ids(self, version: int, enabled: bool) -> Optional[List[Dict]]:
        sql = title.select(title.c.version == version and title.c.enabled == enabled).order_by(
            title.c.titleId.asc()
        )

        result = self.execute(sql)
        if result is None:
            return None
        return [list[2] for list in result.fetchall()]