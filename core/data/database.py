import logging, coloredlogs
from typing import Any, Dict, List
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import importlib, os, json

from hashlib import sha256

from core.config import CoreConfig
from core.data.schema import *
from core.utils import Utils

class Data:
    def __init__(self, cfg: CoreConfig) -> None:
        self.config = cfg

        if self.config.database.sha2_password:
            passwd = sha256(self.config.database.password.encode()).digest()
            self.__url = f"{self.config.database.protocol}://{self.config.database.username}:{passwd.hex()}@{self.config.database.host}/{self.config.database.name}?charset=utf8mb4"
        else:
            self.__url = f"{self.config.database.protocol}://{self.config.database.username}:{self.config.database.password}@{self.config.database.host}/{self.config.database.name}?charset=utf8mb4"
        
        self.__engine = create_engine(self.__url, pool_recycle=3600)
        session = sessionmaker(bind=self.__engine, autoflush=True, autocommit=True)
        self.session = scoped_session(session)

        self.user = UserData(self.config, self.session)
        self.arcade = ArcadeData(self.config, self.session)
        self.card = CardData(self.config, self.session)
        self.base = BaseData(self.config, self.session)
        self.schema_ver_latest = 4

        log_fmt_str = "[%(asctime)s] %(levelname)s | Database | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        self.logger = logging.getLogger("database")

        # Prevent the logger from adding handlers multiple times
        if not getattr(self.logger, 'handler_set', None):
            fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.config.server.log_dir, "db"), encoding="utf-8",
                when="d", backupCount=10)
            fileHandler.setFormatter(log_fmt)
            
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(log_fmt)

            self.logger.addHandler(fileHandler)
            self.logger.addHandler(consoleHandler)

            self.logger.setLevel(self.config.database.loglevel)
            coloredlogs.install(cfg.database.loglevel, logger=self.logger, fmt=log_fmt_str)
            self.logger.handler_set = True # type: ignore

    def create_database(self):
        self.logger.info("Creating databases...")
        try:
            metadata.create_all(self.__engine.connect())
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to create databases! {e}")
            return
        
        games = Utils.get_all_titles()
        for game_dir, game_mod in games.items():
            try:
                title_db = game_mod.database(self.config)
                metadata.create_all(self.__engine.connect())

                self.base.set_schema_ver(game_mod.current_schema_version, game_mod.game_codes[0])

            except Exception as e:
                self.logger.warning(f"Could not load database schema from {game_dir} - {e}")
        
        self.logger.info(f"Setting base_schema_ver to {self.schema_ver_latest}")
        self.base.set_schema_ver(self.schema_ver_latest)

        self.logger.info(f"Setting user auto_incrememnt to {self.config.database.user_table_autoincrement_start}")
        self.user.reset_autoincrement(self.config.database.user_table_autoincrement_start)
    
    def recreate_database(self):
        self.logger.info("Dropping all databases...")
        self.base.execute("SET FOREIGN_KEY_CHECKS=0")
        try:
            metadata.drop_all(self.__engine.connect())
        except SQLAlchemyError as e:
            self.logger.error(f"Failed to drop databases! {e}")
            return
        
        for root, dirs, files in os.walk("./titles"):
            for dir in dirs: 
                if not dir.startswith("__"):
                    try:
                        mod = importlib.import_module(f"titles.{dir}")
                        
                        try:
                            title_db = mod.database(self.config)
                            metadata.drop_all(self.__engine.connect())

                        except Exception as e:
                            self.logger.warning(f"Could not load database schema from {dir} - {e}")

                    except ImportError as e:
                        self.logger.warning(f"Failed to load database schema dir {dir} - {e}")
            break
        
        self.base.execute("SET FOREIGN_KEY_CHECKS=1")

        self.create_database()
    
    def migrate_database(self, game: str, version: int, action: str) -> None:
        old_ver = self.base.get_schema_ver(game)
        sql = ""
        
        if old_ver is None:
            self.logger.error(f"Schema for game {game} does not exist, did you run the creation script?")
            return
        
        if old_ver == version:
            self.logger.info(f"Schema for game {game} is already version {old_ver}, nothing to do")
            return
        
        if not os.path.exists(f"core/data/schema/versions/{game.upper()}_{version}_{action}.sql"):            
            self.logger.error(f"Could not find {action} script {game.upper()}_{version}_{action}.sql in core/data/schema/versions folder")
            return

        with open(f"core/data/schema/versions/{game.upper()}_{version}_{action}.sql", "r", encoding="utf-8") as f:
            sql = f.read()
        
        result = self.base.execute(sql)
        if result is None:
            self.logger.error("Error execuing sql script!")
            return None
        
        result = self.base.set_schema_ver(version, game)
        if result is None:
            self.logger.error("Error setting version in schema_version table!")
            return None
        
        self.logger.info(f"Successfully migrated {game} to schema version {version}")
