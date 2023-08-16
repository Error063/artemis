from decimal import Decimal
import logging
import os
import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional
from Crypto.Cipher import AES
import zlib
import codecs

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
        if self.version >= Mai2Constants.VER_MAIMAI_DX:
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
        
        else:
            if not os.path.exists(f"{self.bin_dir}/tables"):
                self.logger.error(f"tables directory not found in {self.bin_dir}")
                return
            
            if self.version >= Mai2Constants.VER_MAIMAI_MILK:
                if self.extra is None:
                    self.logger.error("Milk - Finale requre an AES key via a hex string send as the --extra flag")
                    return
                
                key = bytes.fromhex(self.extra)
            
            else:
                key = None
            
            evt_table = self.load_table_raw(f"{self.bin_dir}/tables", "mmEvent.bin", key)
            txt_table = self.load_table_raw(f"{self.bin_dir}/tables", "mmtextout_jp.bin", key)
            score_table = self.load_table_raw(f"{self.bin_dir}/tables", "mmScore.bin", key)
            
            self.read_old_events(evt_table)
            self.read_old_music(score_table, txt_table)
            
            if self.opt_dir is not None:
                evt_table = self.load_table_raw(f"{self.opt_dir}/tables", "mmEvent.bin", key)
                txt_table = self.load_table_raw(f"{self.opt_dir}/tables", "mmtextout_jp.bin", key)
                score_table = self.load_table_raw(f"{self.opt_dir}/tables", "mmScore.bin", key)

                self.read_old_events(evt_table)
                self.read_old_music(score_table, txt_table)

            return
    
    def load_table_raw(self, dir: str, file: str, key: Optional[bytes]) -> Optional[List[Dict[str, str]]]:
        if not os.path.exists(f"{dir}/{file}"):
            self.logger.warning(f"file {file} does not exist in directory {dir}, skipping")
            return
        
        self.logger.info(f"Load table {file} from {dir}")
        if key is not None:
            cipher = AES.new(key, AES.MODE_CBC)
            with open(f"{dir}/{file}", "rb") as f:
                f_encrypted = f.read()
                f_data = cipher.decrypt(f_encrypted)[0x10:]
        
        else:
            with open(f"{dir}/{file}", "rb") as f:
                f_data = f.read()[0x10:]
        
        if f_data is None or not f_data:
            self.logger.warning(f"file {dir} could not be read, skipping")
            return
        
        f_data_deflate = zlib.decompress(f_data, wbits = zlib.MAX_WBITS | 16)[0x12:] # lop off the junk at the beginning
        f_decoded = codecs.utf_16_le_decode(f_data_deflate)[0]
        f_split = f_decoded.splitlines()

        has_struct_def = "struct " in f_decoded
        is_struct = False
        struct_def = []
        tbl_content = []

        if has_struct_def:
            for x in f_split:
                if x.startswith("struct "):
                    is_struct = True
                    struct_name = x[7:-1]
                    continue
                
                if x.startswith("};"):
                    is_struct = False
                    break

                if is_struct:
                    try:
                        struct_def.append(x[x.rindex("  ") + 2: -1])
                    except ValueError:
                        self.logger.warning(f"rindex failed on line {x}")
            
            if is_struct:
                self.logger.warning("Struct not formatted properly")
            
            if not struct_def:
                self.logger.warning("Struct def not found")
                    
        name = file[:file.index(".")]
        if "_" in name:
            name = name[:file.index("_")]
        
        for x in f_split:
            if not x.startswith(name.upper()):
                continue
            
            line_match = re.match(r"(\w+)\((.*?)\)([ ]+\/{3}<[ ]+(.*))?", x)
            if line_match is None:
                continue

            if not line_match.group(1) == name.upper():
                self.logger.warning(f"Strange regex match for line {x} -> {line_match}")
                continue
            
            vals = line_match.group(2)
            comment = line_match.group(4)
            line_dict = {}
            
            vals_split = vals.split(",")
            for y in range(len(vals_split)):
                stripped = vals_split[y].strip().lstrip("L\"").lstrip("\"").rstrip("\"")
                if not stripped or stripped is None:
                    continue

                if has_struct_def and len(struct_def) > y:
                    line_dict[struct_def[y]] = stripped
                
                else:
                    line_dict[f'item_{y}'] = stripped
            
            if comment:
                line_dict['comment'] = comment
            
            tbl_content.append(line_dict)

        if tbl_content:
            return tbl_content
        
        else:
            self.logger.warning("Failed load table content, skipping")
            return

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

    def read_old_events(self, events: Optional[List[Dict[str, str]]]) -> None:
        if events is None:
            return
        
        for event in events:
            evt_id = int(event.get('イベントID', '0'))
            evt_expire_time = float(event.get('オフ時強制時期', '0.0'))
            is_exp = bool(int(event.get('海外許可', '0')))
            is_aou = bool(int(event.get('AOU許可', '0')))
            name = event.get('comment', f'evt_{evt_id}')

            self.data.static.put_game_event(self.version, 0, evt_id, name)
            
            if not (is_exp or is_aou):
                self.data.static.toggle_game_event(self.version, evt_id, False)
    
    def read_old_music(self, scores: Optional[List[Dict[str, str]]], text: Optional[List[Dict[str, str]]]) -> None:
        if scores is None or text is None:
            return
        # TODO
