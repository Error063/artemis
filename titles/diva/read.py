from typing import Optional, Dict, List
from os import walk, path
import urllib

from read import BaseReader
from core.config import CoreConfig
from titles.diva.database import DivaData
from titles.diva.const import DivaConstants


class DivaReader(BaseReader):
    def __init__(
        self,
        config: CoreConfig,
        version: int,
        bin_dir: Optional[str],
        opt_dir: Optional[str],
        extra: Optional[str],
    ) -> None:
        super().__init__(config, version, bin_dir, opt_dir, extra)
        self.data = DivaData(config)

        try:
            self.logger.info(
                f"Start importer for {DivaConstants.game_ver_to_string(version)}"
            )
        except IndexError:
            self.logger.error(f"Invalid project diva version {version}")
            exit(1)

    def read(self) -> None:
        pull_bin_ram = True
        pull_bin_rom = True
        pull_opt_rom = True

        if not path.exists(f"{self.bin_dir}/ram"):
            self.logger.warning(f"Couldn't find ram folder in {self.bin_dir}, skipping")
            pull_bin_ram = False

        if not path.exists(f"{self.bin_dir}/rom"):
            self.logger.warning(f"Couldn't find rom folder in {self.bin_dir}, skipping")
            pull_bin_rom = False

        if self.opt_dir is not None:
            opt_dirs = self.get_data_directories(self.opt_dir)
        else:
            pull_opt_rom = False
            self.logger.warning("No option directory specified, skipping")

        if pull_bin_ram:
            self.read_ram(f"{self.bin_dir}/ram")
        if pull_bin_rom:
            self.read_rom(f"{self.bin_dir}/rom")
        if pull_opt_rom:
            for dir in opt_dirs:
                self.read_rom(f"{dir}/rom")

    def read_ram(self, ram_root_dir: str) -> None:
        self.logger.info(f"Read RAM from {ram_root_dir}")

        if path.exists(f"{ram_root_dir}/databank"):
            for root, dirs, files in walk(f"{ram_root_dir}/databank"):
                for file in files:
                    if (
                        file.startswith("ShopCatalog_")
                        or file.startswith("CustomizeItemCatalog_")
                        or (
                            file.startswith("QuestInfo")
                            and not file.startswith("QuestInfoTm")
                        )
                    ):
                        with open(f"{root}/{file}", "r") as f:
                            file_data: str = urllib.parse.unquote(
                                urllib.parse.unquote(f.read())
                            )
                            if file_data == "***":
                                self.logger.info(f"{file} is empty, skipping")
                                continue

                            file_lines: List[str] = file_data.split("\n")

                            for line in file_lines:
                                split = line.split(",")

                                if not split[0]:
                                    split.pop(0)

                                if file.startswith("ShopCatalog_"):
                                    for x in range(0, len(split), 7):
                                        self.logger.info(
                                            f"Added shop item {split[x+0]}"
                                        )

                                        self.data.static.put_shop(
                                            self.version,
                                            split[x + 0],
                                            split[x + 2],
                                            split[x + 6],
                                            split[x + 3],
                                            split[x + 1],
                                            split[x + 4],
                                            split[x + 5],
                                        )

                                elif (
                                    file.startswith("CustomizeItemCatalog_")
                                    and len(split) >= 7
                                ):
                                    for x in range(0, len(split), 7):
                                        self.logger.info(f"Added item {split[x+0]}")

                                        self.data.static.put_items(
                                            self.version,
                                            split[x + 0],
                                            split[x + 2],
                                            split[x + 6],
                                            split[x + 3],
                                            split[x + 1],
                                            split[x + 4],
                                            split[x + 5],
                                        )

                                elif file.startswith("QuestInfo") and len(split) >= 9:
                                    self.logger.info(f"Added quest {split[0]}")

                                    self.data.static.put_quests(
                                        self.version,
                                        split[0],
                                        split[6],
                                        split[2],
                                        split[3],
                                        split[7],
                                        split[8],
                                        split[1],
                                        split[4],
                                        split[5],
                                    )

                                else:
                                    continue
        else:
            self.logger.warning(f"Databank folder not found in {ram_root_dir}, skipping")

    def read_rom(self, rom_root_dir: str) -> None:
        self.logger.info(f"Read ROM from {rom_root_dir}")
        pv_list: Dict[str, Dict] = {}

        if path.exists(f"{rom_root_dir}/mdata_pv_db.txt"):
            file_path = f"{rom_root_dir}/mdata_pv_db.txt"
        elif path.exists(f"{rom_root_dir}/pv_db.txt"):
            file_path = f"{rom_root_dir}/pv_db.txt"
        else:
            self.logger.warning(
                f"Cannot find pv_db.txt or mdata_pv_db.txt in {rom_root_dir}, skipping"
            )
            return

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if line.startswith("#") or not line:
                    continue

                line_split = line.split("=")
                if len(line_split) != 2:
                    continue

                key = line_split[0]
                val = line_split[1]
                if val.endswith("\n"):
                    val = val[:-1]

                key_split = key.split(".")
                pv_id = key_split[0]
                key_args = []

                for x in range(1, len(key_split)):
                    key_args.append(key_split[x])

                try:
                    pv_list[pv_id] = self.add_branch(pv_list[pv_id], key_args, val)
                except KeyError:
                    pv_list[pv_id] = {}
                    pv_list[pv_id] = self.add_branch(pv_list[pv_id], key_args, val)

        for pv_id, pv_data in pv_list.items():
            song_id = int(pv_id.split("_")[1])
            if "songinfo" not in pv_data:
                continue
            if "illustrator" not in pv_data["songinfo"]:
                pv_data["songinfo"]["illustrator"] = "-"
            if "arranger" not in pv_data["songinfo"]:
                pv_data["songinfo"]["arranger"] = "-"
            if "lyrics" not in pv_data["songinfo"]:
                pv_data["songinfo"]["lyrics"] = "-"
            if "music" not in pv_data["songinfo"]:
                pv_data["songinfo"]["music"] = "-"

            if "easy" in pv_data["difficulty"] and "0" in pv_data["difficulty"]["easy"]:
                diff = pv_data["difficulty"]["easy"]["0"]["level"].split("_")
                self.logger.info(f"Added song {song_id} chart 0")

                self.data.static.put_music(
                    self.version,
                    song_id,
                    0,
                    pv_data["song_name"],
                    pv_data["songinfo"]["arranger"],
                    pv_data["songinfo"]["illustrator"],
                    pv_data["songinfo"]["lyrics"],
                    pv_data["songinfo"]["music"],
                    float(f"{diff[2]}.{diff[3]}"),
                    pv_data["bpm"],
                    pv_data["date"],
                )

            if (
                "normal" in pv_data["difficulty"]
                and "0" in pv_data["difficulty"]["normal"]
            ):
                diff = pv_data["difficulty"]["normal"]["0"]["level"].split("_")
                self.logger.info(f"Added song {song_id} chart 1")

                self.data.static.put_music(
                    self.version,
                    song_id,
                    1,
                    pv_data["song_name"],
                    pv_data["songinfo"]["arranger"],
                    pv_data["songinfo"]["illustrator"],
                    pv_data["songinfo"]["lyrics"],
                    pv_data["songinfo"]["music"],
                    float(f"{diff[2]}.{diff[3]}"),
                    pv_data["bpm"],
                    pv_data["date"],
                )

            if "hard" in pv_data["difficulty"] and "0" in pv_data["difficulty"]["hard"]:
                diff = pv_data["difficulty"]["hard"]["0"]["level"].split("_")
                self.logger.info(f"Added song {song_id} chart 2")

                self.data.static.put_music(
                    self.version,
                    song_id,
                    2,
                    pv_data["song_name"],
                    pv_data["songinfo"]["arranger"],
                    pv_data["songinfo"]["illustrator"],
                    pv_data["songinfo"]["lyrics"],
                    pv_data["songinfo"]["music"],
                    float(f"{diff[2]}.{diff[3]}"),
                    pv_data["bpm"],
                    pv_data["date"],
                )

            if "extreme" in pv_data["difficulty"]:
                if "0" in pv_data["difficulty"]["extreme"]:
                    diff = pv_data["difficulty"]["extreme"]["0"]["level"].split("_")
                    self.logger.info(f"Added song {song_id} chart 3")

                    self.data.static.put_music(
                        self.version,
                        song_id,
                        3,
                        pv_data["song_name"],
                        pv_data["songinfo"]["arranger"],
                        pv_data["songinfo"]["illustrator"],
                        pv_data["songinfo"]["lyrics"],
                        pv_data["songinfo"]["music"],
                        float(f"{diff[2]}.{diff[3]}"),
                        pv_data["bpm"],
                        pv_data["date"],
                    )

                if "1" in pv_data["difficulty"]["extreme"]:
                    diff = pv_data["difficulty"]["extreme"]["1"]["level"].split("_")
                    self.logger.info(f"Added song {song_id} chart 4")

                    self.data.static.put_music(
                        self.version,
                        song_id,
                        4,
                        pv_data["song_name"],
                        pv_data["songinfo"]["arranger"],
                        pv_data["songinfo"]["illustrator"],
                        pv_data["songinfo"]["lyrics"],
                        pv_data["songinfo"]["music"],
                        float(f"{diff[2]}.{diff[3]}"),
                        pv_data["bpm"],
                        pv_data["date"],
                    )

    def add_branch(self, tree: Dict, vector: List, value: str):
        """
        Recursivly adds nodes to a dictionary
        Author: iJames on StackOverflow
        """
        key = vector[0]
        tree[key] = (
            value
            if len(vector) == 1
            else self.add_branch(tree.get(key, {}), vector[1:], value)
        )
        return tree
