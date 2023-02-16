import json
import logging
from random import randrange
from typing import Any, Optional, Dict, List
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
    mysql_charset='utf8mb4'
)

event_log = Table(
    "event_log",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("system", String(255), nullable=False),
    Column("type", String(255), nullable=False),
    Column("severity", Integer, nullable=False),
    Column("details", JSON, nullable=False),
    Column("when_logged", TIMESTAMP, nullable=False, server_default=func.now()),
    mysql_charset='utf8mb4'
)

class BaseData():
    def __init__(self, cfg: CoreConfig, conn: Connection) -> None:
        self.config = cfg
        self.conn = conn
        self.logger = logging.getLogger("database")
    
    def execute(self, sql: str, opts: Dict[str, Any]={}) -> Optional[CursorResult]:
        res = None

        try:
            self.logger.info(f"SQL Execute: {''.join(str(sql).splitlines())} || {opts}")
            res = self.conn.execute(text(sql), opts)

        except SQLAlchemyError as e:
            self.logger.error(f"SQLAlchemy error {e}")
            return None
        
        except UnicodeEncodeError as e:
            self.logger.error(f"UnicodeEncodeError error {e}")
            return None

        except:
            try:
                res = self.conn.execute(sql, opts)

            except SQLAlchemyError as e:
                self.logger.error(f"SQLAlchemy error {e}")
                return None
            
            except UnicodeEncodeError as e:
                self.logger.error(f"UnicodeEncodeError error {e}")
                return None

            except:
                self.logger.error(f"Unknown error")
                raise

        return res
    
    def generate_id(self) -> int:
        """
        Generate a random 5-7 digit id
        """
        return randrange(10000, 9999999)
    
    def get_schema_ver(self, game: str) -> Optional[int]:
        sql = select(schema_ver).where(schema_ver.c.game == game)

        result = self.execute(sql)
        if result is None:
            return None
        return result.fetchone()["version"]
    
    def set_schema_ver(self, ver: int, game: str = "CORE") -> Optional[int]:
        sql = insert(schema_ver).values(game = game, version = ver)
        conflict = sql.on_duplicate_key_update(version = ver)
        
        result = self.execute(conflict)
        if result is None:
            self.logger.error(f"Failed to update schema version for game {game} (v{ver})")
            return None
        return result.lastrowid

    def log_event(self, system: str, type: str, severity: int, details: Dict) -> Optional[int]:
        sql = event_log.insert().values(system = system, type = type, severity = severity, details = json.dumps(details))
        result = self.execute(sql)

        if result is None:
            self.logger.error(f"{__name__}: Failed to insert event into event log! system = {system}, type = {type}, severity = {severity}, details = {details}")
            return None

        return result.lastrowid
    
    def get_event_log(self, entries: int = 100) -> Optional[List[Dict]]:
        sql = event_log.select().limit(entries).all()
        result = self.execute(sql)

        if result is None: return None
        return result.fetchall()
    
    def fix_bools(self, data: Dict) -> Dict:
        for k,v in data.items():
            if type(v) == str and v.lower() == "true":
                data[k] = True
            elif type(v) == str and v.lower() == "false":
                data[k] = False
        
        return data
