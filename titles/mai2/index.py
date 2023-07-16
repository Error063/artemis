from twisted.web.http import Request
from twisted.web.server import NOT_DONE_YET
import json
import inflection
import yaml
import string
import logging, coloredlogs
import zlib
from logging.handlers import TimedRotatingFileHandler
from os import path, mkdir
from typing import Tuple

from core.config import CoreConfig
from core.utils import Utils
from titles.mai2.config import Mai2Config
from titles.mai2.const import Mai2Constants
from titles.mai2.base import Mai2Base
from titles.mai2.finale import Mai2Finale
from titles.mai2.dx import Mai2DX
from titles.mai2.dxplus import Mai2DXPlus
from titles.mai2.splash import Mai2Splash
from titles.mai2.splashplus import Mai2SplashPlus
from titles.mai2.universe import Mai2Universe
from titles.mai2.universeplus import Mai2UniversePlus
from titles.mai2.festival import Mai2Festival


class Mai2Servlet:
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = Mai2Config()
        if path.exists(f"{cfg_dir}/{Mai2Constants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{Mai2Constants.CONFIG_NAME}"))
            )

        self.versions = [
            Mai2Base,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            Mai2Finale,            
            Mai2DX,
            Mai2DXPlus,
            Mai2Splash,
            Mai2SplashPlus,
            Mai2Universe,
            Mai2UniversePlus,
            Mai2Festival,
        ]

        self.logger = logging.getLogger("mai2")
        if not hasattr(self.logger, "initted"):
            log_fmt_str = "[%(asctime)s] Mai2 | %(levelname)s | %(message)s"
            log_fmt = logging.Formatter(log_fmt_str)
            fileHandler = TimedRotatingFileHandler(
                "{0}/{1}.log".format(self.core_cfg.server.log_dir, "mai2"),
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
            self.logger.initted = True

    @classmethod
    def get_allnet_info(
        cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str
    ) -> Tuple[bool, str, str]:
        game_cfg = Mai2Config()

        if path.exists(f"{cfg_dir}/{Mai2Constants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{Mai2Constants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return (False, "", "")

        if core_cfg.server.is_develop:
            return (
                True,
                f"http://{core_cfg.title.hostname}:{core_cfg.title.port}/{game_code}/$v/",
                f"{core_cfg.title.hostname}",
            )

        return (
            True,
            f"http://{core_cfg.title.hostname}/{game_code}/$v/",
            f"{core_cfg.title.hostname}",
        )

    def setup(self):
        if self.game_cfg.uploads.photos and self.game_cfg.uploads.photos_dir and not path.exists(self.game_cfg.uploads.photos_dir):
            try:
                mkdir(self.game_cfg.uploads.photos_dir)
            except:
                self.logger.error(f"Failed to make photo upload directory at {self.game_cfg.uploads.photos_dir}")

        if self.game_cfg.uploads.movies and self.game_cfg.uploads.movies_dir and not path.exists(self.game_cfg.uploads.movies_dir):
            try:
                mkdir(self.game_cfg.uploads.movies_dir)
            except:
                self.logger.error(f"Failed to make movie upload directory at {self.game_cfg.uploads.movies_dir}")

    def render_POST(self, request: Request, version: int, url_path: str) -> bytes:
        if url_path.lower() == "ping":
            return zlib.compress(b'{"returnCode": "1"}')
        
        elif url_path.startswith("api/movie/"):
            self.logger.info(f"Movie data: {url_path} - {request.content.getvalue()}")
            return b""

        req_raw = request.content.getvalue()
        url = request.uri.decode()
        url_split = url_path.split("/")
        internal_ver = 0
        endpoint = url_split[len(url_split) - 1]
        client_ip = Utils.get_ip_addr(request)

        if request.uri.startswith(b"/SDEZ"):
            if version < 105:  # 1.0
                internal_ver = Mai2Constants.VER_MAIMAI_DX
            elif version >= 105 and version < 110:  # Plus
                internal_ver = Mai2Constants.VER_MAIMAI_DX_PLUS
            elif version >= 110 and version < 115:  # Splash
                internal_ver = Mai2Constants.VER_MAIMAI_DX_SPLASH
            elif version >= 115 and version < 120:  # Splash Plus
                internal_ver = Mai2Constants.VER_MAIMAI_DX_SPLASH_PLUS
            elif version >= 120 and version < 125:  # Universe
                internal_ver = Mai2Constants.VER_MAIMAI_DX_UNIVERSE
            elif version >= 125 and version < 130:  # Universe Plus
                internal_ver = Mai2Constants.VER_MAIMAI_DX_UNIVERSE_PLUS
            elif version >= 130:  # Festival
                internal_ver = Mai2Constants.VER_MAIMAI_DX_FESTIVAL

        else:
            if version < 110:  # 1.0
                internal_ver = Mai2Constants.VER_MAIMAI
            elif version >= 110 and version < 120:  # Plus
                internal_ver = Mai2Constants.VER_MAIMAI_PLUS
            elif version >= 120 and version < 130:  # Green
                internal_ver = Mai2Constants.VER_MAIMAI_GREEN
            elif version >= 130 and version < 140:  # Green Plus
                internal_ver = Mai2Constants.VER_MAIMAI_GREEN_PLUS
            elif version >= 140 and version < 150:  # Orange
                internal_ver = Mai2Constants.VER_MAIMAI_ORANGE
            elif version >= 150 and version < 160:  # Orange Plus
                internal_ver = Mai2Constants.VER_MAIMAI_ORANGE_PLUS
            elif version >= 160 and version < 170:  # Pink
                internal_ver = Mai2Constants.VER_MAIMAI_PINK
            elif version >= 170 and version < 180:  # Pink Plus
                internal_ver = Mai2Constants.VER_MAIMAI_PINK_PLUS
            elif version >= 180 and version < 185:  # Murasaki
                internal_ver = Mai2Constants.VER_MAIMAI_MURASAKI
            elif version >= 185 and version < 190:  # Murasaki Plus
                internal_ver = Mai2Constants.VER_MAIMAI_MURASAKI_PLUS
            elif version >= 190 and version < 195:  # Milk
                internal_ver = Mai2Constants.VER_MAIMAI_MILK
            elif version >= 195 and version < 197:  # Milk Plus
                internal_ver = Mai2Constants.VER_MAIMAI_MILK_PLUS
            elif version >= 197:  # Finale
                internal_ver = Mai2Constants.VER_MAIMAI_FINALE
        
        if all(c in string.hexdigits for c in endpoint) and len(endpoint) == 32:
            # If we get a 32 character long hex string, it's a hash and we're
            # doing encrypted. The likelyhood of false positives is low but
            # technically not 0
            self.logger.error("Encryption not supported at this time")

        try:
            unzip = zlib.decompress(req_raw)

        except zlib.error as e:
            self.logger.error(
                f"Failed to decompress v{version} {endpoint} request -> {e}"
            )
            return zlib.compress(b'{"stat": "0"}')

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

        return zlib.compress(json.dumps(resp, ensure_ascii=False).encode("utf-8"))

    def render_GET(self, request: Request, version: int, url_path: str) -> bytes:
        self.logger.info(f"v{version} GET {url_path}")
        url_split = url_path.split("/")

        if (url_split[0] == "api" and url_split[1] == "movie") or url_split[0] == "movie":
            if url_split[2] == "moviestart":
                return json.dumps({"moviestart":{"status":"OK"}}).encode()

        if url_split[0] == "old":
            if url_split[1] == "ping":
                self.logger.info(f"v{version} old server ping")
                return zlib.compress(b"ok")

            elif url_split[1].startswith("userdata"):
                self.logger.info(f"v{version} old server userdata inquire")
                return zlib.compress(b"{}")

            elif url_split[1].startswith("friend"):
                self.logger.info(f"v{version} old server friend inquire")
                return zlib.compress(b"{}")
        
        elif url_split[0] == "usbdl":
            if url_split[1] == "CONNECTIONTEST":
                self.logger.info(f"v{version} usbdl server test")
                return zlib.compress(b"ok")

        elif url_split[0] == "deliver":
            file = url_split[len(url_split) - 1]
            self.logger.info(f"v{version} {file} deliver inquire")
            
            if not self.game_cfg.deliver.enable or not path.exists(f"{self.game_cfg.deliver.content_folder}/{file}"):
                return zlib.compress(b"")
        
        else:
            return zlib.compress(b"{}")
