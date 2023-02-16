import logging, coloredlogs
from typing import Any, Dict, List
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from logging.handlers import TimedRotatingFileHandler

from hashlib import sha256

from core.config import CoreConfig
from core.data.schema import *

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
        self.schema_ver_latest = 1

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

    