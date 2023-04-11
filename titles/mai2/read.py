from decimal import Decimal
import logging
import os
import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional

from core.config import CoreConfig
from core.data import Data
from read import BaseReader
from titles.mai2.const import Mai2Constants
from titles.mai2.database import Mai2Data


class Mai2Reader(BaseReader):
    def __init__(
        self,
        config: CoreConfig,
        version: int,
        bin_dir: Optional[str],
        opt_dir: Optional[str],
        extra: Optional[str],
    ) -> None:
        super().__init__(config, version, bin_dir, opt_dir, extra)
        self.data = Mai2Data(config)

        try:
            self.logger.info(
                f"Start importer for {Mai2Constants.game_ver_to_string(version)}"
            )
        except IndexError:
            self.logger.error(f"Invalid maimai DX version {version}")
            exit(1)

    def read(self) -> None:
        data_dirs = []
        if self.bin_dir is not None:
            data_dirs += self.get_data_directories(self.bin_dir)

        if self.opt_dir is not None:
            data_dirs += self.get_data_directories(self.opt_dir)

        for dir in data_dirs:
            self.logger.info(f"Read from {dir}")
            self.get_events(f"{dir}/event")
            self.disable_events(f"{dir}/information", f"{dir}/scoreRanking")
            self.read_music(f"{dir}/music")
            self.read_tickets(f"{dir}/ticket")

    def get_events(self, base_dir: str) -> None:
        self.logger.info(f"Reading events from {base_dir}...")

        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                if os.path.exists(f"{root}/{dir}/Event.xml"):
                    with open(f"{root}/{dir}/Event.xml", encoding="utf-8") as f:
                        troot = ET.fromstring(f.read())

                        name = troot.find("name").find("str").text
                        id = int(troot.find("name").find("id").text)
                        event_type = int(troot.find("infoType").text)

                        self.data.static.put_game_event(
                            self.version, event_type, id, name
                        )
                        self.logger.info(f"Added event {id}...")

    def disable_events(
        self, base_information_dir: str, base_score_ranking_dir: str
    ) -> None:
        self.logger.info(f"Reading disabled events from {base_information_dir}...")

        for root, dirs, files in os.walk(base_information_dir):
            for dir in dirs:
                if os.path.exists(f"{root}/{dir}/Information.xml"):
                    with open(f"{root}/{dir}/Information.xml", encoding="utf-8") as f:
                        troot = ET.fromstring(f.read())

                        event_id = int(troot.find("name").find("id").text)

                        self.data.static.toggle_game_event(
                            self.version, event_id, toggle=False
                        )
                        self.logger.info(f"Disabled event {event_id}...")

        for root, dirs, files in os.walk(base_score_ranking_dir):
            for dir in dirs:
                if os.path.exists(f"{root}/{dir}/ScoreRanking.xml"):
                    with open(f"{root}/{dir}/ScoreRanking.xml", encoding="utf-8") as f:
                        troot = ET.fromstring(f.read())

                        event_id = int(troot.find("eventName").find("id").text)

                        self.data.static.toggle_game_event(
                            self.version, event_id, toggle=False
                        )
                        self.logger.info(f"Disabled event {event_id}...")

        # manually disable events wich are known to be problematic
        for event_id in [
            1,
            10,
            220311,
            220312,
            220313,
            220314,
            220315,
            220316,
            220317,
            220318,
            20121821,
            21121651,
            22091511,
            22091512,
            22091513,
            22091514,
            22091515,
            22091516,
            22091517,
            22091518,
            22091519,
        ]:
            self.data.static.toggle_game_event(self.version, event_id, toggle=False)
            self.logger.info(f"Disabled event {event_id}...")

    def read_music(self, base_dir: str) -> None:
        self.logger.info(f"Reading music from {base_dir}...")

        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                if os.path.exists(f"{root}/{dir}/Music.xml"):
                    with open(f"{root}/{dir}/Music.xml", encoding="utf-8") as f:
                        troot = ET.fromstring(f.read())

                        song_id = int(troot.find("name").find("id").text)
                        title = troot.find("name").find("str").text
                        artist = troot.find("artistName").find("str").text
                        genre = troot.find("genreName").find("str").text
                        bpm = int(troot.find("bpm").text)
                        added_ver = troot.find("AddVersion").find("str").text

                        note_data = troot.find("notesData").findall("Notes")

                        for dif in note_data:
                            path = dif.find("file").find("path").text
                            if path is not None:
                                if os.path.exists(f"{root}/{dir}/{path}"):
                                    chart_id = int(path.split(".")[0].split("_")[1])
                                    diff_num = float(
                                        f"{dif.find('level').text}.{dif.find('levelDecimal').text}"
                                    )
                                    note_designer = (
                                        dif.find("notesDesigner").find("str").text
                                    )

                                    self.data.static.put_game_music(
                                        self.version,
                                        song_id,
                                        chart_id,
                                        title,
                                        artist,
                                        genre,
                                        bpm,
                                        added_ver,
                                        diff_num,
                                        note_designer,
                                    )

                                    self.logger.info(
                                        f"Added music id {song_id} chart {chart_id}"
                                    )

    def read_tickets(self, base_dir: str) -> None:
        self.logger.info(f"Reading tickets from {base_dir}...")

        for root, dirs, files in os.walk(base_dir):
            for dir in dirs:
                if os.path.exists(f"{root}/{dir}/Ticket.xml"):
                    with open(f"{root}/{dir}/Ticket.xml", encoding="utf-8") as f:
                        troot = ET.fromstring(f.read())

                        name = troot.find("name").find("str").text
                        id = int(troot.find("name").find("id").text)
                        ticket_type = int(troot.find("ticketKind").find("id").text)
                        price = int(troot.find("creditNum").text)

                        self.data.static.put_game_ticket(
                            self.version, id, ticket_type, price, name
                        )
                        self.logger.info(f"Added ticket {id}...")
