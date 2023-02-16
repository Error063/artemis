from twisted.web import resource
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler

from core.config import CoreConfig
from core.data import Data

class AllnetServlet(resource.Resource):
    isLeaf = True
    def __init__(self, core_cfg: CoreConfig, cfg_folder: str):        
        super().__init__()
        self.config = core_cfg
        self.config_folder = cfg_folder
        self.data = Data(core_cfg)

        self.logger = logging.getLogger("allnet")
        log_fmt_str = "[%(asctime)s] Allnet | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)        

        fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.config.server.log_dir, "allnet"), when="d", backupCount=10)
        fileHandler.setFormatter(log_fmt)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        
        self.logger.setLevel(core_cfg.allnet.loglevel)
        coloredlogs.install(level=core_cfg.allnet.loglevel, logger=self.logger, fmt=log_fmt_str)

class BillingServlet(resource.Resource):
    isLeaf = True
    def __init__(self, core_cfg: CoreConfig, cfg_folder: str):        
        super().__init__()
        self.config = core_cfg
        self.config_folder = cfg_folder
        self.data = Data(core_cfg)
        self.logger = logging.getLogger('allnet')