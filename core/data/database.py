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
        self.schema_ver_latest = 2

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

    def dump_db(self):        
        dbname = self.config.database.name

        self.logger.info("Database dumper for use with the reworked schema")
        self.logger.info("Dumping users...")

        sql = f"SELECT * FROM `{dbname}`.`user`"

        result = self.base.execute(sql)
        if result is None:
            self.logger.error("Failed")
            return None
        users = result.fetchall()

        user_list: List[Dict[str, Any]] = []
        for usr in users:
            user_list.append({
                "id": usr["id"],
                "username": usr["username"],
                "email": usr["email"],
                "password": usr["password"],
                "permissions": usr["permissions"],
                "created_date": datetime.strftime(usr["created_date"], "%Y-%m-%d %H:%M:%S"),
                "last_login_date": datetime.strftime(usr["accessed_date"], "%Y-%m-%d %H:%M:%S"),
            })

        self.logger.info(f"Done, found {len(user_list)} users")
        with open("dbdump-user.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(user_list))
            self.logger.info(f"Saved as dbdump-user.json")
        
        self.logger.info("Dumping cards...")

        sql = f"SELECT * FROM `{dbname}`.`card`"

        result = self.base.execute(sql)
        if result is None:
            self.logger.error("Failed")
            return None
        cards = result.fetchall()

        card_list: List[Dict[str, Any]] = []
        for crd in cards:
            card_list.append({
                "id": crd["id"],
                "user": crd["user"],
                "access_code": crd["access_code"],
                "is_locked": crd["is_locked"],
                "is_banned": crd["is_banned"],
                "created_date": datetime.strftime(crd["created_date"], "%Y-%m-%d %H:%M:%S"),
                "last_login_date": datetime.strftime(crd["accessed_date"], "%Y-%m-%d %H:%M:%S"),
            })
        
        self.logger.info(f"Done, found {len(card_list)} cards")
        with open("dbdump-card.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(card_list))
            self.logger.info(f"Saved as dbdump-card.json")

        self.logger.info("Dumping arcades...")

        sql = f"SELECT * FROM `{dbname}`.`arcade`"

        result = self.base.execute(sql)
        if result is None:
            self.logger.error("Failed")
            return None
        arcades = result.fetchall()

        arcade_list: List[Dict[str, Any]] = []
        for arc in arcades:            
            arcade_list.append({
                "id": arc["id"],
                "name": arc["name"],
                "nickname": arc["name"],
                "country": None,
                "country_id": None,
                "state": None,
                "city": None,
                "region_id": None,
                "timezone": None,
            })
        
        self.logger.info(f"Done, found {len(arcade_list)} arcades")
        with open("dbdump-arcade.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(arcade_list))
            self.logger.info(f"Saved as dbdump-arcade.json")

        self.logger.info("Dumping machines...")

        sql = f"SELECT * FROM `{dbname}`.`machine`"

        result = self.base.execute(sql)
        if result is None:
            self.logger.error("Failed")
            return None
        machines = result.fetchall()

        machine_list: List[Dict[str, Any]] = []
        for mech in machines:            
            if "country" in mech["data"]:
                country = mech["data"]["country"]
            else:
                country = None

            if "ota_enable" in mech["data"]:
                ota_enable = mech["data"]["ota_enable"]
            else:
                ota_enable = None

            machine_list.append({
                "id": mech["id"],
                "arcade": mech["arcade"],
                "serial": mech["keychip"],
                "game": mech["game"],
                "board": None,
                "country": country,
                "timezone": None,
                "ota_enable": ota_enable,
                "is_cab": False,
            })
        
        self.logger.info(f"Done, found {len(machine_list)} machines")
        with open("dbdump-machine.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(machine_list))
            self.logger.info(f"Saved as dbdump-machine.json")

        self.logger.info("Dumping arcade owners...")

        sql = f"SELECT * FROM `{dbname}`.`arcade_owner`"

        result = self.base.execute(sql)
        if result is None:
            self.logger.error("Failed")
            return None
        arcade_owners = result.fetchall()

        owner_list: List[Dict[str, Any]] = []
        for owner in owner_list:
            owner_list.append(owner._asdict())
        
        self.logger.info(f"Done, found {len(owner_list)} arcade owners")
        with open("dbdump-arcade_owner.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(owner_list))
            self.logger.info(f"Saved as dbdump-arcade_owner.json")
        
        self.logger.info("Dumping profiles...")

        sql = f"SELECT * FROM `{dbname}`.`profile`"

        result = self.base.execute(sql)
        if result is None:
            self.logger.error("Failed")
            return None
        profiles = result.fetchall()

        profile_list: Dict[List[Dict[str, Any]]] = {}
        for pf in profiles:
            game = pf["game"]

            if game not in profile_list:
                profile_list[game] = []

            profile_list[game].append({
                "id": pf["id"],
                "user": pf["user"],
                "version": pf["version"],
                "use_count": pf["use_count"],
                "name": pf["name"],
                "game_id": pf["game_id"],
                "mods": pf["mods"],
                "data": pf["data"],
            })
        
        self.logger.info(f"Done, found profiles for {len(profile_list)} games")
        with open("dbdump-profile.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(profile_list))
            self.logger.info(f"Saved as dbdump-profile.json")

        self.logger.info("Dumping scores...")

        sql = f"SELECT * FROM `{dbname}`.`score`"

        result = self.base.execute(sql)
        if result is None:
            self.logger.error("Failed")
            return None
        scores = result.fetchall()

        score_list: Dict[List[Dict[str, Any]]] = {}
        for sc in scores:
            game = sc["game"]

            if game not in score_list:
                score_list[game] = []
                
            score_list[game].append({
                "id": sc["id"],
                "user": sc["user"],
                "version": sc["version"],
                "song_id": sc["song_id"],
                "chart_id": sc["chart_id"],
                "score1": sc["score1"],
                "score2": sc["score2"],
                "fc1": sc["fc1"],
                "fc2": sc["fc2"],
                "cleared": sc["cleared"],
                "grade": sc["grade"],
                "data": sc["data"],
            })
        
        self.logger.info(f"Done, found scores for {len(score_list)} games")
        with open("dbdump-score.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(score_list))
            self.logger.info(f"Saved as dbdump-score.json")

        self.logger.info("Dumping achievements...")

        sql = f"SELECT * FROM `{dbname}`.`achievement`"

        result = self.base.execute(sql)
        if result is None:
            self.logger.error("Failed")
            return None
        achievements = result.fetchall()

        achievement_list: Dict[List[Dict[str, Any]]] = {}
        for ach in achievements:
            game = ach["game"]

            if game not in achievement_list:
                achievement_list[game] = []
                
            achievement_list[game].append({
                "id": ach["id"],
                "user": ach["user"],
                "version": ach["version"],
                "type": ach["type"],
                "achievement_id": ach["achievement_id"],
                "data": ach["data"],
            })
        
        self.logger.info(f"Done, found achievements for {len(achievement_list)} games")
        with open("dbdump-achievement.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(achievement_list))
            self.logger.info(f"Saved as dbdump-achievement.json")

        self.logger.info("Dumping items...")

        sql = f"SELECT * FROM `{dbname}`.`item`"

        result = self.base.execute(sql)
        if result is None:
            self.logger.error("Failed")
            return None
        items = result.fetchall()

        item_list: Dict[List[Dict[str, Any]]] = {}
        for itm in items:
            game = itm["game"]

            if game not in item_list:
                item_list[game] = []
                
            item_list[game].append({
                "id": itm["id"],
                "user": itm["user"],
                "version": itm["version"],
                "type": itm["type"],
                "item_id": itm["item_id"],
                "data": ach["data"],
            })
        
        self.logger.info(f"Done, found items for {len(item_list)} games")
        with open("dbdump-item.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(item_list))
            self.logger.info(f"Saved as dbdump-item.json")

    def restore_from_old_schema(self):
        # Import the tables we expect to be there
        from core.data.schema.user import aime_user
        from core.data.schema.card import aime_card
        from core.data.schema.arcade import arcade, machine, arcade_owner
        from sqlalchemy.dialects.mysql import Insert

        # Make sure that all the tables we're trying to access exist
        self.create_database()

        # Import the data, making sure that dependencies are accounted for
        if os.path.exists("dbdump-user.json"):
            users = []
            with open("dbdump-user.json", "r", encoding="utf-8") as f:
                users = json.load(f)
            
            self.logger.info(f"Load {len(users)} users")
            
            for user in users:
                sql = Insert(aime_user).values(**user)

                conflict = sql.on_duplicate_key_update(**user)

                result = self.base.execute(conflict)
                if result is None:
                    self.logger.error(f"Failed to insert user {user['id']}")
                    continue
                self.logger.info(f"Inserted user {user['id']} -> {result.lastrowid}")

        if os.path.exists("dbdump-card.json"):
            cards = []
            with open("dbdump-card.json", "r", encoding="utf-8") as f:
                cards = json.load(f)
            
            self.logger.info(f"Load {len(cards)} cards")

            for card in cards:
                sql = Insert(aime_card).values(**card)

                conflict = sql.on_duplicate_key_update(**card)

                result = self.base.execute(conflict)
                if result is None:
                    self.logger.error(f"Failed to insert card {card['id']}")
                    continue
                self.logger.info(f"Inserted card {card['id']} -> {result.lastrowid}")

        if os.path.exists("dbdump-arcade.json"):
            arcades = []
            with open("dbdump-arcade.json", "r", encoding="utf-8") as f:
                arcades = json.load(f)
            
            self.logger.info(f"Load {len(arcades)} arcades")

            for ac in arcades:
                sql = Insert(arcade).values(**ac)

                conflict = sql.on_duplicate_key_update(**ac)
            
                result = self.base.execute(conflict)
                if result is None:
                    self.logger.error(f"Failed to insert arcade {ac['id']}")
                    continue
                self.logger.info(f"Inserted arcade {ac['id']} -> {result.lastrowid}")
        
        if os.path.exists("dbdump-arcade_owner.json"):
            ac_owners = []
            with open("dbdump-arcade_owner.json", "r", encoding="utf-8") as f:
                ac_owners = json.load(f)
            
            self.logger.info(f"Load {len(ac_owners)} arcade owners")

            for owner in ac_owners:
                sql = Insert(arcade_owner).values(**owner)

                conflict = sql.on_duplicate_key_update(**owner)

                result = self.base.execute(conflict)
                if result is None:
                    self.logger.error(f"Failed to insert arcade_owner {owner['user']}")
                    continue
                self.logger.info(f"Inserted arcade_owner {owner['user']} -> {result.lastrowid}")

        if os.path.exists("dbdump-machine.json"):
            mechs = []
            with open("dbdump-machine.json", "r", encoding="utf-8") as f:
                mechs = json.load(f)
            
            self.logger.info(f"Load {len(mechs)} machines")

            for mech in mechs:
                sql = Insert(machine).values(**mech)

                conflict = sql.on_duplicate_key_update(**mech)

                result = self.base.execute(conflict)
                if result is None:
                    self.logger.error(f"Failed to insert machine {mech['id']}")
                    continue
                self.logger.info(f"Inserted machine {mech['id']} -> {result.lastrowid}")
        
        # Now the fun part, grabbing all our scores, profiles, items, and achievements and trying
        # to conform them to our current, freeform schema. This will be painful...
        profiles = {}
        items = {}
        scores = {}
        achievements = {}

        if os.path.exists("dbdump-profile.json"):
            with open("dbdump-profile.json", "r", encoding="utf-8") as f:
                profiles = json.load(f)
            
            self.logger.info(f"Load {len(profiles)} profiles")

        if os.path.exists("dbdump-item.json"):
            with open("dbdump-item.json", "r", encoding="utf-8") as f:
                items = json.load(f)
            
            self.logger.info(f"Load {len(items)} items")

        if os.path.exists("dbdump-score.json"):
            with open("dbdump-score.json", "r", encoding="utf-8") as f:
                scores = json.load(f)
            
            self.logger.info(f"Load {len(scores)} scores")

        if os.path.exists("dbdump-achievement.json"):
            with open("dbdump-achievement.json", "r", encoding="utf-8") as f:
                achievements = json.load(f)
            
            self.logger.info(f"Load {len(achievements)} achievements")

        # Chuni / Chusan
        if os.path.exists("titles/chuni/schema"):
            from titles.chuni.schema.item import character, item, duel, map, map_area
            from titles.chuni.schema.profile import profile, profile_ex, option, option_ex
            from titles.chuni.schema.profile import recent_rating, activity, charge, emoney
            from titles.chuni.schema.profile import overpower
            from titles.chuni.schema.score import best_score, course

            chuni_profiles = []
            chuni_items = []
            chuni_scores = []
            
            if "SDBT" in profiles:
                chuni_profiles = profiles["SDBT"]
            if "SDBT" in items:
                chuni_items = items["SDBT"]
            if "SDBT" in scores:
                chuni_scores = scores["SDBT"]
            if "SDHD" in profiles:
                chuni_profiles += profiles["SDHD"]
            if "SDHD" in items:
                chuni_items += items["SDHD"]
            if "SDHD" in scores:
                chuni_scores += scores["SDHD"]

            self.logger.info(f"Importing {len(chuni_profiles)} chunithm/chunithm new profiles")
            
            for pf in chuni_profiles:
                if type(pf["data"]) is not dict:
                    pf["data"] = json.loads(pf["data"])
                pf_data = pf["data"]

                # data
                if "userData" in pf_data:
                    pf_data["userData"]["userName"] = bytes([ord(c) for c in pf_data["userData"]["userName"]]).decode("utf-8")
                    pf_data["userData"]["user"] = pf["user"]
                    pf_data["userData"]["version"] = pf["version"]
                    pf_data["userData"].pop("accessCode")

                    if pf_data["userData"]["lastRomVersion"].startswith("2."):
                        pf_data["userData"]["version"] += 10

                    pf_data["userData"] = self.base.fix_bools(pf_data["userData"])

                    sql = Insert(profile).values(**pf_data["userData"])
                    conflict = sql.on_duplicate_key_update(**pf_data["userData"])

                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert chuni profile data for {pf['user']}")
                        continue
                    self.logger.info(f"Inserted chuni profile for {pf['user']} ->{result.lastrowid}")

                # data_ex
                if "userDataEx" in pf_data and len(pf_data["userDataEx"]) > 0:
                    pf_data["userDataEx"][0]["user"] = pf["user"]
                    pf_data["userDataEx"][0]["version"] = pf["version"]

                    pf_data["userDataEx"] = self.base.fix_bools(pf_data["userDataEx"][0])

                    sql = Insert(profile_ex).values(**pf_data["userDataEx"])
                    conflict = sql.on_duplicate_key_update(**pf_data["userDataEx"])

                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert chuni profile data_ex for {pf['user']}")
                        continue
                    self.logger.info(f"Inserted chuni profile data_ex for {pf['user']} ->{result.lastrowid}")

                # option
                if "userGameOption" in pf_data:
                    pf_data["userGameOption"]["user"] = pf["user"]

                    pf_data["userGameOption"] = self.base.fix_bools(pf_data["userGameOption"])

                    sql = Insert(option).values(**pf_data["userGameOption"])
                    conflict = sql.on_duplicate_key_update(**pf_data["userGameOption"])

                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert chuni profile options for {pf['user']}")
                        continue
                    self.logger.info(f"Inserted chuni profile options for {pf['user']} ->{result.lastrowid}")

                # option_ex
                if "userGameOptionEx" in pf_data and len(pf_data["userGameOptionEx"]) > 0:
                    pf_data["userGameOptionEx"][0]["user"] = pf["user"]

                    pf_data["userGameOptionEx"] = self.base.fix_bools(pf_data["userGameOptionEx"][0])

                    sql = Insert(option_ex).values(**pf_data["userGameOptionEx"])
                    conflict = sql.on_duplicate_key_update(**pf_data["userGameOptionEx"])

                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert chuni profile option_ex for {pf['user']}")
                        continue
                    self.logger.info(f"Inserted chuni profile option_ex for {pf['user']} ->{result.lastrowid}")

                # recent_rating
                if "userRecentRatingList" in pf_data:
                    rr = {
                        "user": pf["user"],
                        "recentRating": pf_data["userRecentRatingList"]
                    }

                    sql = Insert(recent_rating).values(**rr)
                    conflict = sql.on_duplicate_key_update(**rr)

                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert chuni profile recent_rating for {pf['user']}")
                        continue
                    self.logger.info(f"Inserted chuni profile recent_rating for {pf['user']} ->{result.lastrowid}")

                # activity
                if "userActivityList" in pf_data:
                    for act in pf_data["userActivityList"]:
                        act["user"] = pf["user"]

                        sql = Insert(activity).values(**act)
                        conflict = sql.on_duplicate_key_update(**act)

                        result = self.base.execute(conflict)
                        if result is None:
                            self.logger.error(f"Failed to insert chuni profile activity for {pf['user']}")
                        else:
                            self.logger.info(f"Inserted chuni profile activity for {pf['user']} ->{result.lastrowid}")

                # charge
                if "userChargeList" in pf_data:
                    for cg in pf_data["userChargeList"]:
                        cg["user"] = pf["user"]

                        cg = self.base.fix_bools(cg)
                        
                        sql = Insert(charge).values(**cg)
                        conflict = sql.on_duplicate_key_update(**cg)

                        result = self.base.execute(conflict)
                        if result is None:
                            self.logger.error(f"Failed to insert chuni profile charge for {pf['user']}")
                        else:
                            self.logger.info(f"Inserted chuni profile charge for {pf['user']} ->{result.lastrowid}")
                
                # emoney
                if "userEmoneyList" in pf_data:
                    for emon in pf_data["userEmoneyList"]:
                        emon["user"] = pf["user"]

                        sql = Insert(emoney).values(**emon)
                        conflict = sql.on_duplicate_key_update(**emon)

                        result = self.base.execute(conflict)
                        if result is None:
                            self.logger.error(f"Failed to insert chuni profile emoney for {pf['user']}")
                        else:
                            self.logger.info(f"Inserted chuni profile emoney for {pf['user']} ->{result.lastrowid}")
                
                # overpower
                if "userOverPowerList" in pf_data:
                    for op in pf_data["userOverPowerList"]:
                        op["user"] = pf["user"]

                        sql = Insert(overpower).values(**op)
                        conflict = sql.on_duplicate_key_update(**op)

                        result = self.base.execute(conflict)
                        if result is None:
                            self.logger.error(f"Failed to insert chuni profile overpower for {pf['user']}")
                        else:
                            self.logger.info(f"Inserted chuni profile overpower for {pf['user']} ->{result.lastrowid}")
                
                # map_area
                if "userMapAreaList" in pf_data:
                    for ma in pf_data["userMapAreaList"]:
                        ma["user"] = pf["user"]

                        ma = self.base.fix_bools(ma)

                        sql = Insert(map_area).values(**ma)
                        conflict = sql.on_duplicate_key_update(**ma)

                        result = self.base.execute(conflict)
                        if result is None:
                            self.logger.error(f"Failed to insert chuni map_area for {pf['user']}")
                        else:
                            self.logger.info(f"Inserted chuni map_area for {pf['user']} ->{result.lastrowid}")

                #duel
                if "userDuelList" in pf_data:
                    for ma in pf_data["userDuelList"]:
                        ma["user"] = pf["user"]

                        ma = self.base.fix_bools(ma)

                        sql = Insert(duel).values(**ma)
                        conflict = sql.on_duplicate_key_update(**ma)

                        result = self.base.execute(conflict)
                        if result is None:
                            self.logger.error(f"Failed to insert chuni duel for {pf['user']}")
                        else:
                            self.logger.info(f"Inserted chuni duel for {pf['user']} ->{result.lastrowid}")
                
                # map
                if "userMapList" in pf_data:
                    for ma in pf_data["userMapList"]:
                        ma["user"] = pf["user"]

                        ma = self.base.fix_bools(ma)

                        sql = Insert(map).values(**ma)
                        conflict = sql.on_duplicate_key_update(**ma)

                        result = self.base.execute(conflict)
                        if result is None:
                            self.logger.error(f"Failed to insert chuni map for {pf['user']}")
                        else:
                            self.logger.info(f"Inserted chuni map for {pf['user']} ->{result.lastrowid}")
            
            self.logger.info(f"Importing {len(chuni_items)} chunithm/chunithm new items")

            for i in chuni_items:
                if type(i["data"]) is not dict:
                    i["data"] = json.loads(i["data"])
                i_data = i["data"]

                i_data["user"] = i["user"]
                
                i_data = self.base.fix_bools(i_data)

                try: i_data.pop("assignIllust")
                except: pass

                try: i_data.pop("exMaxLv")
                except: pass

                if i["type"] == 20: #character
                    sql = Insert(character).values(**i_data)
                else:
                    sql = Insert(item).values(**i_data)
                
                conflict = sql.on_duplicate_key_update(**i_data)

                result = self.base.execute(conflict)
                if result is None:
                    self.logger.error(f"Failed to insert chuni item for user {i['user']}")

                else:
                    self.logger.info(f"Inserted chuni item for user {i['user']} {i['item_id']} -> {result.lastrowid}")

            self.logger.info(f"Importing {len(chuni_scores)} chunithm/chunithm new scores")

            for sc in chuni_scores:
                if type(sc["data"]) is not dict:
                    sc["data"] = json.loads(sc["data"])

                score_data = self.base.fix_bools(sc["data"])

                try: score_data.pop("theoryCount")
                except: pass

                try: score_data.pop("ext1")
                except: pass

                score_data["user"] = sc["user"]

                sql = Insert(best_score).values(**score_data)
                conflict = sql.on_duplicate_key_update(**score_data)

                result = self.base.execute(conflict)
                if result is None:
                    self.logger.error(f"Failed to put chuni score for user {sc['user']}")
                else:
                    self.logger.info(f"Inserted chuni score for user {sc['user']} {sc['song_id']}/{sc['chart_id']} -> {result.lastrowid}")
        
        else:
            self.logger.info(f"Chuni/Chusan not found, skipping...")

        # CXB
        if os.path.exists("titles/cxb/schema"):
            from titles.cxb.schema.item import energy
            from titles.cxb.schema.profile import profile
            from titles.cxb.schema.score import score, ranking

            cxb_profiles = []
            cxb_items = []
            cxb_scores = []

            if "SDCA" in profiles:
                cxb_profiles = profiles["SDCA"]
            if "SDCA" in items:
                cxb_items = items["SDCA"]
            if "SDCA" in scores:
                cxb_scores = scores["SDCA"]

            self.logger.info(f"Importing {len(cxb_profiles)} CXB profiles")
            
            for pf in cxb_profiles:
                user = pf["user"]
                version = pf["version"]
                pf_data = pf["data"]["data"]
                pf_idx = pf["data"]["index"]

                for x in range(len(pf_data)):
                    sql = Insert(profile).values(
                        user = user,
                        version = version,
                        index = int(pf_idx[x]),
                        data = json.loads(pf_data[x]) if type(pf_data[x]) is not dict else pf_data[x]
                    )

                    conflict = sql.on_duplicate_key_update(
                        user = user,
                        version = version,
                        index = int(pf_idx[x]),
                        data = json.loads(pf_data[x]) if type(pf_data[x]) is not dict else pf_data[x]
                    )
                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert CXB profile for user {user} Index {pf_idx[x]}")

            self.logger.info(f"Importing {len(cxb_scores)} CXB scores")

            for sc in cxb_scores:
                user = sc["user"]
                version = sc["version"]
                mcode = sc["data"]["mcode"]
                index = sc["data"]["index"]

                sql = Insert(score).values(
                    user = user,
                    game_version = version,
                    song_mcode = mcode,
                    song_index = index,
                    data = sc["data"]
                )

                conflict = sql.on_duplicate_key_update(
                    user = user,
                    game_version = version,
                    song_mcode = mcode,
                    song_index = index,
                    data = sc["data"]
                )

                result = self.base.execute(conflict)
                if result is None:
                    self.logger.error(f"Failed to insert CXB score for user {user} mcode {mcode}")

            self.logger.info(f"Importing {len(cxb_items)} CXB items")

            for it in cxb_items:
                user = it["user"]

                if it["type"] == 3: # energy
                    sql = Insert(energy).values(
                        user = user,
                        energy = it["data"]["total"]
                    )

                    conflict = sql.on_duplicate_key_update(
                        user = user,
                        energy = it["data"]["total"]
                    )

                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert CXB energy for user {user}")

                elif it["type"] == 2:
                    sql = Insert(ranking).values(
                        user = user,
                        rev_id = it["data"]["rid"],
                        song_id = it["data"]["sc"][1] if len(it["data"]["sc"]) > 1 else None,
                        score = it["data"]["sc"][0],
                        clear = it["data"]["clear"],
                    )

                    conflict = sql.on_duplicate_key_update(
                        user = user,
                        rev_id = it["data"]["rid"],
                        song_id = it["data"]["sc"][1] if len(it["data"]["sc"]) > 1 else None,
                        score = it["data"]["sc"][0],
                        clear = it["data"]["clear"],
                    )

                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert CXB ranking for user {user}")
                
                else:
                    self.logger.error(f"Unknown CXB item type {it['type']} for user {user}")
        
        else:
            self.logger.info(f"CXB not found, skipping...")

        # Diva
        if os.path.exists("titles/diva/schema"):
            from titles.diva.schema.profile import profile
            from titles.diva.schema.score import score
            from titles.diva.schema.item import shop

            diva_profiles = []
            diva_scores = []

            if "SBZV" in profiles:
                diva_profiles = profiles["SBZV"]
            if "SBZV" in scores:
                diva_scores = scores["SBZV"]

            self.logger.info(f"Importing {len(diva_profiles)} Diva profiles")

            for pf in diva_profiles:
                pf["data"]["user"] = pf["user"]
                pf["data"]["version"] = pf["version"]
                pf_data = pf["data"]
                
                if "mdl_eqp_ary" in pf["data"]:
                    sql = Insert(shop).values(
                        user = user,
                        version = version,
                        mdl_eqp_ary = pf["data"]["mdl_eqp_ary"],
                    )
                    conflict = sql.on_duplicate_key_update(
                        user = user,
                        version = version,
                        mdl_eqp_ary = pf["data"]["mdl_eqp_ary"]
                    )
                    self.base.execute(conflict)
                    pf["data"].pop("mdl_eqp_ary")

                sql = Insert(profile).values(**pf_data)
                conflict = sql.on_duplicate_key_update(**pf_data)
                result = self.base.execute(conflict)
                if result is None:
                    self.logger.error(f"Failed to insert diva profile for {pf['user']}")
            
            self.logger.info(f"Importing {len(diva_scores)} Diva scores")
            
            for sc in diva_scores:
                user = sc["user"]

                clr_kind = -1
                for x in sc["data"]["stg_clr_kind"].split(","):
                    if x != "-1":
                        clr_kind = x

                cool_ct = 0
                for x in sc["data"]["stg_cool_cnt"].split(","):
                    if x != "0":
                        cool_ct = x

                fine_ct = 0
                for x in sc["data"]["stg_fine_cnt"].split(","):
                    if x != "0":
                        fine_ct = x

                safe_ct = 0
                for x in sc["data"]["stg_safe_cnt"].split(","):
                    if x != "0":
                        safe_ct = x

                sad_ct = 0
                for x in sc["data"]["stg_sad_cnt"].split(","):
                    if x != "0":
                        sad_ct = x

                worst_ct = 0
                for x in sc["data"]["stg_wt_wg_cnt"].split(","):
                    if x != "0":
                        worst_ct = x

                max_cmb = 0
                for x in sc["data"]["stg_max_cmb"].split(","):
                    if x != "0":
                        max_cmb = x

                sql = Insert(score).values(
                    user = user,
                    version = sc["version"],
                    pv_id = sc["song_id"],
                    difficulty = sc["chart_id"],
                    score = sc["score1"],
                    atn_pnt = sc["score2"],
                    clr_kind = clr_kind,
                    sort_kind = sc["data"]["sort_kind"],
                    cool = cool_ct,
                    fine = fine_ct,
                    safe = safe_ct,
                    sad = sad_ct,
                    worst = worst_ct,
                    max_combo = max_cmb,
                )

                conflict = sql.on_duplicate_key_update(user = user,
                    version = sc["version"],
                    pv_id = sc["song_id"],
                    difficulty = sc["chart_id"],
                    score = sc["score1"],
                    atn_pnt = sc["score2"],
                    clr_kind = clr_kind,
                    sort_kind = sc["data"]["sort_kind"],
                    cool = cool_ct,
                    fine = fine_ct,
                    safe = safe_ct,
                    sad = sad_ct,
                    worst = worst_ct,
                    max_combo = max_cmb
                )

                result = self.base.execute(conflict)
                if result is None:
                    self.logger.error(f"Failed to insert diva score for {pf['user']}")
        
        else:
            self.logger.info(f"Diva not found, skipping...")

        # Ongeki
        if os.path.exists("titles/ongeki/schema"):
            from titles.ongeki.schema.item import card, deck, character, boss, story
            from titles.ongeki.schema.item import chapter, item, music_item, login_bonus
            from titles.ongeki.schema.item import event_point, mission_point, scenerio
            from titles.ongeki.schema.item import trade_item, event_music, tech_event
            from titles.ongeki.schema.profile import profile, option, activity, recent_rating
            from titles.ongeki.schema.profile import rating_log, training_room, kop
            from titles.ongeki.schema.score import score_best, tech_count, playlog
            from titles.ongeki.schema.log import session_log

            item_types = {
                "character": 20,
                "story": 21,
                "card": 22,
                "deck": 23,
                "login": 24,
                "chapter": 25
            }

            ongeki_profiles = []
            ongeki_items = []
            ongeki_scores = []

            if "SDDT" in profiles:
                ongeki_profiles = profiles["SDDT"]
            if "SDDT" in items:
                ongeki_items = items["SDDT"]
            if "SDDT" in scores:
                ongeki_scores = scores["SDDT"]
            
            self.logger.info(f"Importing {len(ongeki_profiles)} ongeki profiles")
            
            for pf in ongeki_profiles:
                user = pf["user"]
                version = pf["version"]
                pf_data = pf["data"]

                pf_data["userData"]["user"] = user
                pf_data["userData"]["version"] = version
                pf_data["userData"].pop("accessCode")

                sql = Insert(profile).values(**pf_data["userData"])
                conflict = sql.on_duplicate_key_update(**pf_data["userData"])                
                result = self.base.execute(conflict)
                if result is None:
                    self.logger.error(f"Failed to insert ongeki profile data for user {pf['user']}")
                    continue

                pf_data["userOption"]["user"] = user

                sql = Insert(option).values(**pf_data["userOption"])
                conflict = sql.on_duplicate_key_update(**pf_data["userOption"])                
                result = self.base.execute(conflict)
                if result is None:
                    self.logger.error(f"Failed to insert ongeki profile options for user {pf['user']}")
                    continue

                for pf_list in pf_data["userActivityList"]:
                    pf_list["user"] = user

                    sql = Insert(activity).values(**pf_list)
                    conflict = sql.on_duplicate_key_update(**pf_list)                
                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert ongeki profile activity for user {pf['user']}")
                        continue

                sql = Insert(recent_rating).values(
                    user = user,
                    recentRating = pf_data["userRecentRatingList"]
                )

                conflict = sql.on_duplicate_key_update(
                    user = user,
                    recentRating = pf_data["userRecentRatingList"]
                )                
                result = self.base.execute(conflict)

                if result is None:
                    self.logger.error(f"Failed to insert ongeki profile recent rating for user {pf['user']}")
                    continue

                for pf_list in pf_data["userRatinglogList"]:
                    pf_list["user"] = user

                    sql = Insert(rating_log).values(**pf_list)

                    conflict = sql.on_duplicate_key_update(**pf_list)                
                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert ongeki profile rating log for user {pf['user']}")
                        continue

                for pf_list in pf_data["userTrainingRoomList"]:
                    pf_list["user"] = user

                    sql = Insert(training_room).values(**pf_list)
                    conflict = sql.on_duplicate_key_update(**pf_list)                
                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert ongeki profile training room for user {pf['user']}")
                        continue
                
                if "userKopList" in pf_data:
                    for pf_list in pf_data["userKopList"]:
                        pf_list["user"] = user

                        sql = Insert(kop).values(**pf_list)
                        conflict = sql.on_duplicate_key_update(**pf_list)                
                        result = self.base.execute(conflict)
                        if result is None:
                            self.logger.error(f"Failed to insert ongeki profile training room for user {pf['user']}")
                            continue

                for pf_list in pf_data["userBossList"]:
                    pf_list["user"] = user

                    sql = Insert(boss).values(**pf_list)
                    conflict = sql.on_duplicate_key_update(**pf_list)                
                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert ongeki item boss for user {pf['user']}")
                        continue

                for pf_list in pf_data["userDeckList"]:
                    pf_list["user"] = user

                    sql = Insert(deck).values(**pf_list)
                    conflict = sql.on_duplicate_key_update(**pf_list)                
                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert ongeki item deck for user {pf['user']}")
                        continue

                for pf_list in pf_data["userStoryList"]:
                    pf_list["user"] = user

                    sql = Insert(story).values(**pf_list)
                    conflict = sql.on_duplicate_key_update(**pf_list)                
                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert ongeki item story for user {pf['user']}")
                        continue

                for pf_list in pf_data["userChapterList"]:
                    pf_list["user"] = user

                    sql = Insert(chapter).values(**pf_list)
                    conflict = sql.on_duplicate_key_update(**pf_list)                
                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert ongeki item chapter for user {pf['user']}")
                        continue

                for pf_list in pf_data["userPlaylogList"]:
                    pf_list["user"] = user

                    sql = Insert(playlog).values(**pf_list)
                    conflict = sql.on_duplicate_key_update(**pf_list)                
                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert ongeki score playlog for user {pf['user']}")
                        continue

                for pf_list in pf_data["userMusicItemList"]:
                    pf_list["user"] = user

                    sql = Insert(music_item).values(**pf_list)
                    conflict = sql.on_duplicate_key_update(**pf_list)                
                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert ongeki item music item for user {pf['user']}")
                        continue

                for pf_list in pf_data["userTechCountList"]:
                    pf_list["user"] = user

                    sql = Insert(tech_count).values(**pf_list)
                    conflict = sql.on_duplicate_key_update(**pf_list)                
                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert ongeki item tech count for user {pf['user']}")
                        continue

                if "userTechEventList" in pf_data:
                    for pf_list in pf_data["userTechEventList"]:
                        pf_list["user"] = user

                        sql = Insert(tech_event).values(**pf_list)
                        conflict = sql.on_duplicate_key_update(**pf_list)                
                        result = self.base.execute(conflict)
                        if result is None:
                            self.logger.error(f"Failed to insert ongeki item tech event for user {pf['user']}")
                            continue

                for pf_list in pf_data["userTradeItemList"]:
                    pf_list["user"] = user

                    sql = Insert(trade_item).values(**pf_list)
                    conflict = sql.on_duplicate_key_update(**pf_list)                
                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert ongeki item trade item for user {pf['user']}")
                        continue

                if "userEventMusicList" in pf_data:
                    for pf_list in pf_data["userEventMusicList"]:
                        pf_list["user"] = user

                        sql = Insert(event_music).values(**pf_list)
                        conflict = sql.on_duplicate_key_update(**pf_list)                
                        result = self.base.execute(conflict)
                        if result is None:
                            self.logger.error(f"Failed to insert ongeki item event music for user {pf['user']}")
                            continue

                if "userEventPointList" in pf_data:
                    for pf_list in pf_data["userEventPointList"]:
                        pf_list["user"] = user

                        sql = Insert(event_point).values(**pf_list)
                        conflict = sql.on_duplicate_key_update(**pf_list)                
                        result = self.base.execute(conflict)
                        if result is None:
                            self.logger.error(f"Failed to insert ongeki item event point for user {pf['user']}")
                            continue

                for pf_list in pf_data["userLoginBonusList"]:
                    pf_list["user"] = user

                    sql = Insert(login_bonus).values(**pf_list)
                    conflict = sql.on_duplicate_key_update(**pf_list)                
                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert ongeki item login bonus for user {pf['user']}")
                        continue

                for pf_list in pf_data["userMissionPointList"]:
                    pf_list["user"] = user

                    sql = Insert(mission_point).values(**pf_list)
                    conflict = sql.on_duplicate_key_update(**pf_list)                
                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert ongeki item mission point for user {pf['user']}")
                        continue

                for pf_list in pf_data["userScenarioList"]:
                    pf_list["user"] = user

                    sql = Insert(scenerio).values(**pf_list)
                    conflict = sql.on_duplicate_key_update(**pf_list)                
                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert ongeki item scenerio for user {pf['user']}")
                        continue
                
                if "userSessionlogList" in pf_data:
                    for pf_list in pf_data["userSessionlogList"]:
                        pf_list["user"] = user

                        sql = Insert(session_log).values(**pf_list)
                        conflict = sql.on_duplicate_key_update(**pf_list)                
                        result = self.base.execute(conflict)
                        if result is None:
                            self.logger.error(f"Failed to insert ongeki log session for user {pf['user']}")
                            continue

            self.logger.info(f"Importing {len(ongeki_items)} ongeki items")
            
            for it in ongeki_items:
                user = it["user"]
                it_type = it["type"]
                it_id = it["item_id"]
                it_data = it["data"]
                it_data["user"] = user

                if it_type == item_types["character"] and "characterId" in it_data:
                    sql = Insert(character).values(**it_data)

                elif it_type == item_types["story"]:
                    sql = Insert(story).values(**it_data)

                elif it_type == item_types["card"]:
                    sql = Insert(card).values(**it_data)

                elif it_type == item_types["deck"]:
                    sql = Insert(deck).values(**it_data)

                elif it_type == item_types["login"]: # login bonus
                    sql = Insert(login_bonus).values(**it_data)

                elif it_type == item_types["chapter"]:
                    sql = Insert(chapter).values(**it_data)

                else:
                    sql = Insert(item).values(**it_data)
                
                conflict = sql.on_duplicate_key_update(**it_data)                
                result = self.base.execute(conflict)
                if result is None:
                    self.logger.error(f"Failed to insert ongeki item {it_id} kind {it_type} for user {user}")
            
            self.logger.info(f"Importing {len(ongeki_scores)} ongeki scores")
            
            for sc in ongeki_scores:
                user = sc["user"]
                sc_data = sc["data"]
                sc_data["user"] = user

                sql = Insert(score_best).values(**sc_data)                
                conflict = sql.on_duplicate_key_update(**sc_data)

                result = self.base.execute(conflict)
                if result is None:
                    self.logger.error(f"Failed to insert ongeki score for user {user}: {sc['song_id']}/{sc['chart_id']}")
        
        else:
            self.logger.info(f"Ongeki not found, skipping...")

        # Wacca
        if os.path.exists("titles/wacca/schema"):
            from titles.wacca.schema.profile import profile, option, bingo, gate, favorite
            from titles.wacca.schema.item import item, ticket, song_unlock, trophy
            from titles.wacca.schema.score import best_score, stageup
            from titles.wacca.reverse import WaccaReverse
            from titles.wacca.const import WaccaConstants

            default_opts = WaccaReverse.OPTIONS_DEFAULTS
            opts = WaccaConstants.OPTIONS
            item_types = WaccaConstants.ITEM_TYPES

            wacca_profiles = []
            wacca_items = []
            wacca_scores = []
            wacca_achievements = []

            if "SDFE" in profiles:
                wacca_profiles = profiles["SDFE"]
            if "SDFE" in items:
                wacca_items = items["SDFE"]
            if "SDFE" in scores:
                wacca_scores = scores["SDFE"]
            if "SDFE" in achievements:
                wacca_achievements = achievements["SDFE"]
            
            self.logger.info(f"Importing {len(wacca_profiles)} wacca profiles")

            for pf in wacca_profiles:
                if pf["version"] == 0 or pf["version"] == 1:
                    season = 1
                elif pf["version"] == 2 or pf["version"] == 3:
                    season = 2
                elif pf["version"] >= 4:
                    season = 3
                
                if type(pf["data"]) is not dict:
                    pf["data"] = json.loads(pf["data"])

                try:
                    sql = Insert(profile).values(
                        id = pf["id"],
                        user = pf["user"],
                        version = pf["version"],
                        season = season,
                        username = pf["data"]["profile"]["username"] if "username" in pf["data"]["profile"] else pf["name"],
                        xp = pf["data"]["profile"]["xp"],
                        xp_season = pf["data"]["profile"]["xp"],
                        wp = pf["data"]["profile"]["wp"],
                        wp_season = pf["data"]["profile"]["wp"],
                        wp_total = pf["data"]["profile"]["total_wp_gained"],
                        dan_type = pf["data"]["profile"]["dan_type"],
                        dan_level = pf["data"]["profile"]["dan_level"],
                        title_0 = pf["data"]["profile"]["title_part_ids"][0],
                        title_1 = pf["data"]["profile"]["title_part_ids"][1],
                        title_2 = pf["data"]["profile"]["title_part_ids"][2],
                        rating = pf["data"]["profile"]["rating"],
                        vip_expire_time = datetime.fromtimestamp(pf["data"]["profile"]["vip_expire_time"]) if "vip_expire_time" in pf["data"]["profile"] else None,
                        login_count = pf["use_count"],
                        playcount_single = pf["use_count"],
                        playcount_single_season = pf["use_count"],
                        last_game_ver = pf["data"]["profile"]["last_game_ver"],
                        last_song_id = pf["data"]["profile"]["last_song_info"][0] if "last_song_info" in pf["data"]["profile"] else 0,
                        last_song_difficulty = pf["data"]["profile"]["last_song_info"][1] if "last_song_info" in pf["data"]["profile"] else 0,
                        last_folder_order = pf["data"]["profile"]["last_song_info"][2] if "last_song_info" in pf["data"]["profile"] else 0,
                        last_folder_id = pf["data"]["profile"]["last_song_info"][3] if "last_song_info" in pf["data"]["profile"] else 0,
                        last_song_order = pf["data"]["profile"]["last_song_info"][4] if "last_song_info" in pf["data"]["profile"] else 0,
                        last_login_date = datetime.fromtimestamp(pf["data"]["profile"]["last_login_timestamp"]),
                    )

                    conflict = sql.on_duplicate_key_update(
                        id = pf["id"],
                        user = pf["user"],
                        version = pf["version"],
                        season = season,
                        username = pf["data"]["profile"]["username"] if "username" in pf["data"]["profile"] else pf["name"],
                        xp = pf["data"]["profile"]["xp"],
                        xp_season = pf["data"]["profile"]["xp"],
                        wp = pf["data"]["profile"]["wp"],
                        wp_season = pf["data"]["profile"]["wp"],
                        wp_total = pf["data"]["profile"]["total_wp_gained"],
                        dan_type = pf["data"]["profile"]["dan_type"],
                        dan_level = pf["data"]["profile"]["dan_level"],
                        title_0 = pf["data"]["profile"]["title_part_ids"][0],
                        title_1 = pf["data"]["profile"]["title_part_ids"][1],
                        title_2 = pf["data"]["profile"]["title_part_ids"][2],
                        rating = pf["data"]["profile"]["rating"],
                        vip_expire_time = datetime.fromtimestamp(pf["data"]["profile"]["vip_expire_time"]) if "vip_expire_time" in pf["data"]["profile"] else None,
                        login_count = pf["use_count"],
                        playcount_single = pf["use_count"],
                        playcount_single_season = pf["use_count"],
                        last_game_ver = pf["data"]["profile"]["last_game_ver"],
                        last_song_id = pf["data"]["profile"]["last_song_info"][0] if "last_song_info" in pf["data"]["profile"] else 0,
                        last_song_difficulty = pf["data"]["profile"]["last_song_info"][1] if "last_song_info" in pf["data"]["profile"] else 0,
                        last_folder_order = pf["data"]["profile"]["last_song_info"][2] if "last_song_info" in pf["data"]["profile"] else 0,
                        last_folder_id = pf["data"]["profile"]["last_song_info"][3] if "last_song_info" in pf["data"]["profile"] else 0,
                        last_song_order = pf["data"]["profile"]["last_song_info"][4] if "last_song_info" in pf["data"]["profile"] else 0,
                        last_login_date = datetime.fromtimestamp(pf["data"]["profile"]["last_login_timestamp"]),
                    )

                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.error(f"Failed to insert wacca profile for user {pf['user']}")
                        continue
                    
                    for opt, val in pf["data"]["option"].items():
                        if val != default_opts[opt]:
                            opt_id = opts[opt]
                            sql = Insert(option).values(
                                user = pf["user"],
                                opt_id = opt_id,
                                value = val,
                            )

                            conflict = sql.on_duplicate_key_update(
                                user = pf["user"],
                                opt_id = opt_id,
                                value = val,
                            )                    
                            result = self.base.execute(conflict)
                            if result is None:
                                self.logger.error(f"Failed to insert wacca option for user {pf['user']} {opt} -> {val}")

                except KeyError as e:
                    self.logger.warn(f"Outdated wacca profile, skipping: {e}")

                if "gate" in pf["data"]:
                    for profile_gate in pf["data"]["gate"]:
                        sql = Insert(gate).values(
                            user = pf["user"],
                            gate_id = profile_gate["id"],
                            page = profile_gate["page"],
                            loops = profile_gate["loops"],
                            progress = profile_gate["progress"],
                            last_used = datetime.fromtimestamp(profile_gate["last_used"]),
                            mission_flag = profile_gate["mission_flag"],
                            total_points = profile_gate["total_points"],
                        )

                        conflict = sql.on_duplicate_key_update(
                            user = pf["user"],
                            gate_id = profile_gate["id"],
                            page = profile_gate["page"],
                            loops = profile_gate["loops"],
                            progress = profile_gate["progress"],
                            last_used = datetime.fromtimestamp(profile_gate["last_used"]),
                            mission_flag = profile_gate["mission_flag"],
                            total_points = profile_gate["total_points"],
                        )                    
                        result = self.base.execute(conflict)
                        if result is None:
                            self.logger.error(f"Failed to insert wacca gate for user {pf['user']} -> {profile_gate['id']}")
                            continue
                
                if "favorite" in pf["data"]:
                    for profile_favorite in pf["data"]["favorite"]:
                        sql = Insert(favorite).values(
                            user = pf["user"],
                            song_id = profile_favorite
                        )

                        conflict = sql.on_duplicate_key_update(
                            user = pf["user"],
                            song_id = profile_favorite
                        )                    
                        result = self.base.execute(conflict)
                        if result is None:
                            self.logger.error(f"Failed to insert wacca favorite songs for user {pf['user']} -> {profile_favorite}")
                            continue
            
            for it in wacca_items:
                user = it["user"]
                item_type = it["type"]
                item_id = it["item_id"]

                if type(it["data"]) is not dict:
                    it["data"] = json.loads(it["data"])

                if item_type == item_types["ticket"]:
                    if "quantity" in it["data"]:
                        for x in range(it["data"]["quantity"]):
                            sql = Insert(ticket).values(
                                user = user,
                                ticket_id = item_id,
                            )

                            conflict = sql.on_duplicate_key_update(
                                user = user,
                                ticket_id = item_id,
                            )                
                            result = self.base.execute(conflict)
                            if result is None:
                                self.logger.warn(f"Wacca: Failed to insert ticket {item_id} for user {user}")
                
                elif item_type == item_types["music_unlock"] or item_type == item_types["music_difficulty_unlock"]:
                    diff = 0
                    if "difficulty" in it["data"]:
                        for x in it["data"]["difficulty"]:
                            if x == 1:
                                diff += 1
                            else:
                                break

                        sql = Insert(song_unlock).values(
                            user = user,
                            song_id = item_id,
                            highest_difficulty = diff,
                        )

                        conflict = sql.on_duplicate_key_update(
                            user = user,
                            song_id = item_id,
                            highest_difficulty = diff,
                        )                
                        result = self.base.execute(conflict)
                        if result is None:
                            self.logger.warn(f"Wacca: Failed to insert song unlock {item_id} {diff} for user {user}")
                
                elif item_type == item_types["trophy"]:
                    season = int(item_id / 100000)
                    sql = Insert(trophy).values(
                        user = user,
                        trophy_id = item_id,
                        season = season,
                        progress = 0 if "progress" not in it["data"] else it["data"]["progress"],
                        badge_type = 0 # ???
                    )
                    
                    conflict = sql.on_duplicate_key_update(
                        user = user,
                        trophy_id = item_id,
                        season = season,
                        progress = 0 if "progress" not in it["data"] else it["data"]["progress"],
                        badge_type = 0 # ???
                    )
                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.warn(f"Wacca: Failed to insert trophy {item_id} for user {user}")
                
                else:
                    sql = Insert(item).values(
                        user = user,
                        item_id = item_id,
                        type = item_type,
                        acquire_date = datetime.fromtimestamp(it["data"]["obtainedDate"]) if "obtainedDate" in it["data"] else datetime.now(),
                        use_count = it["data"]["uses"] if "uses" in it["data"] else 0,
                        use_count_season = it["data"]["season_uses"] if "season_uses" in it["data"] else 0
                    )

                    conflict = sql.on_duplicate_key_update(
                        user = user,
                        item_id = item_id,
                        type = item_type,
                        acquire_date = datetime.fromtimestamp(it["data"]["obtainedDate"]) if "obtainedDate" in it["data"] else datetime.now(),
                        use_count = it["data"]["uses"] if "uses" in it["data"] else 0,
                        use_count_season = it["data"]["season_uses"] if "season_uses" in it["data"] else 0
                    )                
                    result = self.base.execute(conflict)
                    if result is None:
                        self.logger.warn(f"Wacca: Failed to insert trophy {item_id} for user {user}")

            for sc in wacca_scores:
                if type(sc["data"]) is not dict:
                    sc["data"] = json.loads(sc["data"])

                sql = Insert(best_score).values(
                    user = sc["user"],
                    song_id = int(sc["song_id"]),
                    chart_id = sc["chart_id"],
                    score = sc["score1"],
                    play_ct = 1 if "play_count" not in sc["data"] else sc["data"]["play_count"],
                    clear_ct = 1 if sc["cleared"] & 0x01 else 0,
                    missless_ct = 1 if sc["cleared"] & 0x02 else 0,
                    fullcombo_ct = 1 if sc["cleared"] & 0x04 else 0,
                    allmarv_ct = 1 if sc["cleared"] & 0x08 else 0,
                    grade_d_ct = 1 if sc["grade"] & 0x01 else 0,
                    grade_c_ct = 1 if sc["grade"] & 0x02 else 0,
                    grade_b_ct = 1 if sc["grade"] & 0x04 else 0,
                    grade_a_ct = 1 if sc["grade"] & 0x08 else 0,
                    grade_aa_ct = 1 if sc["grade"] & 0x10 else 0,
                    grade_aaa_ct = 1 if sc["grade"] & 0x20 else 0,
                    grade_s_ct = 1 if sc["grade"] & 0x40 else 0,
                    grade_ss_ct = 1 if sc["grade"] & 0x80 else 0,
                    grade_sss_ct = 1 if sc["grade"] & 0x100 else 0,
                    grade_master_ct = 1 if sc["grade"] & 0x200 else 0,
                    grade_sp_ct = 1 if sc["grade"] & 0x400 else 0,
                    grade_ssp_ct = 1 if sc["grade"] & 0x800 else 0,
                    grade_sssp_ct = 1 if sc["grade"] & 0x1000 else 0,
                    best_combo = 0 if "max_combo" not in sc["data"] else sc["data"]["max_combo"],
                    lowest_miss_ct = 0 if "lowest_miss_count" not in sc["data"] else sc["data"]["lowest_miss_count"],
                    rating = 0 if "rating" not in sc["data"] else sc["data"]["rating"],
                )

                conflict = sql.on_duplicate_key_update(
                    user = sc["user"],
                    song_id = int(sc["song_id"]),
                    chart_id = sc["chart_id"],
                    score = sc["score1"],
                    play_ct = 1 if "play_count" not in sc["data"] else sc["data"]["play_count"],
                    clear_ct = 1 if sc["cleared"] & 0x01 else 0,
                    missless_ct = 1 if sc["cleared"] & 0x02 else 0,
                    fullcombo_ct = 1 if sc["cleared"] & 0x04 else 0,
                    allmarv_ct = 1 if sc["cleared"] & 0x08 else 0,
                    grade_d_ct = 1 if sc["grade"] & 0x01 else 0,
                    grade_c_ct = 1 if sc["grade"] & 0x02 else 0,
                    grade_b_ct = 1 if sc["grade"] & 0x04 else 0,
                    grade_a_ct = 1 if sc["grade"] & 0x08 else 0,
                    grade_aa_ct = 1 if sc["grade"] & 0x10 else 0,
                    grade_aaa_ct = 1 if sc["grade"] & 0x20 else 0,
                    grade_s_ct = 1 if sc["grade"] & 0x40 else 0,
                    grade_ss_ct = 1 if sc["grade"] & 0x80 else 0,
                    grade_sss_ct = 1 if sc["grade"] & 0x100 else 0,
                    grade_master_ct = 1 if sc["grade"] & 0x200 else 0,
                    grade_sp_ct = 1 if sc["grade"] & 0x400 else 0,
                    grade_ssp_ct = 1 if sc["grade"] & 0x800 else 0,
                    grade_sssp_ct = 1 if sc["grade"] & 0x1000 else 0,
                    best_combo = 0 if "max_combo" not in sc["data"] else sc["data"]["max_combo"],
                    lowest_miss_ct = 0 if "lowest_miss_count" not in sc["data"] else sc["data"]["lowest_miss_count"],
                    rating = 0 if "rating" not in sc["data"] else sc["data"]["rating"],
                )
                result = self.base.execute(conflict)
                if result is None:
                    self.logger.error(f"Failed to insert wacca score for user {sc['user']} {int(sc['song_id'])} {sc['chart_id']}")

            for ach in wacca_achievements:
                if ach["version"] == 0 or ach["version"] == 1:
                    season = 1
                elif ach["version"] == 2 or ach["version"] == 3:
                    season = 2
                elif ach["version"] >= 4:
                    season = 3

                if type(ach["data"]) is not dict:
                    ach["data"] = json.loads(ach["data"])

                sql = Insert(stageup).values(
                    user = ach["user"],
                    season = season,
                    stage_id = ach["achievement_id"],
                    clear_status = 0 if "clear" not in ach["data"] else ach["data"]["clear"],
                    clear_song_ct = 0 if "clear_song_ct" not in ach["data"] else ach["data"]["clear_song_ct"],
                    song1_score = 0 if "score1" not in ach["data"] else ach["data"]["score1"],
                    song2_score = 0 if "score2" not in ach["data"] else ach["data"]["score2"],
                    song3_score = 0 if "score3" not in ach["data"] else ach["data"]["score3"],
                    play_ct = 1 if "attemps" not in ach["data"] else ach["data"]["attemps"],
                )

                conflict = sql.on_duplicate_key_update(
                    user = ach["user"],
                    season = season,
                    stage_id = ach["achievement_id"],
                    clear_status = 0 if "clear" not in ach["data"] else ach["data"]["clear"],
                    clear_song_ct = 0 if "clear_song_ct" not in ach["data"] else ach["data"]["clear_song_ct"],
                    song1_score = 0 if "score1" not in ach["data"] else ach["data"]["score1"],
                    song2_score = 0 if "score2" not in ach["data"] else ach["data"]["score2"],
                    song3_score = 0 if "score3" not in ach["data"] else ach["data"]["score3"],
                    play_ct = 1 if "attemps" not in ach["data"] else ach["data"]["attemps"],
                )
                result = self.base.execute(conflict)
                if result is None:
                    self.logger.error(f"Failed to insert wacca achievement for user {ach['user']}")
        
        else:
            self.logger.info(f"Wacca not found, skipping...")
