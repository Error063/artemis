from decimal import Decimal
import logging
import os
import re
import csv
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional

from read import BaseReader
from core.config import CoreConfig
from titles.ongeki.database import OngekiData
from titles.cm.const import CardMakerConstants
from titles.ongeki.const import OngekiConstants
from titles.ongeki.config import OngekiConfig


class CardMakerReader(BaseReader):
    def __init__(
        self,
        config: CoreConfig,
        version: int,
        bin_dir: Optional[str],
        opt_dir: Optional[str],
        extra: Optional[str],
    ) -> None:
        super().__init__(config, version, bin_dir, opt_dir, extra)
        self.ongeki_data = OngekiData(config)

        try:
            self.logger.info(
                f"Start importer for {CardMakerConstants.game_ver_to_string(version)}"
            )
        except IndexError:
            self.logger.error(f"Invalid Card Maker version {version}")
            exit(1)

    def read(self) -> None:
        static_datas = {
            "static_gachas.csv": "read_ongeki_gacha_csv",
            "static_gacha_cards.csv": "read_ongeki_gacha_card_csv",
        }

        data_dirs = []

        if self.bin_dir is not None:
            for file, func in static_datas.items():
                if os.path.exists(f"{self.bin_dir}/MU3/{file}"):
                    read_csv = getattr(CardMakerReader, func)
                    read_csv(self, f"{self.bin_dir}/MU3/{file}")
                else:
                    self.logger.warn(
                        f"Couldn't find {file} file in {self.bin_dir}, skipping"
                    )

        if self.opt_dir is not None:
            data_dirs += self.get_data_directories(self.opt_dir)

            # ONGEKI (MU3) cnnot easily access the bin data(A000.pac)
            # so only opt_dir will work for now
            for dir in data_dirs:
                self.read_ongeki_gacha(f"{dir}/MU3/gacha")

    def read_ongeki_gacha_csv(self, file_path: str) -> None:
        self.logger.info(f"Reading gachas from {file_path}...")

        with open(file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.ongeki_data.static.put_gacha(
                    row["version"],
                    row["gachaId"],
                    row["gachaName"],
                    row["kind"],
                    type=row["type"],
                    isCeiling=True if row["isCeiling"] == "1" else False,
                    maxSelectPoint=row["maxSelectPoint"],
                )

                self.logger.info(f"Added gacha {row['gachaId']}")

    def read_ongeki_gacha_card_csv(self, file_path: str) -> None:
        self.logger.info(f"Reading gacha cards from {file_path}...")

        with open(file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.ongeki_data.static.put_gacha_card(
                    row["gachaId"],
                    row["cardId"],
                    rarity=row["rarity"],
                    weight=row["weight"],
                    isPickup=True if row["isPickup"] == "1" else False,
                    isSelect=True if row["isSelect"] == "1" else False,
                )

                self.logger.info(f"Added card {row['cardId']} to gacha")

    def read_ongeki_gacha(self, base_dir: str) -> None:
        self.logger.info(f"Reading gachas from {base_dir}...")

        # assuming some GachaKinds based on the GachaType
        type_to_kind = {
            "Normal": "Normal",
            "Pickup": "Pickup",
            "RecoverFiveShotFlag": "BonusRestored",
            "Free": "Free",
            "FreeSR": "Free",
        }

        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                if os.path.exists(f"{root}/{dir}/Gacha.xml"):
                    with open(f"{root}/{dir}/Gacha.xml", "r", encoding="utf-8") as f:
                        troot = ET.fromstring(f.read())

                        name = troot.find("Name").find("str").text
                        gacha_id = int(troot.find("Name").find("id").text)

                        # skip already existing gachas
                        if (
                            self.ongeki_data.static.get_gacha(
                                OngekiConstants.VER_ONGEKI_BRIGHT_MEMORY, gacha_id
                            )
                            is not None
                        ):
                            self.logger.info(
                                f"Gacha {gacha_id} already added, skipping"
                            )
                            continue

                        # 1140 is the first bright memory gacha
                        if gacha_id < 1140:
                            version = OngekiConstants.VER_ONGEKI_BRIGHT
                        else:
                            version = OngekiConstants.VER_ONGEKI_BRIGHT_MEMORY

                        gacha_kind = OngekiConstants.CM_GACHA_KINDS[
                            type_to_kind[troot.find("Type").text]
                        ].value

                        # hardcode which gachas get "Select Gacha" with 33 points
                        is_ceiling, max_select_point = 0, 0
                        if gacha_id in {1163, 1164, 1165, 1166, 1167, 1168}:
                            is_ceiling = 1
                            max_select_point = 33

                        self.ongeki_data.static.put_gacha(
                            version,
                            gacha_id,
                            name,
                            gacha_kind,
                            isCeiling=is_ceiling,
                            maxSelectPoint=max_select_point,
                        )
                        self.logger.info(f"Added gacha {gacha_id}")
