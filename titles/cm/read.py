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
    def __init__(self, config: CoreConfig, version: int, bin_dir: Optional[str],
                 opt_dir: Optional[str], extra: Optional[str]) -> None:
        super().__init__(config, version, bin_dir, opt_dir, extra)
        self.ongeki_data = OngekiData(config)

        try:
            self.logger.info(
                f"Start importer for {CardMakerConstants.game_ver_to_string(version)}")
        except IndexError:
            self.logger.error(f"Invalid ongeki version {version}")
            exit(1)

    def read(self) -> None:
        static_datas = {
            "static_cards.csv": "read_ongeki_card_csv",
            "static_gachas.csv": "read_ongeki_gacha_csv",
            "static_gacha_cards.csv": "read_ongeki_gacha_card_csv"
        }

        if self.bin_dir is not None:
            for file, func in static_datas.items():
                if os.path.exists(f"{self.bin_dir}/MU3/{file}"):
                    read_csv = getattr(CardMakerReader, func)
                    read_csv(self, f"{self.bin_dir}/MU3/{file}")
                else:
                    self.logger.warn(f"Couldn't find {file} file in {self.bin_dir}, skipping")

        if self.opt_dir is not None:
            dir = self.get_data_directories(self.opt_dir)

            # ONGEKI (MU3) cnnot easily access the bin data(A000.pac)
            # so only opt_dir will work for now
            self.read_gacha(f"{dir}/MU3/gacha")
            self.read_card(f"{dir}/MU3/card")

    def read_ongeki_card_csv(self, file_path: str) -> None:
        self.logger.info(f"Reading cards from {file_path}...")

        with open(file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.ongeki_data.static.put_card(
                    row["version"],
                    row["cardId"],
                    name=row["name"],
                    charaId=row["charaId"],
                    nickName=row["nickName"] if row["nickName"] != "" else None,
                    school=row["school"],
                    attribute=row["attribute"],
                    gakunen=row["gakunen"],
                    rarity=row["rarity"],
                    levelParam=row["levelParam"],
                    skillId=row["skillId"],
                    choKaikaSkillId=row["choKaikaSkillId"],
                    cardNumber=row["cardNumber"] if row["cardNumber"] != "" else None
                )

                self.logger.info(f"Added card {row['cardId']}")

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
                    ceilingCnt=row["ceilingCnt"],
                    changeRateCnt1=row["changeRateCnt1"],
                    changeRateCnt2=row["changeRateCnt2"]
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
                    isSelect=True if row["isSelect"] == "1" else False
                )

                self.logger.info(f"Added card {row['cardId']} to gacha")

    def read_ongeki_card(self, base_dir: str) -> None:
        self.logger.info(f"Reading cards from {base_dir}...")

        version_ids = {
            '1000': OngekiConstants.VER_ONGEKI,
            '1005': OngekiConstants.VER_ONGEKI_PLUS,
            '1010': OngekiConstants.VER_ONGEKI_SUMMER,
            '1015': OngekiConstants.VER_ONGEKI_SUMMER_PLUS,
            '1020': OngekiConstants.VER_ONGEKI_RED,
            '1025': OngekiConstants.VER_ONGEKI_RED_PLUS,
            '1030': OngekiConstants.VER_ONGEKI_BRIGHT,
            '1035': OngekiConstants.VER_ONGEKI_BRIGHT_MEMORY
        }

        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                if os.path.exists(f"{root}/{dir}/Card.xml"):
                    with open(f"{root}/{dir}/Card.xml", "r", encoding="utf-8") as f:
                        troot = ET.fromstring(f.read())

                        card_id = int(troot.find('Name').find('id').text)
                        name = troot.find('Name').find('str').text
                        chara_id = int(troot.find('CharaID').find('id').text)
                        nick_name = troot.find('NickName').text
                        school = troot.find('School').find('str').text
                        attribute = troot.find('Attribute').text
                        gakunen = troot.find('Gakunen').find('str').text
                        rarity = OngekiConstants.RARITY_TYPES[
                            troot.find('Rarity').text].value

                        level_param = []
                        for lvl in troot.find('LevelParam').findall('int'):
                            level_param.append(lvl.text)

                        skill_id = int(troot.find('SkillID').find('id').text)
                        cho_kai_ka_skill_id = int(troot.find('ChoKaikaSkillID').find('id').text)

                        version = version_ids[
                            troot.find('VersionID').find('id').text]
                        card_number = troot.find('CardNumberString').text

                        self.ongeki_data.static.put_card(
                            version,
                            card_id,
                            name=name,
                            charaId=chara_id,
                            nickName=nick_name,
                            school=school,
                            attribute=attribute,
                            gakunen=gakunen,
                            rarity=rarity,
                            levelParam=','.join(level_param),
                            skillId=skill_id,
                            choKaikaSkillId=cho_kai_ka_skill_id,
                            cardNumber=card_number
                        )
                        self.logger.info(f"Added card {card_id}")

    def read_ongeki_gacha(self, base_dir: str) -> None:
        self.logger.info(f"Reading gachas from {base_dir}...")

        # assuming some GachaKinds based on the GachaType
        type_to_kind = {
            "Normal": "Normal",
            "Pickup": "Pickup",
            "RecoverFiveShotFlag": "BonusRestored",
            "Free": "Free",
            "FreeSR": "Free"
        }

        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                if os.path.exists(f"{root}/{dir}/Gacha.xml"):
                    with open(f"{root}/{dir}/Gacha.xml", "r", encoding="utf-8") as f:
                        troot = ET.fromstring(f.read())

                        name = troot.find('Name').find('str').text
                        id = int(troot.find('Name').find('id').text)

                        gacha_kind = OngekiConstants.CM_GACHA_KINDS[
                            type_to_kind[troot.find('Type').text]].value

                        self.ongeki_data.static.put_gacha(
                            self.version, id, name, gacha_kind)
                        self.logger.info(f"Added gacha {id}")
