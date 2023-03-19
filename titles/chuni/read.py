from typing import Optional
from os import walk, path
import xml.etree.ElementTree as ET
from read import BaseReader

from core.config import CoreConfig
from titles.chuni.database import ChuniData
from titles.chuni.const import ChuniConstants


class ChuniReader(BaseReader):
    def __init__(
        self,
        config: CoreConfig,
        version: int,
        bin_dir: Optional[str],
        opt_dir: Optional[str],
        extra: Optional[str],
    ) -> None:
        super().__init__(config, version, bin_dir, opt_dir, extra)
        self.data = ChuniData(config)

        try:
            self.logger.info(
                f"Start importer for {ChuniConstants.game_ver_to_string(version)}"
            )
        except IndexError:
            self.logger.error(f"Invalid chunithm version {version}")
            exit(1)

    def read(self) -> None:
        data_dirs = []
        if self.bin_dir is not None:
            data_dirs += self.get_data_directories(self.bin_dir)

        if self.opt_dir is not None:
            data_dirs += self.get_data_directories(self.opt_dir)

        for dir in data_dirs:
            self.logger.info(f"Read from {dir}")
            self.read_events(f"{dir}/event")
            self.read_music(f"{dir}/music")
            self.read_charges(f"{dir}/chargeItem")
            self.read_avatar(f"{dir}/avatarAccessory")

    def read_events(self, evt_dir: str) -> None:
        for root, dirs, files in walk(evt_dir):
            for dir in dirs:
                if path.exists(f"{root}/{dir}/Event.xml"):
                    with open(f"{root}/{dir}/Event.xml", "rb") as fp:
                        bytedata = fp.read()
                        strdata = bytedata.decode("UTF-8")

                    xml_root = ET.fromstring(strdata)
                    for name in xml_root.findall("name"):
                        id = name.find("id").text
                        name = name.find("str").text
                    for substances in xml_root.findall("substances"):
                        event_type = substances.find("type").text

                    result = self.data.static.put_event(
                        self.version, id, event_type, name
                    )
                    if result is not None:
                        self.logger.info(f"Inserted event {id}")
                    else:
                        self.logger.warn(f"Failed to insert event {id}")

    def read_music(self, music_dir: str) -> None:
        for root, dirs, files in walk(music_dir):
            for dir in dirs:
                if path.exists(f"{root}/{dir}/Music.xml"):
                    with open(f"{root}/{dir}/Music.xml", "rb") as fp:
                        bytedata = fp.read()
                        strdata = bytedata.decode("UTF-8")

                    xml_root = ET.fromstring(strdata)
                    for name in xml_root.findall("name"):
                        song_id = name.find("id").text
                        title = name.find("str").text

                    for artistName in xml_root.findall("artistName"):
                        artist = artistName.find("str").text

                    for genreNames in xml_root.findall("genreNames"):
                        for list_ in genreNames.findall("list"):
                            for StringID in list_.findall("StringID"):
                                genre = StringID.find("str").text

                    for jaketFile in xml_root.findall("jaketFile"):  # nice typo, SEGA
                        jacket_path = jaketFile.find("path").text

                    for fumens in xml_root.findall("fumens"):
                        for MusicFumenData in fumens.findall("MusicFumenData"):
                            fumen_path = MusicFumenData.find("file").find("path")

                            if fumen_path is not None:
                                chart_id = MusicFumenData.find("type").find("id").text
                                if chart_id == "4":
                                    level = float(xml_root.find("starDifType").text)
                                    we_chara = (
                                        xml_root.find("worldsEndTagName")
                                        .find("str")
                                        .text
                                    )
                                else:
                                    level = float(
                                        f"{MusicFumenData.find('level').text}.{MusicFumenData.find('levelDecimal').text}"
                                    )
                                    we_chara = None

                                result = self.data.static.put_music(
                                    self.version,
                                    song_id,
                                    chart_id,
                                    title,
                                    artist,
                                    level,
                                    genre,
                                    jacket_path,
                                    we_chara,
                                )

                                if result is not None:
                                    self.logger.info(
                                        f"Inserted music {song_id} chart {chart_id}"
                                    )
                                else:
                                    self.logger.warn(
                                        f"Failed to insert music {song_id} chart {chart_id}"
                                    )

    def read_charges(self, charge_dir: str) -> None:
        for root, dirs, files in walk(charge_dir):
            for dir in dirs:
                if path.exists(f"{root}/{dir}/ChargeItem.xml"):
                    with open(f"{root}/{dir}/ChargeItem.xml", "rb") as fp:
                        bytedata = fp.read()
                        strdata = bytedata.decode("UTF-8")

                    xml_root = ET.fromstring(strdata)
                    for name in xml_root.findall("name"):
                        id = name.find("id").text
                        name = name.find("str").text
                    expirationDays = xml_root.find("expirationDays").text
                    consumeType = xml_root.find("consumeType").text
                    sellingAppeal = bool(xml_root.find("sellingAppeal").text)

                    result = self.data.static.put_charge(
                        self.version,
                        id,
                        name,
                        expirationDays,
                        consumeType,
                        sellingAppeal,
                    )

                    if result is not None:
                        self.logger.info(f"Inserted charge {id}")
                    else:
                        self.logger.warn(f"Failed to insert charge {id}")

    def read_avatar(self, avatar_dir: str) -> None:
        for root, dirs, files in walk(avatar_dir):
            for dir in dirs:
                if path.exists(f"{root}/{dir}/AvatarAccessory.xml"):
                    with open(f"{root}/{dir}/AvatarAccessory.xml", "rb") as fp:
                        bytedata = fp.read()
                        strdata = bytedata.decode("UTF-8")

                    xml_root = ET.fromstring(strdata)
                    for name in xml_root.findall("name"):
                        id = name.find("id").text
                        name = name.find("str").text
                    category = xml_root.find("category").text
                    for image in xml_root.findall("image"):
                        iconPath = image.find("path").text
                    for texture in xml_root.findall("texture"):
                        texturePath = texture.find("path").text

                    result = self.data.static.put_avatar(
                        self.version, id, name, category, iconPath, texturePath
                    )

                    if result is not None:
                        self.logger.info(f"Inserted avatarAccessory {id}")
                    else:
                        self.logger.warn(f"Failed to insert avatarAccessory {id}")
