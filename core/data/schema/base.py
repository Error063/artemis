import json
import logging
from random import randrange
from typing import Any, Optional, Dict, List
from sqlalchemy.engine import Row
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine.base import Connection
from sqlalchemy.sql import text, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import MetaData, Table, Column
from sqlalchemy.types import Integer, String, TIMESTAMP, JSON
from sqlalchemy.dialects.mysql import insert

from core.config import CoreConfig

metadata = MetaData()

schema_ver = Table(
    "schema_versions",
    metadata,
    Column("game", String(4), primary_key=True, nullable=False),
    Column("version", Integer, nullable=False, server_default="1"),
    mysql_charset="utf8mb4",
)

event_log = Table(
    "event_log",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("system", String(255), nullable=False),
    Column("type", String(255), nullable=False),
    Column("severity", Integer, nullable=False),
    Column("message", String(1000), nullable=False),
    Column("details", JSON, nullable=False),
    Column("when_logged", TIMESTAMP, nullable=False, server_default=func.now()),
    mysql_charset="utf8mb4",
)


class BaseData:
    def __init__(self, cfg: CoreConfig, conn: Connection) -> None:
        self.config = cfg
        self.conn = conn
        self.logger = logging.getLogger("database")

    async def execute(self, sql: str, opts: Dict[str, Any] = {}) -> Optional[CursorResult]:
        res = None

        try:
            self.logger.debug(f"SQL Execute: {''.join(str(sql).splitlines())}")
            res = self.conn.execute(text(sql), opts)

        except SQLAlchemyError as e:
            self.logger.error(f"SQLAlchemy error {e}")
            return None

        except UnicodeEncodeError as e:
            self.logger.error(f"UnicodeEncodeError error {e}")
            return None

        except Exception:
            try:
                res = self.conn.execute(sql, opts)

            except SQLAlchemyError as e:
                self.logger.error(f"SQLAlchemy error {e}")
                return None

            except UnicodeEncodeError as e:
                self.logger.error(f"UnicodeEncodeError error {e}")
                return None

            except Exception:
                self.logger.error(f"Unknown error")
                raise

        return res

    def generate_id(self) -> int:
        """
        Generate a random 5-7 digit id
        """
        return randrange(10000, 9999999)

    async def log_event(
        self, system: str, type: str, severity: int, message: str, details: Dict = {}
    ) -> Optional[int]:
        sql = event_log.insert().values(
            system=system,
            type=type,
            severity=severity,
            message=message,
            details=json.dumps(details),
        )
        result = await self.execute(sql)

        if result is None:
            self.logger.error(
                f"{__name__}: Failed to insert event into event log! system = {system}, type = {type}, severity = {severity}, message = {message}"
            )
            return None

        return result.lastrowid

    async def get_event_log(self, entries: int = 100) -> Optional[List[Dict]]:
        sql = event_log.select().limit(entries).all()
        result = await self.execute(sql)

        if result is None:
            return None
        return result.fetchall()

    def fix_bools(self, data: Dict) -> Dict:
        for k, v in data.items():
            if k == "userName" or k == "teamName":
                continue
            if type(v) == str and v.lower() == "true":
                data[k] = True
            elif type(v) == str and v.lower() == "false":
                data[k] = False

        return data
