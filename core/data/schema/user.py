from enum import Enum
from typing import Optional, List
from sqlalchemy import Table, Column
from sqlalchemy.types import Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.sql import func, select
from sqlalchemy.engine import Row
import bcrypt

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
    mysql_charset="utf8mb4",
)


class PermissionBits(Enum):
    PermUser = 1
    PermMod = 2
    PermSysAdmin = 4


class UserData(BaseData):
    def create_user(
        self,
        id: int = None,
        username: str = None,
        email: str = None,
        password: str = None,
        permission: int = 1,
    ) -> Optional[int]:
        if id is None:
            sql = insert(aime_user).values(
                username=username,
                email=email,
                password=password,
                permissions=permission,
            )
        else:
            sql = insert(aime_user).values(
                id=id,
                username=username,
                email=email,
                password=password,
                permissions=permission,
            )

        conflict = sql.on_duplicate_key_update(
            username=username, email=email, password=password, permissions=permission
        )

        result = self.execute(conflict)
        if result is None:
            return None
        return result.lastrowid

    def get_user(self, user_id: int) -> Optional[Row]:
        sql = select(aime_user).where(aime_user.c.id == user_id)
        result = self.execute(sql)
        if result is None:
            return False
        return result.fetchone()

    def check_password(self, user_id: int, passwd: bytes = None) -> bool:
        usr = self.get_user(user_id)
        if usr is None:
            return False

        if usr["password"] is None:
            return False
        
        if passwd is None or not passwd:
            return False

        return bcrypt.checkpw(passwd, usr["password"].encode())

    def reset_autoincrement(self, ai_value: int) -> None:
        # ALTER TABLE isn't in sqlalchemy so we do this the ugly way
        sql = f"ALTER TABLE aime_user AUTO_INCREMENT={ai_value}"
        self.execute(sql)

    def delete_user(self, user_id: int) -> None:
        sql = aime_user.delete(aime_user.c.id == user_id)

        result = self.execute(sql)
        if result is None:
            self.logger.error(f"Failed to delete user with id {user_id}")

    def get_unregistered_users(self) -> List[Row]:
        """
        Returns a list of users who have not registered with the webui. They may or may not have cards.
        """
        sql = select(aime_user).where(aime_user.c.password == None)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchall()

    def find_user_by_email(self, email: str) -> Row:
        sql = select(aime_user).where(aime_user.c.email == email)
        result = self.execute(sql)
        if result is None:
            return False
        return result.fetchone()

    def find_user_by_username(self, username: str) -> List[Row]:
        sql = aime_user.select(aime_user.c.username.like(f"%{username}%"))
        result = self.execute(sql)
        if result is None:
            return False
        return result.fetchall()
