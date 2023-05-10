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
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA1
from os import path
from typing import Tuple, Dict

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
from titles.chuni.sun import ChuniSun


class ChuniServlet:
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = ChuniConfig()
        self.hash_table: Dict[Dict[str, str]] = {}
        if path.exists(f"{cfg_dir}/{ChuniConstants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{ChuniConstants.CONFIG_NAME}"))
            )

        self.versions = [
            ChuniBase,
            ChuniPlus,
            ChuniAir,
            ChuniAirPlus,
            ChuniStar,
            ChuniStarPlus,
            ChuniAmazon,
            ChuniAmazonPlus,
            ChuniCrystal,
            ChuniCrystalPlus,
            ChuniParadise,
            ChuniNew,
            ChuniNewPlus,
            ChuniSun,
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

        for version, keys in self.game_cfg.crypto.keys.items():
            if len(keys) < 3:
                continue

            self.hash_table[version] = {}

            method_list = [
                method
                for method in dir(self.versions[version])
                if not method.startswith("__")
            ]
            for method in method_list:
                method_fixed = inflection.camelize(method)[6:-7]
                # number of iterations was changed to 70 in SUN
                iter_count = 70 if version >= ChuniConstants.VER_CHUNITHM_SUN else 44
                hash = PBKDF2(
                    method_fixed,
                    bytes.fromhex(keys[2]),
                    128,
                    count=iter_count,
                    hmac_hash_module=SHA1,
                )

                hashed_name = hash.hex()[:32] # truncate unused bytes like the game does
                self.hash_table[version][hashed_name] = method_fixed

                self.logger.debug(
                    f"Hashed v{version} method {method_fixed} with {bytes.fromhex(keys[2])} to get {hash.hex()}"
                )

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
        if url_path.lower() == "ping":
            return zlib.compress(b'{"returnCode": "1"}')

        req_raw = request.content.getvalue()
        url_split = url_path.split("/")
        encrtped = False
        internal_ver = 0
        endpoint = url_split[len(url_split) - 1]
        client_ip = Utils.get_ip_addr(request)

        if version < 105:  # 1.0
            internal_ver = ChuniConstants.VER_CHUNITHM
        elif version >= 105 and version < 110:  # PLUS
            internal_ver = ChuniConstants.VER_CHUNITHM_PLUS
        elif version >= 110 and version < 115:  # AIR
            internal_ver = ChuniConstants.VER_CHUNITHM_AIR
        elif version >= 115 and version < 120:  # AIR PLUS
            internal_ver = ChuniConstants.VER_CHUNITHM_AIR_PLUS
        elif version >= 120 and version < 125:  # STAR
            internal_ver = ChuniConstants.VER_CHUNITHM_STAR
        elif version >= 125 and version < 130:  # STAR PLUS
            internal_ver = ChuniConstants.VER_CHUNITHM_STAR_PLUS
        elif version >= 130 and version < 135:  # AMAZON
            internal_ver = ChuniConstants.VER_CHUNITHM_AMAZON
        elif version >= 135 and version < 140:  # AMAZON PLUS
            internal_ver = ChuniConstants.VER_CHUNITHM_AMAZON_PLUS
        elif version >= 140 and version < 145:  # CRYSTAL
            internal_ver = ChuniConstants.VER_CHUNITHM_CRYSTAL
        elif version >= 145 and version < 150:  # CRYSTAL PLUS
            internal_ver = ChuniConstants.VER_CHUNITHM_CRYSTAL_PLUS
        elif version >= 150 and version < 200:  # PARADISE
            internal_ver = ChuniConstants.VER_CHUNITHM_PARADISE
        elif version >= 200 and version < 205:  # NEW!!
            internal_ver = ChuniConstants.VER_CHUNITHM_NEW
        elif version >= 205 and version < 210:  # NEW PLUS!!
            internal_ver = ChuniConstants.VER_CHUNITHM_NEW_PLUS
        elif version >= 210:  # SUN
            internal_ver = ChuniConstants.VER_CHUNITHM_SUN

        if all(c in string.hexdigits for c in endpoint) and len(endpoint) == 32:
            # If we get a 32 character long hex string, it's a hash and we're
            # doing encrypted. The likelyhood of false positives is low but
            # technically not 0
            if internal_ver < ChuniConstants.VER_CHUNITHM_NEW:
                endpoint = request.getHeader("User-Agent").split("#")[0]

            else:
                if internal_ver not in self.hash_table:
                    self.logger.error(
                        f"v{version} does not support encryption or no keys entered"
                    )
                    return zlib.compress(b'{"stat": "0"}')

                elif endpoint.lower() not in self.hash_table[internal_ver]:
                    self.logger.error(
                        f"No hash found for v{version} endpoint {endpoint}"
                    )
                    return zlib.compress(b'{"stat": "0"}')

                endpoint = self.hash_table[internal_ver][endpoint.lower()]

            try:
                crypt = AES.new(
                    bytes.fromhex(self.game_cfg.crypto.keys[internal_ver][0]),
                    AES.MODE_CBC,
                    bytes.fromhex(self.game_cfg.crypto.keys[internal_ver][1]),
                )

                req_raw = crypt.decrypt(req_raw)

            except Exception as e:
                self.logger.error(
                    f"Failed to decrypt v{version} request to {endpoint} -> {e}"
                )
                return zlib.compress(b'{"stat": "0"}')

            encrtped = True

        if (
            not encrtped
            and self.game_cfg.crypto.encrypted_only
            and internal_ver >= ChuniConstants.VER_CHUNITHM_CRYSTAL_PLUS
        ):
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

        self.logger.info(f"v{version} {endpoint} request from {client_ip}")
        self.logger.debug(req_data)

        func_to_find = "handle_" + inflection.underscore(endpoint) + "_request"
        handler_cls = self.versions[internal_ver](self.core_cfg, self.game_cfg)

        if not hasattr(handler_cls, func_to_find):
            self.logger.warning(f"Unhandled v{version} request {endpoint}")
            resp = {"returnCode": 1}

        else:
            try:
                handler = getattr(handler_cls, func_to_find)
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
            bytes.fromhex(self.game_cfg.crypto.keys[internal_ver][0]),
            AES.MODE_CBC,
            bytes.fromhex(self.game_cfg.crypto.keys[internal_ver][1]),
        )

        return crypt.encrypt(padded)
