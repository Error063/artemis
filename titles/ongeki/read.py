import os
import xml.etree.ElementTree as ET
from typing import Optional

from read import BaseReader
from core.config import CoreConfig
from titles.ongeki.database import OngekiData
from titles.ongeki.const import OngekiConstants

class OngekiReader(BaseReader):
    def __init__(
        self,
        config: CoreConfig,
        version: int,
        bin_dir: Optional[str],
        opt_dir: Optional[str],
        extra: Optional[str],
    ) -> None:
        super().__init__(config, version, bin_dir, opt_dir, extra)
        self.data = OngekiData(config)

        try:
            self.logger.info(
                f"Start importer for {OngekiConstants.game_ver_to_string(version)}"
            )
        except IndexError:
            self.logger.error(f"Invalid ongeki version {version}")
            exit(1)

    async def read(self) -> None:
        data_dirs = []
        if self.bin_dir is not None:
            data_dirs += self.get_data_directories(self.bin_dir)

        if self.opt_dir is not None:
            data_dirs += self.get_data_directories(self.opt_dir)

        for dir in data_dirs:
            await self.read_events(f"{dir}/event")
            await self.read_music(f"{dir}/music")
            await self.read_card(f"{dir}/card")
            await self.read_reward(f"{dir}/reward")

    async def read_card(self, base_dir: str) -> None:
        self.logger.info(f"Reading cards from {base_dir}...")

        version_ids = {
            "1000": OngekiConstants.VER_ONGEKI,
            "1005": OngekiConstants.VER_ONGEKI_PLUS,
            "1010": OngekiConstants.VER_ONGEKI_SUMMER,
            "1015": OngekiConstants.VER_ONGEKI_SUMMER_PLUS,
            "1020": OngekiConstants.VER_ONGEKI_RED,
            "1025": OngekiConstants.VER_ONGEKI_RED_PLUS,
            "1030": OngekiConstants.VER_ONGEKI_BRIGHT,
            "1035": OngekiConstants.VER_ONGEKI_BRIGHT_MEMORY,
        }

        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                if os.path.exists(f"{root}/{dir}/Card.xml"):
                    with open(f"{root}/{dir}/Card.xml", "r", encoding="utf-8") as f:
                        troot = ET.fromstring(f.read())

                        card_id = int(troot.find("Name").find("id").text)

                        # skip already existing cards
                        if (
                            await self.data.static.get_card(
                                OngekiConstants.VER_ONGEKI_BRIGHT_MEMORY, card_id
                            )
                            is not None
                        ):
                            self.logger.info(f"Card {card_id} already added, skipping")
                            continue

                        name = troot.find("Name").find("str").text
                        chara_id = int(troot.find("CharaID").find("id").text)
                        nick_name = troot.find("NickName").text
                        school = troot.find("School").find("str").text
                        attribute = troot.find("Attribute").text
                        gakunen = troot.find("Gakunen").find("str").text
                        rarity = OngekiConstants.RARITY_TYPES[
                            troot.find("Rarity").text
                        ].value

                        level_param = []
                        for lvl in troot.find("LevelParam").findall("int"):
                            level_param.append(lvl.text)

                        skill_id = int(troot.find("SkillID").find("id").text)
                        cho_kai_ka_skill_id = int(
                            troot.find("ChoKaikaSkillID").find("id").text
                        )

                        version = version_ids[troot.find("VersionID").find("id").text]
                        card_number = troot.find("CardNumberString").text

                        await self.data.static.put_card(
                            version,
                            card_id,
                            name=name,
                            charaId=chara_id,
                            nickName=nick_name,
                            school=school,
                            attribute=attribute,
                            gakunen=gakunen,
                            rarity=rarity,
                            levelParam=",".join(level_param),
                            skillId=skill_id,
                            choKaikaSkillId=cho_kai_ka_skill_id,
                            cardNumber=card_number,
                        )
                        self.logger.info(f"Added card {card_id}")

    async def read_events(self, base_dir: str) -> None:
        self.logger.info(f"Reading events from {base_dir}...")

        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                if os.path.exists(f"{root}/{dir}/Event.xml"):
                    with open(f"{root}/{dir}/Event.xml", "r", encoding="utf-8") as f:
                        troot = ET.fromstring(f.read())

                        name = troot.find("Name").find("str").text
                        id = int(troot.find("Name").find("id").text)
                        event_type = OngekiConstants.EVT_TYPES[
                            troot.find("EventType").text
                        ].value

                        await self.data.static.put_event(self.version, id, event_type, name)
                        self.logger.info(f"Added event {id}")

    async def read_music(self, base_dir: str) -> None:
        self.logger.info(f"Reading music from {base_dir}...")

        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                if os.path.exists(f"{root}/{dir}/Music.xml"):
                    strdata = ""

                    with open(f"{root}/{dir}/Music.xml", "r", encoding="utf-8") as f:
                        strdata = f.read()

                    troot = ET.fromstring(strdata)

                    if root is None:
                        continue

                    name = troot.find("Name")
                    song_id = name.find("id").text
                    title = name.find("str").text
                    artist = troot.find("ArtistName").find("str").text
                    genre = troot.find("Genre").find("str").text

                    fumens = troot.find("FumenData")
                    for fumens_data in fumens.findall("FumenData"):
                        path = fumens_data.find("FumenFile").find("path").text
                        if path is None or not os.path.exists(f"{root}/{dir}/{path}"):
                            continue

                        chart_id = int(path.split(".")[0].split("_")[1])
                        level = float(
                            f"{fumens_data.find('FumenConstIntegerPart').text}.{fumens_data.find('FumenConstFractionalPart').text}"
                        )

                        await self.data.static.put_chart(
                            self.version, song_id, chart_id, title, artist, genre, level
                        )
                        self.logger.info(f"Added song {song_id} chart {chart_id}")

    async def read_reward(self, base_dir: str) -> None:
            self.logger.info(f"Reading rewards from {base_dir}...")

            for root, dirs, files in os.walk(base_dir):
                for dir in dirs:
                    if os.path.exists(f"{root}/{dir}/Reward.xml"):
                        strdata = ""

                    with open(f"{root}/{dir}/Reward.xml", "r", encoding="utf-8") as f:
                        strdata = f.read()

                    troot = ET.fromstring(strdata)

                    if root is None:
                        continue

                    name = troot.find("Name")
                    rewardId = name.find("id").text
                    rewardname = name.find("str").text
                    itemKind = OngekiConstants.REWARD_TYPES[troot.find("ItemType").text].value
                    itemId = troot.find("RewardItem").find("ItemName").find("id").text

                    await self.data.static.put_reward(self.version, rewardId, rewardname, itemKind, itemId)
                    self.logger.info(f"Added reward {rewardId}")
