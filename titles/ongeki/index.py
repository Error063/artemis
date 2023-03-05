from twisted.web.http import Request
import json
import inflection
import yaml
import string
import logging, coloredlogs
import zlib
from logging.handlers import TimedRotatingFileHandler
from os import path
from typing import Tuple

from core.config import CoreConfig
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

class OngekiServlet():
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = OngekiConfig()
        if path.exists(f"{cfg_dir}/{OngekiConstants.CONFIG_NAME}"):
            self.game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/{OngekiConstants.CONFIG_NAME}")))

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
        log_fmt_str = "[%(asctime)s] Ongeki | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.core_cfg.server.log_dir, "ongeki"), encoding='utf8',
        when="d", backupCount=10)

        fileHandler.setFormatter(log_fmt)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        
        self.logger.setLevel(self.game_cfg.server.loglevel)
        coloredlogs.install(level=self.game_cfg.server.loglevel, logger=self.logger, fmt=log_fmt_str)
    
    @classmethod
    def get_allnet_info(cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str) -> Tuple[bool, str, str]:
        game_cfg = OngekiConfig()

        if path.exists(f"{cfg_dir}/{OngekiConstants.CONFIG_NAME}"):
            game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/{OngekiConstants.CONFIG_NAME}")))

        if not game_cfg.server.enable:
            return (False, "", "")
        
        if core_cfg.server.is_develop:
            return (True, f"http://{core_cfg.title.hostname}:{core_cfg.title.port}/{game_code}/$v/", f"{core_cfg.title.hostname}:{core_cfg.title.port}/")
        
        return (True, f"http://{core_cfg.title.hostname}/{game_code}/$v/", f"{core_cfg.title.hostname}/")

    def render_POST(self, request: Request, version: int, url_path: str) -> bytes:
        req_raw = request.content.getvalue()
        url_split = url_path.split("/")
        internal_ver = 0
        endpoint = url_split[len(url_split) - 1]

        if version < 105: # 1.0
            internal_ver = OngekiConstants.VER_ONGEKI
        elif version >= 105 and version < 110: # Plus
            internal_ver = OngekiConstants.VER_ONGEKI_PLUS
        elif version >= 110 and version < 115: # Summer
            internal_ver = OngekiConstants.VER_ONGEKI_SUMMER
        elif version >= 115 and version < 120: # Summer Plus
            internal_ver = OngekiConstants.VER_ONGEKI_SUMMER_PLUS
        elif version >= 120 and version < 125: # Red
            internal_ver = OngekiConstants.VER_ONGEKI_RED
        elif version >= 125 and version < 130: # Red Plus
            internal_ver = OngekiConstants.VER_ONGEKI_RED_PLUS
        elif version >= 130 and version < 135: # Bright
            internal_ver = OngekiConstants.VER_ONGEKI_BRIGHT
        elif version >= 135 and version < 140: # Bright Memory
            internal_ver = OngekiConstants.VER_ONGEKI_BRIGHT_MEMORY

        if all(c in string.hexdigits for c in endpoint) and len(endpoint) == 32:
            # If we get a 32 character long hex string, it's a hash and we're 
            # doing encrypted. The likelyhood of false positives is low but 
            # technically not 0
            self.logger.error("Encryption not supported at this time")

        try:            
            unzip = zlib.decompress(req_raw)
            
        except zlib.error as e:
            self.logger.error(f"Failed to decompress v{version} {endpoint} request -> {e}")
            return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))
        
        req_data = json.loads(unzip)
        
        self.logger.info(f"v{version} {endpoint} request - {req_data}")

        func_to_find = "handle_" + inflection.underscore(endpoint) + "_request"

        try:
            handler = getattr(self.versions[internal_ver], func_to_find)
            resp = handler(req_data)
            
        except AttributeError as e: 
            self.logger.warning(f"Unhandled v{version} request {endpoint} - {e}")
            return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

        except Exception as e:
            self.logger.error(f"Error handling v{version} method {endpoint} - {e}")
            return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))
        
        if resp == None:
            resp = {'returnCode': 1}
        
        self.logger.info(f"Response {resp}")
        
        return zlib.compress(json.dumps(resp, ensure_ascii=False).encode("utf-8"))


        