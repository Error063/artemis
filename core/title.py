from twisted.web import resource
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler

from core.config import CoreConfig
from core.data import Data

class TitleServlet(resource.Resource):
    isLeaf = True
    def __init__(self, core_cfg: CoreConfig, cfg_folder: str):        
        super().__init__()
        self.config = core_cfg
        self.config_folder = cfg_folder
        self.data = Data(core_cfg)