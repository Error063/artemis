from twisted.web.http import Request
import json
import inflection
import yaml
import string
import logging, coloredlogs
import zlib
from logging.handlers import TimedRotatingFileHandler

from core.config import CoreConfig
from titles.mai2.config import Mai2Config
from titles.mai2.const import Mai2Constants
from titles.mai2.base import Mai2Base
from titles.mai2.plus import Mai2Plus
from titles.mai2.splash import Mai2Splash
from titles.mai2.splashplus import Mai2SplashPlus
from titles.mai2.universe import Mai2Universe
from titles.mai2.universeplus import Mai2UniversePlus


class Mai2Servlet():
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = Mai2Config()
        self.game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/{Mai2Constants.CONFIG_NAME}")))

        self.versions = [
            Mai2Base(core_cfg, self.game_cfg),
            Mai2Plus(core_cfg, self.game_cfg),
            Mai2Splash(core_cfg, self.game_cfg),
            Mai2SplashPlus(core_cfg, self.game_cfg),
            Mai2Universe(core_cfg, self.game_cfg),
            Mai2UniversePlus(core_cfg, self.game_cfg),
        ]

        self.logger = logging.getLogger("mai2")
        log_fmt_str = "[%(asctime)s] Mai2 | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.core_cfg.server.log_dir, "mai2"), encoding='utf8',
            when="d", backupCount=10)

        fileHandler.setFormatter(log_fmt)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        
        self.logger.setLevel(self.game_cfg.server.loglevel)
        coloredlogs.install(level=self.game_cfg.server.loglevel, logger=self.logger, fmt=log_fmt_str)

    def render_POST(self, request: Request, version: int, url_path: str) -> bytes:
        req_raw = request.content.getvalue()
        url = request.uri.decode()
        url_split = url_path.split("/")
        internal_ver = 0
        endpoint = url_split[len(url_split) - 1]

        if version < 105: # 1.0
            internal_ver = Mai2Constants.VER_MAIMAI_DX
        elif version >= 105 and version < 110: # Plus
            internal_ver = Mai2Constants.VER_MAIMAI_DX_PLUS
        elif version >= 110 and version < 115: # Splash
            internal_ver = Mai2Constants.VER_MAIMAI_DX_SPLASH
        elif version >= 115 and version < 120: # Splash Plus
            internal_ver = Mai2Constants.VER_MAIMAI_DX_SPLASH_PLUS
        elif version >= 120 and version < 125: # Universe
            internal_ver = Mai2Constants.VER_MAIMAI_DX_UNIVERSE
        elif version >= 125: # Universe Plus
            internal_ver = Mai2Constants.VER_MAIMAI_DX_UNIVERSE_PLUS

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