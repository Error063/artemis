from typing import Optional
import wacky
import json
from os import walk, path

from read import BaseReader
from core.config import CoreConfig
from titles.wacca.database import WaccaData
from titles.wacca.const import WaccaConstants


class WaccaReader(BaseReader):
    def __init__(
        self,
        config: CoreConfig,
        version: int,
        bin_dir: Optional[str],
        opt_dir: Optional[str],
        extra: Optional[str],
    ) -> None:
        super().__init__(config, version, bin_dir, opt_dir, extra)
        self.data = WaccaData(config)

        try:
            self.logger.info(
                f"Start importer for {WaccaConstants.game_ver_to_string(version)}"
            )
        except IndexError:
            self.logger.error(f"Invalid wacca version {version}")
            exit(1)

    def read(self) -> None:
        if not (
            path.exists(f"{self.bin_dir}/Table")
            and path.exists(f"{self.bin_dir}/Message")
        ):
            self.logger.error("Could not find Table or Message folder, nothing to read")
            return

        self.read_music(f"{self.bin_dir}/Table", "MusicParameterTable")

    def read_music(self, base_dir: str, table: str) -> None:
        if not self.check_valid_pair(base_dir, table):
            self.logger.warning(
                f"Cannot find {table} uasset/uexp pair at {base_dir}, music will not be read"
            )
            return

        uasset = open(f"{base_dir}/{table}.uasset", "rb")
        uexp = open(f"{base_dir}/{table}.uexp", "rb")

        package = wacky.jsonify(uasset, uexp)
        package_json = json.dumps(package, indent=4, sort_keys=True)
        data = json.loads(package_json)

        first_elem = data[0]
        wacca_data = first_elem["rows"]

        for i, key in enumerate(wacca_data):
            song_id = int(key)
            title = wacca_data[str(key)]["MusicMessage"]
            artist = wacca_data[str(key)]["ArtistMessage"]
            bpm = wacca_data[str(key)]["Bpm"]
            jacket_asset_name = wacca_data[str(key)]["JacketAssetName"]

            diff = float(wacca_data[str(key)]["DifficultyNormalLv"])
            designer = wacca_data[str(key)]["NotesDesignerNormal"]

            if diff > 0:
                self.data.static.put_music(
                    self.version,
                    song_id,
                    1,
                    title,
                    artist,
                    bpm,
                    diff,
                    designer,
                    jacket_asset_name,
                )
                self.logger.info(f"Read song {song_id} chart 1")

            diff = float(wacca_data[str(key)]["DifficultyHardLv"])
            designer = wacca_data[str(key)]["NotesDesignerHard"]

            if diff > 0:
                self.data.static.put_music(
                    self.version,
                    song_id,
                    2,
                    title,
                    artist,
                    bpm,
                    diff,
                    designer,
                    jacket_asset_name,
                )
                self.logger.info(f"Read song {song_id} chart 2")

            diff = float(wacca_data[str(key)]["DifficultyExtremeLv"])
            designer = wacca_data[str(key)]["NotesDesignerExpert"]

            if diff > 0:
                self.data.static.put_music(
                    self.version,
                    song_id,
                    3,
                    title,
                    artist,
                    bpm,
                    diff,
                    designer,
                    jacket_asset_name,
                )
                self.logger.info(f"Read song {song_id} chart 3")

            diff = float(wacca_data[str(key)]["DifficultyInfernoLv"])
            designer = wacca_data[str(key)]["NotesDesignerInferno"]

            if diff > 0:
                self.data.static.put_music(
                    self.version,
                    song_id,
                    4,
                    title,
                    artist,
                    bpm,
                    diff,
                    designer,
                    jacket_asset_name,
                )
                self.logger.info(f"Read song {song_id} chart 4")

    def check_valid_pair(self, dir: str, file: str) -> bool:
        return path.exists(f"{dir}/{file}.uasset") and path.exists(f"{dir}/{file}.uexp")
