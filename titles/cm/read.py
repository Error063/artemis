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
from titles.mai2.database import Mai2Data
from titles.mai2.const import Mai2Constants
from titles.chuni.database import ChuniData
from titles.chuni.const import ChuniConstants


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
        self.mai2_data = Mai2Data(config)
        self.chuni_data = ChuniData(config)

        try:
            self.logger.info(
                f"Start importer for {CardMakerConstants.game_ver_to_string(version)}"
            )
        except IndexError:
            self.logger.error(f"Invalid Card Maker version {version}")
            exit(1)

    def _get_card_maker_directory(self, directory: str) -> str:
        for root, dirs, files in os.walk(directory):
            for dir in dirs:
                if (
                    os.path.exists(f"{root}/{dir}/MU3")
                    and os.path.exists(f"{root}/{dir}/MAI")
                    and os.path.exists(f"{root}/{dir}/CHU")
                ):
                    return f"{root}/{dir}"

    async def read(self) -> None:
        static_datas = {
            "static_gachas.csv": "read_ongeki_gacha_csv",
            "static_gacha_cards.csv": "read_ongeki_gacha_card_csv",
        }

        if self.bin_dir is not None:
            data_dir = self._get_card_maker_directory(self.bin_dir)

            self.read_chuni_card(f"{data_dir}/CHU/Data/A000/card")
            self.read_chuni_gacha(f"{data_dir}/CHU/Data/A000/gacha")

            self.read_mai2_card(f"{data_dir}/MAI/Data/A000/card")
            for file, func in static_datas.items():
                if os.path.exists(f"{self.bin_dir}/MU3/{file}"):
                    read_csv = getattr(CardMakerReader, func)
                    await read_csv(self, f"{self.bin_dir}/MU3/{file}")
                else:
                    self.logger.warning(
                        f"Couldn't find {file} file in {self.bin_dir}, skipping"
                    )

        if self.opt_dir is not None:
            data_dirs = self.get_data_directories(self.opt_dir)

            # ONGEKI (MU3) cnnot easily access the bin data(A000.pac)
            # so only opt_dir will work for now
            for dir in data_dirs:
                await self.read_chuni_card(f"{dir}/CHU/card")
                await self.read_chuni_gacha(f"{dir}/CHU/gacha")
                await self.read_mai2_card(f"{dir}/MAI/card")
                await self.read_ongeki_gacha(f"{dir}/MU3/gacha")

    async def read_chuni_card(self, base_dir: str) -> None:
        self.logger.info(f"Reading cards from {base_dir}...")

        version_ids = {
            "v2_00": ChuniConstants.VER_CHUNITHM_NEW,
            "v2_05": ChuniConstants.VER_CHUNITHM_NEW_PLUS,
            "v2_10": ChuniConstants.VER_CHUNITHM_SUN,
        }

        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                if os.path.exists(f"{root}/{dir}/Card.xml"):
                    with open(f"{root}/{dir}/Card.xml", "r", encoding="utf-8") as f:
                        troot = ET.fromstring(f.read())

                        card_id = int(troot.find("name").find("id").text)

                        chara_name = troot.find("chuniCharaName").find("str").text
                        chara_id = troot.find("chuniCharaName").find("id").text
                        version = version_ids[
                            troot.find("netOpenName").find("str").text[:5]
                        ]
                        present_name = troot.find("chuniPresentName").find("str").text
                        rarity = int(troot.find("rareType").text)
                        label = int(troot.find("labelType").text)
                        dif = int(troot.find("difType").text)
                        miss = int(troot.find("miss").text)
                        combo = int(troot.find("combo").text)
                        chain = int(troot.find("chain").text)
                        skill_name = troot.find("skillName").text

                        await self.chuni_data.static.put_card(
                            version,
                            card_id,
                            charaName=chara_name,
                            charaId=chara_id,
                            presentName=present_name,
                            rarity=rarity,
                            labelType=label,
                            difType=dif,
                            miss=miss,
                            combo=combo,
                            chain=chain,
                            skillName=skill_name,
                        )

                        self.logger.info(f"Added chuni card {card_id}")

    async def read_chuni_gacha(self, base_dir: str) -> None:
        self.logger.info(f"Reading gachas from {base_dir}...")

        version_ids = {
            "v2_00": ChuniConstants.VER_CHUNITHM_NEW,
            "v2_05": ChuniConstants.VER_CHUNITHM_NEW_PLUS,
            "v2_10": ChuniConstants.VER_CHUNITHM_SUN,
        }

        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                if os.path.exists(f"{root}/{dir}/Gacha.xml"):
                    with open(f"{root}/{dir}/Gacha.xml", "r", encoding="utf-8") as f:
                        troot = ET.fromstring(f.read())

                        name = troot.find("gachaName").text
                        gacha_id = int(troot.find("name").find("id").text)

                        version = version_ids[
                            troot.find("netOpenName").find("str").text[:5]
                        ]
                        ceiling_cnt = int(troot.find("ceilingNum").text)
                        gacha_type = int(troot.find("gachaType").text)
                        is_ceiling = (
                            True if troot.find("ceilingType").text == "1" else False
                        )

                        await self.chuni_data.static.put_gacha(
                            version,
                            gacha_id,
                            name,
                            type=gacha_type,
                            isCeiling=is_ceiling,
                            ceilingCnt=ceiling_cnt,
                        )

                        self.logger.info(f"Added chuni gacha {gacha_id}")

                        for gacha_card in troot.find("infos").iter("GachaCardDataInfo"):
                            # get the card ID from the id element
                            card_id = gacha_card.find("cardName").find("id").text

                            # get the weight from the weight element
                            weight = int(gacha_card.find("weight").text)

                            # get the pickup flag from the pickup element
                            is_pickup = (
                                True if gacha_card.find("pickup").text == "1" else False
                            )

                            await self.chuni_data.static.put_gacha_card(
                                gacha_id,
                                card_id,
                                weight=weight,
                                rarity=2,
                                isPickup=is_pickup,
                            )

                            self.logger.info(
                                f"Added chuni card {card_id} to gacha {gacha_id}"
                            )

    async def read_mai2_card(self, base_dir: str) -> None:
        self.logger.info(f"Reading cards from {base_dir}...")

        version_ids = {
            "1.00": Mai2Constants.VER_MAIMAI_DX,
            "1.05": Mai2Constants.VER_MAIMAI_DX_PLUS,
            "1.09": Mai2Constants.VER_MAIMAI_DX_PLUS,
            "1.10": Mai2Constants.VER_MAIMAI_DX_SPLASH,
            "1.15": Mai2Constants.VER_MAIMAI_DX_SPLASH_PLUS,
            "1.20": Mai2Constants.VER_MAIMAI_DX_UNIVERSE,
            "1.25": Mai2Constants.VER_MAIMAI_DX_UNIVERSE_PLUS,
            "1.30": Mai2Constants.VER_MAIMAI_DX_FESTIVAL,
            "1.35": Mai2Constants.VER_MAIMAI_DX_FESTIVAL_PLUS,
        }

        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                if os.path.exists(f"{root}/{dir}/Card.xml"):
                    with open(f"{root}/{dir}/Card.xml", "r", encoding="utf-8") as f:
                        troot = ET.fromstring(f.read())

                        name = troot.find("name").find("str").text
                        card_id = int(troot.find("name").find("id").text)

                        version = version_ids[
                            troot.find("enableVersion").find("str").text
                        ]

                        enabled = (
                            True if troot.find("disable").text == "false" else False
                        )

                        # check if a date is part of the name and disable the
                        # card if it is
                        enabled = (
                            False if re.search(r"\d{2}/\d{2}/\d{2}", name) else enabled
                        )

                        await self.mai2_data.static.put_card(
                            version, card_id, name, enabled=enabled
                        )
                        self.logger.info(f"Added mai2 card {card_id}")

    async def read_ongeki_gacha_csv(self, file_path: str) -> None:
        self.logger.info(f"Reading gachas from {file_path}...")

        with open(file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                await self.ongeki_data.static.put_gacha(
                    row["version"],
                    row["gachaId"],
                    row["gachaName"],
                    row["kind"],
                    type=row["type"],
                    isCeiling=True if row["isCeiling"] == "1" else False,
                    maxSelectPoint=row["maxSelectPoint"],
                )

                self.logger.info(f"Added ongeki gacha {row['gachaId']}")

    async def read_ongeki_gacha_card_csv(self, file_path: str) -> None:
        self.logger.info(f"Reading gacha cards from {file_path}...")

        with open(file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                await self.ongeki_data.static.put_gacha_card(
                    row["gachaId"],
                    row["cardId"],
                    rarity=row["rarity"],
                    weight=row["weight"],
                    isPickup=True if row["isPickup"] == "1" else False,
                    isSelect=True if row["isSelect"] == "1" else False,
                )

                self.logger.info(f"Added ongeki card {row['cardId']} to gacha")

    async def read_ongeki_gacha(self, base_dir: str) -> None:
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
                            await self.ongeki_data.static.get_gacha(
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

                        await self.ongeki_data.static.put_gacha(
                            version,
                            gacha_id,
                            name,
                            gacha_kind,
                            isCeiling=is_ceiling,
                            maxSelectPoint=max_select_point,
                        )
                        self.logger.info(f"Added ongeki gacha {gacha_id}")
