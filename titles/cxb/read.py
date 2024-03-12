from typing import Optional
from os import path
import csv

from read import BaseReader
from core.config import CoreConfig
from titles.cxb.database import CxbData
from titles.cxb.const import CxbConstants

class CxbReader(BaseReader):
    def __init__(
        self,
        config: CoreConfig,
        version: int,
        bin_arg: Optional[str],
        opt_arg: Optional[str],
        extra: Optional[str],
    ) -> None:
        super().__init__(config, version, bin_arg, opt_arg, extra)
        self.data = CxbData(config)

        try:
            self.logger.info(
                f"Start importer for {CxbConstants.game_ver_to_string(version)}"
            )
        except IndexError:
            self.logger.error(f"Invalid project cxb version {version}")
            exit(1)

    async def read(self) -> None:
        if path.exists(self.bin_dir):
            await self.read_csv(self.bin_dir)
        
        else:
            self.logger.warn(f"{self.bin_dir} does not exist, nothing to import")

    async def read_csv(self, bin_dir: str) -> None:
        self.logger.info(f"Read csv from {bin_dir}")

        try:
            fullPath = bin_dir + "/export.csv"
            with open(fullPath, encoding="UTF-8") as fp:
                reader = csv.DictReader(fp)
                for row in reader:
                    song_id = row["mcode"]
                    index = row["index"]
                    title = row["name"]
                    artist = row["artist"]
                    genre = row["category"]

                    if not "N/A" in row["standard"]:
                        self.logger.info(f"Added song {song_id} chart 0")
                        await self.data.static.put_music(
                            self.version,
                            song_id,
                            index,
                            0,
                            title,
                            artist,
                            genre,
                            int(
                                row["standard"]
                                .replace("Standard ", "")
                                .replace("N/A", "0")
                            ),
                        )
                    if not "N/A" in row["hard"]:
                        self.logger.info(f"Added song {song_id} chart 1")
                        await self.data.static.put_music(
                            self.version,
                            song_id,
                            index,
                            1,
                            title,
                            artist,
                            genre,
                            int(row["hard"].replace("Hard ", "").replace("N/A", "0")),
                        )
                    if not "N/A" in row["master"]:
                        self.logger.info(f"Added song {song_id} chart 2")
                        await self.data.static.put_music(
                            self.version,
                            song_id,
                            index,
                            2,
                            title,
                            artist,
                            genre,
                            int(
                                row["master"].replace("Master ", "").replace("N/A", "0")
                            ),
                        )
                    if not "N/A" in row["unlimited"]:
                        self.logger.info(f"Added song {song_id} chart 3")
                        await self.data.static.put_music(
                            self.version,
                            song_id,
                            index,
                            3,
                            title,
                            artist,
                            genre,
                            int(
                                row["unlimited"]
                                .replace("Unlimited ", "")
                                .replace("N/A", "0")
                            ),
                        )
                    if not "N/A" in row["easy"]:
                        self.logger.info(f"Added song {song_id} chart 4")
                        await self.data.static.put_music(
                            self.version,
                            song_id,
                            index,
                            4,
                            title,
                            artist,
                            genre,
                            int(row["easy"].replace("Easy ", "").replace("N/A", "0")),
                        )
        except Exception:
            self.logger.warning(f"Couldn't read csv file in {self.bin_dir}, skipping")
