from typing import Optional, Dict
from sqlalchemy import Table, Column
from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.sql import func, select
from sqlalchemy.dialects.mysql import insert

from core.data.schema.base import BaseData, metadata

arcade = Table(
    "arcade",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("name", String(255)),
    Column("nickname", String(255)),    
    Column("country", String(3)),
    Column("country_id", Integer),
    Column("state", String(255)),
    Column("city", String(255)),
    Column("region_id", Integer),
    Column("timezone", String(255)),
    mysql_charset='utf8mb4'
)

machine = Table(
    "machine",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("arcade", ForeignKey("arcade.id", ondelete="cascade", onupdate="cascade"), nullable=False),    
    Column("serial", String(15), nullable=False),
    Column("board", String(15)),
    Column("game", String(4)),
    Column("country", String(3)), # overwrites if not null
    Column("timezone", String(255)),
    Column("ota_enable", Boolean),
    Column("is_cab", Boolean),
    mysql_charset='utf8mb4'
)

arcade_owner = Table(
    'arcade_owner',
    metadata,
    Column('user', Integer, ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"), nullable=False),
    Column('arcade', Integer, ForeignKey("arcade.id", ondelete="cascade", onupdate="cascade"), nullable=False),
    Column('permissions', Integer, nullable=False),
    PrimaryKeyConstraint('user', 'arcade', name='arcade_owner_pk'),
    mysql_charset='utf8mb4'
)

class ArcadeData(BaseData):
    def get_machine(self, serial: str = None, id: int = None) -> Optional[Dict]:
        if serial is not None:
            sql = machine.select(machine.c.serial == serial)
        elif id is not None:
            sql = machine.select(machine.c.id == id)
        else: 
            self.logger.error(f"{__name__ }: Need either serial or ID to look up!")
            return None
        
        result = self.execute(sql)
        if result is None: return None
        return result.fetchone()
    
    def put_machine(self, arcade_id: int, serial: str = None, board: str = None, game: str = None, is_cab: bool = False) -> Optional[int]:
        if arcade_id:
            self.logger.error(f"{__name__ }: Need arcade id!")
            return None

        if serial is None:
            pass

        sql = machine.insert().values(arcade = arcade_id, keychip = serial, board = board, game = game, is_cab = is_cab)
        
        result = self.execute(sql)
        if result is None: return None
        return result.lastrowid
    
    def get_arcade(self, id: int) -> Optional[Dict]:
        sql = arcade.select(arcade.c.id == id)
        result = self.execute(sql)
        if result is None: return None
        return result.fetchone()
    
    def put_arcade(self, name: str, nickname: str = None, country: str = "JPN", country_id: int = 1, 
        state: str = "", city: str = "", regional_id: int = 1) -> Optional[int]:
        if nickname is None: nickname = name

        sql = arcade.insert().values(name = name, nickname = nickname, country = country, country_id = country_id,
        state = state, city = city, regional_id = regional_id)

        result = self.execute(sql)
        if result is None: return None
        return result.lastrowid

    def get_arcade_owners(self, arcade_id: int) -> Optional[Dict]:
        sql = select(arcade_owner).where(arcade_owner.c.arcade==arcade_id)

        result = self.execute(sql)
        if result is None: return None
        return result.fetchall()

    def add_arcade_owner(self, arcade_id: int, user_id: int) -> None:
        sql = insert(arcade_owner).values(
            arcade=arcade_id,
            user=user_id
        )

        result = self.execute(sql)
        if result is None: return None
        return result.lastrowid

    def generate_keychip_serial(self, platform_id: int) -> str:
        pass