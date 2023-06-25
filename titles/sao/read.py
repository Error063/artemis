from typing import Optional, Dict, List
from os import walk, path
import urllib
import csv

from read import BaseReader
from core.config import CoreConfig
from titles.sao.database import SaoData
from titles.sao.const import SaoConstants


class SaoReader(BaseReader):
    def __init__(
        self,
        config: CoreConfig,
        version: int,
        bin_arg: Optional[str],
        opt_arg: Optional[str],
        extra: Optional[str],
    ) -> None:
        super().__init__(config, version, bin_arg, opt_arg, extra)
        self.data = SaoData(config)

        try:
            self.logger.info(
                f"Start importer for {SaoConstants.game_ver_to_string(version)}"
            )
        except IndexError:
            self.logger.error(f"Invalid project SAO version {version}")
            exit(1)

    def read(self) -> None:
        pull_bin_ram = True

        if not path.exists(f"{self.bin_dir}"):
            self.logger.warn(f"Couldn't find csv file in {self.bin_dir}, skipping")
            pull_bin_ram = False

        if pull_bin_ram:
            self.read_csv(f"{self.bin_dir}")

    def read_csv(self, bin_dir: str) -> None:
        self.logger.info(f"Read csv from {bin_dir}")

        self.logger.info("Now reading QuestScene.csv")
        try:
            fullPath = bin_dir + "/QuestScene.csv"
            with open(fullPath, encoding="UTF-8") as fp:
                reader = csv.DictReader(fp)
                for row in reader:
                    questSceneId = row["QuestSceneId"]
                    sortNo = row["SortNo"]
                    name = row["Name"]
                    enabled = True

                    self.logger.info(f"Added quest {questSceneId} | Name: {name}")
                    
                    try:
                        self.data.static.put_quest(
                            questSceneId,
                            0,
                            sortNo,
                            name,
                            enabled
                        )
                    except Exception as err:
                        print(err)
        except:
            self.logger.warn(f"Couldn't read csv file in {self.bin_dir}, skipping")
        
        self.logger.info("Now reading HeroLog.csv")
        try:
            fullPath = bin_dir + "/HeroLog.csv"
            with open(fullPath, encoding="UTF-8") as fp:
                reader = csv.DictReader(fp)
                for row in reader:
                    heroLogId = row["HeroLogId"]
                    name = row["Name"]
                    nickname = row["Nickname"]
                    rarity = row["Rarity"]
                    skillTableSubId = row["SkillTableSubId"]
                    awakeningExp = row["AwakeningExp"]
                    flavorText = row["FlavorText"]
                    enabled = True

                    self.logger.info(f"Added hero {heroLogId} | Name: {name}")
                    
                    try:
                        self.data.static.put_hero(
                            0,
                            heroLogId,
                            name,
                            nickname,
                            rarity,
                            skillTableSubId,
                            awakeningExp,
                            flavorText,
                            enabled
                        )
                    except Exception as err:
                        print(err)
        except:
            self.logger.warn(f"Couldn't read csv file in {self.bin_dir}, skipping")
        
        self.logger.info("Now reading Equipment.csv")
        try:
            fullPath = bin_dir + "/Equipment.csv"
            with open(fullPath, encoding="UTF-8") as fp:
                reader = csv.DictReader(fp)
                for row in reader:
                    equipmentId = row["EquipmentId"]
                    equipmentType = row["EquipmentType"]
                    weaponTypeId = row["WeaponTypeId"]
                    name = row["Name"]
                    rarity = row["Rarity"]
                    flavorText = row["FlavorText"]
                    enabled = True

                    self.logger.info(f"Added equipment {equipmentId} | Name: {name}")
                    
                    try:
                        self.data.static.put_equipment(
                            0,
                            equipmentId,
                            name,
                            equipmentType,
                            weaponTypeId,
                            rarity,
                            flavorText,
                            enabled
                        )
                    except Exception as err:
                        print(err)
        except:
            self.logger.warn(f"Couldn't read csv file in {self.bin_dir}, skipping")

        self.logger.info("Now reading Item.csv")
        try:
            fullPath = bin_dir + "/Item.csv"
            with open(fullPath, encoding="UTF-8") as fp:
                reader = csv.DictReader(fp)
                for row in reader:
                    itemId = row["ItemId"]
                    itemTypeId = row["ItemTypeId"]
                    name = row["Name"]
                    rarity = row["Rarity"]
                    flavorText = row["FlavorText"]
                    enabled = True

                    self.logger.info(f"Added item {itemId} | Name: {name}")
                    
                    try:
                        self.data.static.put_item(
                            0,
                            itemId,
                            name,
                            itemTypeId,
                            rarity,
                            flavorText,
                            enabled
                        )
                    except Exception as err:
                        print(err)
        except:
            self.logger.warn(f"Couldn't read csv file in {self.bin_dir}, skipping")
        
        self.logger.info("Now reading SupportLog.csv")
        try:
            fullPath = bin_dir + "/SupportLog.csv"
            with open(fullPath, encoding="UTF-8") as fp:
                reader = csv.DictReader(fp)
                for row in reader:
                    supportLogId = row["SupportLogId"]
                    charaId = row["CharaId"]
                    name = row["Name"]
                    rarity = row["Rarity"]
                    salePrice = row["SalePrice"]
                    skillName = row["SkillName"]
                    enabled = True

                    self.logger.info(f"Added support log {supportLogId} | Name: {name}")
                    
                    try:
                        self.data.static.put_support_log(
                            0,
                            supportLogId,
                            charaId,
                            name,
                            rarity,
                            salePrice,
                            skillName,
                            enabled
                        )
                    except Exception as err:
                        print(err)
        except:
            self.logger.warn(f"Couldn't read csv file in {self.bin_dir}, skipping")
            
        self.logger.info("Now reading Title.csv")
        try:
            fullPath = bin_dir + "/Title.csv"
            with open(fullPath, encoding="UTF-8") as fp:
                reader = csv.DictReader(fp)
                for row in reader:
                    titleId = row["TitleId"]
                    displayName = row["DisplayName"]
                    requirement = row["Requirement"]
                    rank = row["Rank"]
                    imageFilePath = row["ImageFilePath"]
                    enabled = True

                    self.logger.info(f"Added title {titleId} | Name: {displayName}")
                    
                    if len(titleId) > 5:
                        try:
                            self.data.static.put_title(
                                0,
                                titleId,
                                displayName,
                                requirement,
                                rank,
                                imageFilePath,
                                enabled
                            )
                        except Exception as err:
                            print(err)
                    elif len(titleId) < 6: # current server code cannot have multiple lengths for the id
                        continue
        except:
            self.logger.warn(f"Couldn't read csv file in {self.bin_dir}, skipping")

        self.logger.info("Now reading RareDropTable.csv")
        try:
            fullPath = bin_dir + "/RareDropTable.csv"
            with open(fullPath, encoding="UTF-8") as fp:
                reader = csv.DictReader(fp)
                for row in reader:
                    questRareDropId = row["QuestRareDropId"]
                    commonRewardId = row["CommonRewardId"]
                    enabled = True

                    self.logger.info(f"Added rare drop {questRareDropId} | Reward: {commonRewardId}")
                    
                    try:
                        self.data.static.put_rare_drop(
                            0,
                            questRareDropId,
                            commonRewardId,
                            enabled
                        )
                    except Exception as err:
                        print(err)
        except:
            self.logger.warn(f"Couldn't read csv file in {self.bin_dir}, skipping")
