import logging, coloredlogs
from typing import Optional
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from logging.handlers import TimedRotatingFileHandler
import importlib, os
import secrets, string
import bcrypt
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
        self.current_schema_version = 4

        log_fmt_str = "[%(asctime)s] %(levelname)s | Database | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        self.logger = logging.getLogger("database")

        # Prevent the logger from adding handlers multiple times
        if not getattr(self.logger, "handler_set", None):
            fileHandler = TimedRotatingFileHandler(
                "{0}/{1}.log".format(self.config.server.log_dir, "db"),
                encoding="utf-8",
                when="d",
                backupCount=10,
            )
            fileHandler.setFormatter(log_fmt)

            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(log_fmt)

            self.logger.addHandler(fileHandler)
            self.logger.addHandler(consoleHandler)

            self.logger.setLevel(self.config.database.loglevel)
            coloredlogs.install(
                cfg.database.loglevel, logger=self.logger, fmt=log_fmt_str
            )
            self.logger.handler_set = True  # type: ignore

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
                if hasattr(game_mod, "database") and hasattr(game_mod, "current_schema_version"):
                    game_mod.database(self.config)
                metadata.create_all(self.__engine.connect())

                self.base.set_schema_ver(
                    game_mod.current_schema_version, game_mod.game_codes[0]
                )

            except Exception as e:
                self.logger.warning(
                    f"Could not load database schema from {game_dir} - {e}"
                )

        self.logger.info(f"Setting base_schema_ver to {self.current_schema_version}")
        self.base.set_schema_ver(self.current_schema_version)

        self.logger.info(
            f"Setting user auto_incrememnt to {self.config.database.user_table_autoincrement_start}"
        )
        self.user.reset_autoincrement(
            self.config.database.user_table_autoincrement_start
        )

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
                            if hasattr(mod, "database"):
                                mod.database(self.config)
                            metadata.drop_all(self.__engine.connect())

                        except Exception as e:
                            self.logger.warning(
                                f"Could not load database schema from {dir} - {e}"
                            )

                    except ImportError as e:
                        self.logger.warning(
                            f"Failed to load database schema dir {dir} - {e}"
                        )
            break

        self.base.execute("SET FOREIGN_KEY_CHECKS=1")

        self.create_database()

    def migrate_database(self, game: str, version: Optional[int], action: str) -> None:
        old_ver = self.base.get_schema_ver(game)
        sql = ""
        if version is None:
            if not game == "CORE":
                titles = Utils.get_all_titles()
                
                for folder, mod in titles.items():
                    for game_ in mod.game_codes:
                        if not game_ == game: continue
                        
                        if hasattr(mod, "current_schema_version"):
                            version = mod.current_schema_version
                        
                        else:
                            self.logger.warn(f"current_schema_version not found for {folder}")
        
            else:
                version = self.current_schema_version
        
        if version is None:
            self.logger.warn(f"Could not determine latest version for {game}, please specify --version")

        if old_ver is None:
            self.logger.error(
                f"Schema for game {game} does not exist, did you run the creation script?"
            )
            return

        if old_ver == version:
            self.logger.info(
                f"Schema for game {game} is already version {old_ver}, nothing to do"
            )
            return

        if action == "upgrade":
            for x in range(old_ver, version):
                if not os.path.exists(
                    f"core/data/schema/versions/{game.upper()}_{x + 1}_{action}.sql"
                ):
                    self.logger.error(
                        f"Could not find {action} script {game.upper()}_{x + 1}_{action}.sql in core/data/schema/versions folder"
                    )
                    return

                with open(
                    f"core/data/schema/versions/{game.upper()}_{x + 1}_{action}.sql",
                    "r",
                    encoding="utf-8",
                ) as f:
                    sql = f.read()

                result = self.base.execute(sql)
                if result is None:
                    self.logger.error("Error execuing sql script!")
                    return None
        
        else:
            for x in range(old_ver, version, -1):
                if not os.path.exists(
                    f"core/data/schema/versions/{game.upper()}_{x - 1}_{action}.sql"
                ):
                    self.logger.error(
                        f"Could not find {action} script {game.upper()}_{x - 1}_{action}.sql in core/data/schema/versions folder"
                    )
                    return

                with open(
                    f"core/data/schema/versions/{game.upper()}_{x - 1}_{action}.sql",
                    "r",
                    encoding="utf-8",
                ) as f:
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

    def create_owner(self, email: Optional[str] = None) -> None:
        pw = "".join(
            secrets.choice(string.ascii_letters + string.digits) for i in range(20)
        )
        hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())

        user_id = self.user.create_user(email=email, permission=255, password=hash)
        if user_id is None:
            self.logger.error(f"Failed to create owner with email {email}")
            return

        card_id = self.card.create_card(user_id, "00000000000000000000")
        if card_id is None:
            self.logger.error(f"Failed to create card for owner with id {user_id}")
            return

        self.logger.warn(
            f"Successfully created owner with email {email}, access code 00000000000000000000, and password {pw} Make sure to change this password and assign a real card ASAP!"
        )

    def migrate_card(self, old_ac: str, new_ac: str, should_force: bool) -> None:
        if old_ac == new_ac:
            self.logger.error("Both access codes are the same!")
            return

        new_card = self.card.get_card_by_access_code(new_ac)
        if new_card is None:
            self.card.update_access_code(old_ac, new_ac)
            return

        if not should_force:
            self.logger.warn(
                f"Card already exists for access code {new_ac} (id {new_card['id']}). If you wish to continue, rerun with the '--force' flag."
                f" All exiting data on the target card {new_ac} will be perminently erased and replaced with data from card {old_ac}."
            )
            return

        self.logger.info(
            f"All exiting data on the target card {new_ac} will be perminently erased and replaced with data from card {old_ac}."
        )
        self.card.delete_card(new_card["id"])
        self.card.update_access_code(old_ac, new_ac)

        hanging_user = self.user.get_user(new_card["user"])
        if hanging_user["password"] is None:
            self.logger.info(f"Delete hanging user {hanging_user['id']}")
            self.user.delete_user(hanging_user["id"])

    def delete_hanging_users(self) -> None:
        """
        Finds and deletes users that have not registered for the webui that have no cards assocated with them.
        """
        unreg_users = self.user.get_unregistered_users()
        if unreg_users is None:
            self.logger.error("Error occoured finding unregistered users")

        for user in unreg_users:
            cards = self.card.get_user_cards(user["id"])
            if cards is None:
                self.logger.error(f"Error getting cards for user {user['id']}")
                continue

            if not cards:
                self.logger.info(f"Delete hanging user {user['id']}")
                self.user.delete_user(user["id"])

    def autoupgrade(self) -> None:
        all_games = self.base.get_all_schema_vers()
        if all_games is None:
            self.logger.warn("Failed to get schema versions")
        
        for x in all_games:
            game = x["game"].upper()
            update_ver = 1
            for y in range(2, 100):
                if os.path.exists(f"core/data/schema/versions/{game}_{y}_upgrade.sql"):
                    update_ver = y
                else:
                    break
        
            self.migrate_database(game, update_ver, "upgrade")