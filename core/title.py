from twisted.web import resource
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
        
        if "game_registry" not in globals():
            globals()["game_registry"] = Utils.get_all_titles()
    
    def handle_GET(self, request: Request):
        pass
    
    def handle_POST(self, request: Request):
        pass