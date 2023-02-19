from enum import Enum
from typing import Dict, Optional
from sqlalchemy import Table, Column, and_
from sqlalchemy.types import Integer, String, TIMESTAMP
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.sql import func, select, Delete
from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy.engine import Row

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
    Column("ip", String(15)),
    Column('session_cookie', String(32), nullable=False, unique=True),
    Column("expires", TIMESTAMP, nullable=False),
    mysql_charset='utf8mb4'
)

class PermissionBits(Enum):
    PermUser = 1
    PermMod = 2
    PermSysAdmin = 4

class UserData(BaseData):
    def create_user(self, id: int = None, username: str = None, email: str = None, password: str = None, permission: int = 1) -> Optional[int]:
        if email is None:
            permission = 1

        if id is None:
            sql = insert(aime_user).values(
                username=username, 
                email=email, 
                password=password, 
                permissions=permission
            )
        else:
            sql = insert(aime_user).values(
                id=id, 
                username=username, 
                email=email, 
                password=password, 
                permissions=permission
            )

        conflict = sql.on_duplicate_key_update(
            username=username, 
            email=email, 
            password=password, 
            permissions=permission
        )
        
        result = self.execute(conflict)
        if result is None: return None
        return result.lastrowid
    
    def login(self, user_id: int, passwd: bytes = None, ip: str = "0.0.0.0") -> Optional[str]:
        sql = select(aime_user).where(and_(aime_user.c.id == user_id, aime_user.c.password == passwd))

        result = self.execute(sql)
        if result is None: return None
        
        usr = result.fetchone()
        if usr is None: return None

        return self.create_session(user_id, ip)
    
    def check_session(self, cookie: str, ip: str = "0.0.0.0") -> Optional[Row]:
        sql = select(frontend_session).where(
            and_(
                frontend_session.c.session_cookie == cookie,
                frontend_session.c.ip == ip
            )
        )

        result = self.execute(sql)
        if result is None: return None        
        return result.fetchone()
    
    def delete_session(self, session_id: int) -> bool:
        sql = Delete(frontend_session).where(frontend_session.c.id == session_id)

        result = self.execute(sql)
        if result is None: return False
        return True

    def create_session(self, user_id: int, ip: str = "0.0.0.0", expires: datetime = datetime.now() + timedelta(days=1)) -> Optional[str]:
        cookie = uuid4().hex

        sql = insert(frontend_session).values(
            user = user_id,
            ip = ip,
            session_cookie = cookie,
            expires = expires
        )

        result = self.execute(sql)
        if result is None:
            return None
        return cookie

    def reset_autoincrement(self, ai_value: int) -> None:
        # ALTER TABLE isn't in sqlalchemy so we do this the ugly way
        sql = f"ALTER TABLE aime_user AUTO_INCREMENT={ai_value}"
        self.execute(sql)