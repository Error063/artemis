from twisted.web.http import Request
import json
import inflection
import yaml
import string
import logging
import coloredlogs
import zlib
from logging.handlers import TimedRotatingFileHandler
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA1
from os import path
from typing import Tuple

from core.config import CoreConfig
from core.utils import Utils
from titles.ongeki.config import OngekiConfig
from titles.ongeki.const import OngekiConstants
from titles.ongeki.base import OngekiBase
from titles.ongeki.plus import OngekiPlus
from titles.ongeki.summer import OngekiSummer
from titles.ongeki.summerplus import OngekiSummerPlus
from titles.ongeki.red import OngekiRed
from titles.ongeki.redplus import OngekiRedPlus
from titles.ongeki.bright import OngekiBright
from titles.ongeki.brightmemory import OngekiBrightMemory


class OngekiServlet:
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = OngekiConfig()
        self.hash_table: Dict[Dict[str, str]] = {}
        if path.exists(f"{cfg_dir}/{OngekiConstants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{OngekiConstants.CONFIG_NAME}"))
            )

        self.versions = [
            OngekiBase(core_cfg, self.game_cfg),
            OngekiPlus(core_cfg, self.game_cfg),
            OngekiSummer(core_cfg, self.game_cfg),
            OngekiSummerPlus(core_cfg, self.game_cfg),
            OngekiRed(core_cfg, self.game_cfg),
            OngekiRedPlus(core_cfg, self.game_cfg),
            OngekiBright(core_cfg, self.game_cfg),
            OngekiBrightMemory(core_cfg, self.game_cfg),
        ]

        self.logger = logging.getLogger("ongeki")

        if not hasattr(self.logger, "inited"):
            log_fmt_str = "[%(asctime)s] Ongeki | %(levelname)s | %(message)s"
            log_fmt = logging.Formatter(log_fmt_str)
            fileHandler = TimedRotatingFileHandler(
                "{0}/{1}.log".format(self.core_cfg.server.log_dir, "ongeki"),
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
                # number of iterations is 64 on Bright Memory
                iter_count = 64
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
                    f"Hashed v{version} method {method_fixed} with {bytes.fromhex(keys[2])} to get {hash.hex()[:32]}"
                )

    @classmethod
    def get_allnet_info(
        cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str
    ) -> Tuple[bool, str, str]:
        game_cfg = OngekiConfig()

        if path.exists(f"{cfg_dir}/{OngekiConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{OngekiConstants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return (False, "", "")

        if core_cfg.server.is_develop:
            return (
                True,
                f"http://{core_cfg.title.hostname}:{core_cfg.title.port}/{game_code}/$v/",
                f"{core_cfg.title.hostname}:{core_cfg.title.port}/",
            )

        return (
            True,
            f"http://{core_cfg.title.hostname}/{game_code}/$v/",
            f"{core_cfg.title.hostname}/",
        )

    def render_POST(self, request: Request, version: int, url_path: str) -> bytes:
        if url_path.lower() == "ping":
            return zlib.compress(b'{"returnCode": 1}')

        req_raw = request.content.getvalue()
        url_split = url_path.split("/")
        encrtped = False
        internal_ver = 0
        endpoint = url_split[len(url_split) - 1]
        client_ip = Utils.get_ip_addr(request)

        if version < 105:  # 1.0
            internal_ver = OngekiConstants.VER_ONGEKI
        elif version >= 105 and version < 110:  # Plus
            internal_ver = OngekiConstants.VER_ONGEKI_PLUS
        elif version >= 110 and version < 115:  # Summer
            internal_ver = OngekiConstants.VER_ONGEKI_SUMMER
        elif version >= 115 and version < 120:  # Summer Plus
            internal_ver = OngekiConstants.VER_ONGEKI_SUMMER_PLUS
        elif version >= 120 and version < 125:  # Red
            internal_ver = OngekiConstants.VER_ONGEKI_RED
        elif version >= 125 and version < 130:  # Red Plus
            internal_ver = OngekiConstants.VER_ONGEKI_RED_PLUS
        elif version >= 130 and version < 135:  # Bright
            internal_ver = OngekiConstants.VER_ONGEKI_BRIGHT
        elif version >= 135 and version < 140:  # Bright Memory
            internal_ver = OngekiConstants.VER_ONGEKI_BRIGHT_MEMORY

        if all(c in string.hexdigits for c in endpoint) and len(endpoint) == 32:
            # If we get a 32 character long hex string, it's a hash and we're
            # doing encrypted. The likelyhood of false positives is low but
            # technically not 0
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
            return zlib.compress(b'{"stat": "0"}')

        req_data = json.loads(unzip)

        self.logger.info(
            f"v{version} {endpoint} request from {client_ip}"
        )
        self.logger.debug(req_data)

        func_to_find = "handle_" + inflection.underscore(endpoint) + "_request"

        if not hasattr(self.versions[internal_ver], func_to_find):
            self.logger.warning(f"Unhandled v{version} request {endpoint}")
            return zlib.compress(b'{"returnCode": 1}')

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
            bytes.fromhex(self.game_cfg.crypto.keys[internal_ver][0]),
            AES.MODE_CBC,
            bytes.fromhex(self.game_cfg.crypto.keys[internal_ver][1]),
        )

        return crypt.encrypt(padded)