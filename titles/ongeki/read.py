from decimal import Decimal
import logging
import os
import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional

from read import BaseReader
from core.config import CoreConfig
from titles.ongeki.database import OngekiData
from titles.ongeki.const import OngekiConstants
from titles.ongeki.config import OngekiConfig

class OngekiReader(BaseReader):
    def __init__(self, config: CoreConfig, version: int, bin_dir: Optional[str], opt_dir: Optional[str], extra: Optional[str]) -> None:
        super().__init__(config, version, bin_dir, opt_dir, extra)
        self.data = OngekiData(config)

        try:
            self.logger.info(f"Start importer for {OngekiConstants.game_ver_to_string(version)}")
        except IndexError:
            self.logger.error(f"Invalid ongeki version {version}")
            exit(1)
    
    def read(self) -> None:
        data_dirs = []
        if self.bin_dir is not None:
            data_dirs += self.get_data_directories(self.bin_dir)
        
        if self.opt_dir is not None:
            data_dirs += self.get_data_directories(self.opt_dir)
        
        for dir in data_dirs:
            self.read_events(f"{dir}/event")
            self.read_music(f"{dir}/music")
    
    def read_events(self, base_dir: str) -> None:
        self.logger.info(f"Reading events from {base_dir}...")

        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                if os.path.exists(f"{root}/{dir}/Event.xml"):
                    with open(f"{root}/{dir}/Event.xml", "r", encoding="utf-8") as f:
                        troot = ET.fromstring(f.read())

                        name = troot.find('Name').find('str').text
                        id = int(troot.find('Name').find('id').text)
                        event_type = OngekiConstants.EVT_TYPES[troot.find('EventType').text].value
                        

                        self.data.static.put_event(self.version, id, event_type, name)
                        self.logger.info(f"Added event {id}")
    
    def read_music(self, base_dir: str) -> None:
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

                    name = troot.find('Name')
                    song_id = name.find('id').text
                    title = name.find('str').text
                    artist = troot.find('ArtistName').find('str').text
                    genre = troot.find('Genre').find('str').text
                    
                    fumens = troot.find("FumenData")
                    for fumens_data in fumens.findall('FumenData'):                        
                        path = fumens_data.find('FumenFile').find('path').text
                        if path is None or not os.path.exists(f"{root}/{dir}/{path}"):
                            continue

                        chart_id = int(path.split(".")[0].split("_")[1])
                        level = float(
                            f"{fumens_data.find('FumenConstIntegerPart').text}.{fumens_data.find('FumenConstFractionalPart').text}"
                            )
                        
                        self.data.static.put_chart(self.version, song_id, chart_id, title, artist, genre, level)
                        self.logger.info(f"Added song {song_id} chart {chart_id}")

