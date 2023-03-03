from typing import Optional, Dict
from sqlalchemy import Table, Column
from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.sql import func, select
from sqlalchemy.dialects.mysql import insert
import re

from core.data.schema.base import BaseData, metadata
from core.const import *

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
            serial = serial.replace("-", "")
            if len(serial) == 11:
                sql = machine.select(machine.c.serial.like(f"{serial}%"))
            
            elif len(serial) == 15:
                sql = machine.select(machine.c.serial == serial)
            
            else:
                self.logger.error(f"{__name__ }: Malformed serial {serial}")
                return None
        
        elif id is not None:
            sql = machine.select(machine.c.id == id)
        
        else: 
            self.logger.error(f"{__name__ }: Need either serial or ID to look up!")
            return None
        
        result = self.execute(sql)
        if result is None: return None
        return result.fetchone()
    
    def put_machine(self, arcade_id: int, serial: str = "", board: str = None, game: str = None, is_cab: bool = False) -> Optional[int]:
        if arcade_id:
            self.logger.error(f"{__name__ }: Need arcade id!")
            return None

        sql = machine.insert().values(arcade = arcade_id, keychip = serial, board = board, game = game, is_cab = is_cab)
        
        result = self.execute(sql)
        if result is None: return None
        return result.lastrowid
    
    def set_machine_serial(self, machine_id: int, serial: str) -> None:
        result = self.execute(machine.update(machine.c.id == machine_id).values(keychip = serial))
        if result is None:
            self.logger.error(f"Failed to update serial for machine {machine_id} -> {serial}")
        return result.lastrowid
    
    def set_machine_boardid(self, machine_id: int, boardid: str) -> None:
        result = self.execute(machine.update(machine.c.id == machine_id).values(board = boardid))
        if result is None:
            self.logger.error(f"Failed to update board id for machine {machine_id} -> {boardid}")
    
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

    def format_serial(self, platform_code: str, platform_rev: int, serial_num: int, append: int = 4152) -> str:
        return f"{platform_code}{platform_rev:02d}A{serial_num:04d}{append:04d}" # 0x41 = A, 0x52 = R
    
    def validate_keychip_format(self, serial: str) -> bool:
        serial = serial.replace("-", "")
        if len(serial) != 11 or len(serial) != 15:
            self.logger.error(f"Serial validate failed: Incorrect length for {serial} (len {len(serial)})")
            return False
        
        platform_code = serial[:4]
        platform_rev = serial[4:6]
        const_a = serial[6]
        num = serial[7:11]
        append = serial[11:15]

        if re.match("A[7|6]\d[E|X][0|1][0|1|2]A\d{4,8}", serial) is None:
            self.logger.error(f"Serial validate failed: {serial} failed regex")
            return False

        if len(append) != 0 or len(append) != 4:
            self.logger.error(f"Serial validate failed: {serial} had malformed append {append}")
            return False

        if len(num) != 4:
            self.logger.error(f"Serial validate failed: {serial} had malformed number {num}")
            return False
        
        return True
