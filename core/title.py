from typing import Dict, Any
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
from twisted.web.http import Request

from core.config import CoreConfig
from core.data import Data
from core.utils import Utils

class TitleServlet():
    def __init__(self, core_cfg: CoreConfig, cfg_folder: str):        
        super().__init__()
        self.config = core_cfg
        self.config_folder = cfg_folder
        self.data = Data(core_cfg)
        self.title_registry: Dict[str, Any] = {}

        self.logger = logging.getLogger("title")
        if not hasattr(self.logger, "initialized"):
            log_fmt_str = "[%(asctime)s] Title | %(levelname)s | %(message)s"
            log_fmt = logging.Formatter(log_fmt_str)        

            fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.config.server.log_dir, "title"), when="d", backupCount=10)
            fileHandler.setFormatter(log_fmt)
            
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(log_fmt)

            self.logger.addHandler(fileHandler)
            self.logger.addHandler(consoleHandler)
            
            self.logger.setLevel(core_cfg.title.loglevel)
            coloredlogs.install(level=core_cfg.title.loglevel, logger=self.logger, fmt=log_fmt_str)
            self.logger.initialized = True
        
        plugins = Utils.get_all_titles()
        
        for folder, mod in plugins.items():
            if hasattr(mod, "game_codes") and hasattr(mod, "index"):
                handler_cls = mod.index(self.config, self.config_folder)
                if hasattr(handler_cls, "setup"):
                    handler_cls.setup()
                
                for code in mod.game_codes:
                    self.title_registry[code] = handler_cls
            
            else:
                self.logger.error(f"{folder} missing game_code or index in __init__.py")
        
        self.logger.info(f"Serving {len(self.title_registry)} game codes on port {core_cfg.title.port}")

    def render_GET(self, request: Request, endpoints: dict) -> bytes:
        code = endpoints["game"]
        if code not in self.title_registry:
            self.logger.warn(f"Unknown game code {code}")
        
        index = self.title_registry[code]
        if not hasattr(index, "render_GET"):
            self.logger.warn(f"{code} does not dispatch GET")
            return b""

        return index.render_GET(request, endpoints["version"], endpoints["endpoint"])
    
    def render_POST(self, request: Request, endpoints: dict) -> bytes:
        code = endpoints["game"]
        if code not in self.title_registry:
            self.logger.warn(f"Unknown game code {code}")
        
        index = self.title_registry[code]
        if not hasattr(index, "render_POST"):
            self.logger.warn(f"{code} does not dispatch POST")
            return b""

        return index.render_POST(request, int(endpoints["version"]), endpoints["endpoint"])
