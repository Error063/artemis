from enum import Enum
from typing import Dict, Optional
from sqlalchemy import Table, Column
from sqlalchemy.types import Integer, String, TIMESTAMP
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql import func

from core.data.schema.base import BaseData, metadata

aime_user = Table(
    "aime_user",
    metadata,
    Column("id", Integer, nullable=False, primary_key=True, autoincrement=True),
    Column("username", String(25), unique=True),
    Column("email", String(255), unique=True),
    Column("password", String(255)),
    Column("permissions", Integer),    
    Column("created_date", TIMESTAMP, server_default=func.now()),
    Column("last_login_date", TIMESTAMP, onupdate=func.now()),
    Column("suspend_expire_time", TIMESTAMP),
    mysql_charset='utf8mb4'
)

frontend_session = Table(
    "frontend_session",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("user", ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"), nullable=False),
    Column('session_cookie', String(32), nullable=False, unique=True),
    Column("expires", TIMESTAMP, nullable=False),
    mysql_charset='utf8mb4'
)

class PermissionBits(Enum):
    PermUser = 1
    PermMod = 2
    PermSysAdmin = 4

class UserData(BaseData):
    def create_user(self, username: str = None, email: str = None, password: str = None) -> Optional[int]:

        if email is None:
            permission = None
        else:
            permission = 0

        sql = aime_user.insert().values(username=username, email=email, password=password, permissions=permission)
        
        result = self.execute(sql)
        if result is None: return None
        return result.lastrowid
    
    def reset_autoincrement(self, ai_value: int) -> None:
        # Didn't feel like learning how to do this the right way
        # if somebody wants a free PR go nuts I guess
        sql = f"ALTER TABLE aime_user AUTO_INCREMENT={ai_value}"
        self.execute(sql)