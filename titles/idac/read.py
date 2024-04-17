import json
import logging
import os
from typing import Any, Dict, List, Optional

from read import BaseReader
from core.data import Data
from core.config import CoreConfig
from titles.idac.const import IDACConstants
from titles.idac.database import IDACData
from titles.idac.schema.profile import *
from titles.idac.schema.item import *


class IDACReader(BaseReader):
    def __init__(
        self,
        config: CoreConfig,
        version: int,
        bin_dir: Optional[str],
        opt_dir: Optional[str],
        extra: Optional[str],
    ) -> None:
        super().__init__(config, version, bin_dir, opt_dir, extra)
        self.card_data = Data(config).card
        self.data = IDACData(config)

        try:
            self.logger.info(
                f"Start importer for {IDACConstants.game_ver_to_string(version)}"
            )
        except IndexError:
            self.logger.error(f"Invalid Initial D THE ARCADE version {version}")
            exit(1)

    async def read(self) -> None:
        if self.bin_dir is None and self.opt_dir is None:
            self.logger.error(
                (
                    "To import your profile specify the '--optfolder'",
                    " path to your idac_profile.json file, exiting",
                )
            )
            exit(1)

        if self.opt_dir is not None:
            if not os.path.exists(self.opt_dir):
                self.logger.error(
                    f"Path to idac_profile.json does not exist: {self.opt_dir}"
                )
                exit(1)

            if os.path.isdir(self.opt_dir):
                self.opt_dir = os.path.join(self.opt_dir, "idac_profile.json")

            if not os.path.isfile(self.opt_dir) or self.opt_dir[-5:] != ".json":
                self.logger.error(
                    f"Path to idac_profile.json does not exist: {self.opt_dir}"
                )
                exit(1)

            await self.read_idac_profile(self.opt_dir)

    async def read_idac_profile(self, file_path: str) -> None:
        self.logger.info(f"Reading profile from {file_path}...")

        # read it as binary to avoid encoding issues
        profile_data: Dict[str, Any] = {}
        with open(file_path, "rb") as f:
            profile_data = json.loads(f.read().decode("utf-8"))

        if not profile_data:
            self.logger.error("Profile could not be parsed, exiting")
            exit(1)

        access_code = None
        while access_code is None:
            access_code = input("Enter your 20 digits access code: ")
            if len(access_code) != 20 or not access_code.isdigit():
                access_code = None
                self.logger.warning("Invalid access code, please try again.")

        # check if access code already exists, if not create a new profile
        user_id = self.card_data.get_user_id_from_card(access_code)
        if user_id is None:
            choice = input("Access code does not exist, do you want to create a new profile? (Y/n): ")
            if choice.lower() == "n":
                self.logger.info("Exiting...")
                exit(0)

            user_id = await self.data.user.create_user()

            if user_id is None:
                self.logger.error("Failed to register user!")
                user_id = -1

            else:
                card_id = await self.data.card.create_card(user_id, access_code)

                if card_id is None:
                    self.logger.error("Failed to register card!")
                    user_id = -1

        if user_id == -1:
            self.logger.error("Failed to create profile, exiting")
            exit(1)

        # table mapping to insert the data properly
        tables = {
            "idac_profile": profile,
            "idac_profile_config": config,
            "idac_profile_avatar": avatar,
            "idac_profile_rank": rank,
            "idac_profile_stock": stock,
            "idac_profile_theory": theory,
            "idac_user_car": car,
            "idac_user_ticket": ticket,
            "idac_user_story": story,
            "idac_user_story_episode": episode,
            "idac_user_story_episode_difficulty": difficulty,
            "idac_user_course": course,
            "idac_user_time_trial": trial,
            "idac_user_challenge": challenge,
            "idac_user_theory_course": theory_course,
            "idac_user_theory_partner": theory_partner,
            "idac_user_theory_running": theory_running,
            "idac_user_vs_info": vs_info,
            "idac_user_stamp": stamp,
            "idac_user_timetrial_event": timetrial_event,
        }

        for name, data_list in profile_data.items():
            # get the SQLAlchemy table object from the name
            table = tables.get(name)
            if table is None:
                self.logger.warning(f"Unknown table {name}, skipping")
                continue

            for data in data_list:
                # add user to the data
                data["user"] = user_id

                # check if the table has a version column
                if "version" in table.c:
                    data["version"] = self.version

                sql = insert(table).values(
                    **data
                )

                # lol use the profile connection for items, dirty hack
                conflict = sql.on_duplicate_key_update(**data)
                result = await self.data.profile.execute(conflict)

                if result is None:
                    self.logger.error(f"Failed to insert data into table {name}")
                    exit(1)

                self.logger.info(f"Inserted data into table {name}")

        self.logger.info("Profile import complete!")
