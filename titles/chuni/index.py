from twisted.web.http import Request
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
import zlib
import yaml
import json
import inflection
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from os import path
from typing import Tuple

from core import CoreConfig, Utils
from titles.chuni.config import ChuniConfig
from titles.chuni.const import ChuniConstants
from titles.chuni.base import ChuniBase
from titles.chuni.plus import ChuniPlus
from titles.chuni.air import ChuniAir
from titles.chuni.airplus import ChuniAirPlus
from titles.chuni.star import ChuniStar
from titles.chuni.starplus import ChuniStarPlus
from titles.chuni.amazon import ChuniAmazon
from titles.chuni.amazonplus import ChuniAmazonPlus
from titles.chuni.crystal import ChuniCrystal
from titles.chuni.crystalplus import ChuniCrystalPlus
from titles.chuni.paradise import ChuniParadise
from titles.chuni.new import ChuniNew
from titles.chuni.newplus import ChuniNewPlus


class ChuniServlet:
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = ChuniConfig()
        if path.exists(f"{cfg_dir}/{ChuniConstants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{ChuniConstants.CONFIG_NAME}"))
            )

        self.versions = [
            ChuniBase(core_cfg, self.game_cfg),
            ChuniPlus(core_cfg, self.game_cfg),
            ChuniAir(core_cfg, self.game_cfg),
            ChuniAirPlus(core_cfg, self.game_cfg),
            ChuniStar(core_cfg, self.game_cfg),
            ChuniStarPlus(core_cfg, self.game_cfg),
            ChuniAmazon(core_cfg, self.game_cfg),
            ChuniAmazonPlus(core_cfg, self.game_cfg),
            ChuniCrystal(core_cfg, self.game_cfg),
            ChuniCrystalPlus(core_cfg, self.game_cfg),
            ChuniParadise(core_cfg, self.game_cfg),
            ChuniNew(core_cfg, self.game_cfg),
            ChuniNewPlus(core_cfg, self.game_cfg),
        ]

        self.logger = logging.getLogger("chuni")

        if not hasattr(self.logger, "inited"):
            log_fmt_str = "[%(asctime)s] Chunithm | %(levelname)s | %(message)s"
            log_fmt = logging.Formatter(log_fmt_str)
            fileHandler = TimedRotatingFileHandler(
                "{0}/{1}.log".format(self.core_cfg.server.log_dir, "chuni"),
                encoding="utf8",
                when="d",
                backupCount=10,
            )

            fileHandler.setFormatter(log_fmt)

            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(log_fmt)

            self.logger.addHandler(fileHandler)
            self.logger.addHandler(consoleHandler)

            self.logger.setLevel(self.game_cfg.server.loglevel)
            coloredlogs.install(
                level=self.game_cfg.server.loglevel, logger=self.logger, fmt=log_fmt_str
            )
            self.logger.inited = True

    @classmethod
    def get_allnet_info(
        cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str
    ) -> Tuple[bool, str, str]:
        game_cfg = ChuniConfig()
        if path.exists(f"{cfg_dir}/{ChuniConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{ChuniConstants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return (False, "", "")

        if core_cfg.server.is_develop:
            return (
                True,
                f"http://{core_cfg.title.hostname}:{core_cfg.title.port}/{game_code}/$v/",
                "",
            )

        return (True, f"http://{core_cfg.title.hostname}/{game_code}/$v/", "")

    def render_POST(self, request: Request, version: int, url_path: str) -> bytes:
        if url_path.lower() == "/ping":
            return zlib.compress(b'{"returnCode": "1"}')

        req_raw = request.content.getvalue()
        url_split = url_path.split("/")
        encrtped = False
        internal_ver = 0
        endpoint = url_split[len(url_split) - 1]
        client_ip = Utils.get_ip_addr(request)

        if version < 105:  # 1.0
            internal_ver = ChuniConstants.VER_CHUNITHM
        elif version >= 105 and version < 110:  # Plus
            internal_ver = ChuniConstants.VER_CHUNITHM_PLUS
        elif version >= 110 and version < 115:  # Air
            internal_ver = ChuniConstants.VER_CHUNITHM_AIR
        elif version >= 115 and version < 120:  # Air Plus
            internal_ver = ChuniConstants.VER_CHUNITHM_AIR_PLUS
        elif version >= 120 and version < 125:  # Star
            internal_ver = ChuniConstants.VER_CHUNITHM_STAR
        elif version >= 125 and version < 130:  # Star Plus
            internal_ver = ChuniConstants.VER_CHUNITHM_STAR_PLUS
        elif version >= 130 and version < 135:  # Amazon
            internal_ver = ChuniConstants.VER_CHUNITHM_AMAZON
        elif version >= 135 and version < 140:  # Amazon Plus
            internal_ver = ChuniConstants.VER_CHUNITHM_AMAZON_PLUS
        elif version >= 140 and version < 145:  # Crystal
            internal_ver = ChuniConstants.VER_CHUNITHM_CRYSTAL
        elif version >= 145 and version < 150:  # Crystal Plus
            internal_ver = ChuniConstants.VER_CHUNITHM_CRYSTAL_PLUS
        elif version >= 150 and version < 200:  # Paradise
            internal_ver = ChuniConstants.VER_CHUNITHM_PARADISE
        elif version >= 200 and version < 205:  # New
            internal_ver = ChuniConstants.VER_CHUNITHM_NEW
        elif version >= 205 and version < 210:  # New Plus
            internal_ver = ChuniConstants.VER_CHUNITHM_NEW_PLUS

        if all(c in string.hexdigits for c in endpoint) and len(endpoint) == 32:
            # If we get a 32 character long hex string, it's a hash and we're
            # doing encrypted. The likelyhood of false positives is low but
            # technically not 0
            endpoint = request.getHeader("User-Agent").split("#")[0]
            try:
                crypt = AES.new(
                    bytes.fromhex(self.game_cfg.crypto.keys[str(internal_ver)][0]),
                    AES.MODE_CBC,
                    bytes.fromhex(self.game_cfg.crypto.keys[str(internal_ver)][1]),
                )

                req_raw = crypt.decrypt(req_raw)

            except:
                self.logger.error(
                    f"Failed to decrypt v{version} request to {endpoint} -> {req_raw}"
                )
                return zlib.compress(b'{"stat": "0"}')

            encrtped = True

        if not encrtped and self.game_cfg.crypto.encrypted_only:
            self.logger.error(
                f"Unencrypted v{version} {endpoint} request, but config is set to encrypted only: {req_raw}"
            )
            return zlib.compress(b'{"stat": "0"}')

        try:
            unzip = zlib.decompress(req_raw)

        except zlib.error as e:
            self.logger.error(
                f"Failed to decompress v{version} {endpoint} request -> {e}"
            )
            return b""

        req_data = json.loads(unzip)

        self.logger.info(
            f"v{version} {endpoint} request from {client_ip}"
        )
        self.logger.debug(req_data)

        func_to_find = "handle_" + inflection.underscore(endpoint) + "_request"

        if not hasattr(self.versions[internal_ver], func_to_find):
            self.logger.warning(f"Unhandled v{version} request {endpoint}")
            resp = {"returnCode": 1}

        else:
            try:
                handler = getattr(self.versions[internal_ver], func_to_find)
                resp = handler(req_data)

            except Exception as e:
                self.logger.error(f"Error handling v{version} method {endpoint} - {e}")
                return zlib.compress(b'{"stat": "0"}')

        if resp == None:
            resp = {"returnCode": 1}

        self.logger.debug(f"Response {resp}")

        zipped = zlib.compress(json.dumps(resp, ensure_ascii=False).encode("utf-8"))

        if not encrtped:
            return zipped

        padded = pad(zipped, 16)

        crypt = AES.new(
            bytes.fromhex(self.game_cfg.crypto.keys[str(internal_ver)][0]),
            AES.MODE_CBC,
            bytes.fromhex(self.game_cfg.crypto.keys[str(internal_ver)][1]),
        )

        return crypt.encrypt(padded)
