from typing import Dict, List, Tuple
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
from twisted.web.http import Request

from core.config import CoreConfig
from core.data import Data
from core.utils import Utils

class BaseServlet:
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = None
        self.logger = logging.getLogger("title")

    @classmethod
    def is_game_enabled(cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str) -> bool:
        """Called during boot to check if a specific game code should load.

        Args:
            game_code (str): 4 character game code
            core_cfg (CoreConfig): CoreConfig class
            cfg_dir (str): Config directory

        Returns:
            bool: True if the game is enabled and set to run, False otherwise
        
        """
        return False
    
    def get_endpoint_matchers(self) -> Tuple[List[Tuple[str, str, Dict]], List[Tuple[str, str, Dict]]]:
        """Called during boot to get all matcher endpoints this title servlet handles

        Returns:
            Tuple[List[Tuple[str, str, Dict]], List[Tuple[str, str, Dict]]]: A 2-length tuple where offset 0 is GET and offset 1 is POST, 
            containing a list of 3-length tuples where offset 0 is the name of the function in the handler that should be called, offset 1
            is the matching string, and offset 2 is a dict containing rules for the matcher.
        """
        return (
            [("render_GET", "/{game}/{version}/{endpoint}", {'game': R'S...'})], 
            [("render_POST", "/{game}/{version}/{endpoint}", {'game': R'S...'})]
        )
    
    def setup(self) -> None:
        """Called once during boot, should contain any additional setup the handler must do, such as starting any sub-services
        """
        pass

    def get_allnet_info(self, game_code: str, game_ver: int, keychip: str) -> Tuple[str, str]:
        """Called any time a request to PowerOn is made to retrieve the url/host strings to be sent back to the game

        Args:
            game_code (str): 4 character game code
            game_ver (int): version, expressed as an integer by multiplying by 100 (1.10 -> 110)
            keychip (str): Keychip serial of the requesting machine, can be used to deliver specific URIs to different machines

        Returns:
            Tuple[str, str]: A tuple where offset 0 is the allnet uri field, and offset 1 is the allnet host field
        """
        if not self.core_cfg.server.is_using_proxy and Utils.get_title_port(self.core_cfg) != 80:
            return (f"http://{self.core_cfg.title.hostname}:{Utils.get_title_port(self.core_cfg)}/{game_code}/{game_ver}/", "")

        return (f"http://{self.core_cfg.title.hostname}/{game_code}/{game_ver}/", "")

    def get_mucha_info(self, core_cfg: CoreConfig, cfg_dir: str) -> Tuple[bool, str]:
        """Called once during boot to check if this game is a mucha game

        Args:
            core_cfg (CoreConfig): CoreConfig class
            cfg_dir (str): Config directory

        Returns:
            Tuple[bool, str]: Tuple where offset 0 is true if the game is enabled, false otherwise, and offset 1 is the game CD
        """
        return (False, "")

    def render_POST(self, request: Request, game_code: str, matchers: Dict) -> bytes:
        self.logger.warn(f"{game_code} Does not dispatch POST")
        return None

    def render_GET(self, request: Request, game_code: str, matchers: Dict) -> bytes:
        self.logger.warn(f"{game_code} Does not dispatch GET")
        return None

class TitleServlet:
    title_registry: Dict[str, BaseServlet] = {}
    def __init__(self, core_cfg: CoreConfig, cfg_folder: str):
        super().__init__()
        self.config = core_cfg
        self.config_folder = cfg_folder
        self.data = Data(core_cfg)

        self.logger = logging.getLogger("title")
        if not hasattr(self.logger, "initialized"):
            log_fmt_str = "[%(asctime)s] Title | %(levelname)s | %(message)s"
            log_fmt = logging.Formatter(log_fmt_str)

            fileHandler = TimedRotatingFileHandler(
                "{0}/{1}.log".format(self.config.server.log_dir, "title"),
                when="d",
                backupCount=10,
            )
            fileHandler.setFormatter(log_fmt)

            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(log_fmt)

            self.logger.addHandler(fileHandler)
            self.logger.addHandler(consoleHandler)

            self.logger.setLevel(core_cfg.title.loglevel)
            coloredlogs.install(
                level=core_cfg.title.loglevel, logger=self.logger, fmt=log_fmt_str
            )
            self.logger.initialized = True

        plugins = Utils.get_all_titles()

        for folder, mod in plugins.items():
            if hasattr(mod, "game_codes") and hasattr(mod, "index") and hasattr(mod.index, "is_game_enabled"):
                should_call_setup = True
                game_servlet: BaseServlet = mod.index
                game_codes: List[str] = mod.game_codes
                
                for code in game_codes:
                    if game_servlet.is_game_enabled(code, self.config, self.config_folder):
                        handler_cls = game_servlet(self.config, self.config_folder)

                        if hasattr(handler_cls, "setup") and should_call_setup:
                            handler_cls.setup()
                            should_call_setup = False

                        self.title_registry[code] = handler_cls

            else:
                self.logger.error(f"{folder} missing game_code or index in __init__.py, or is_game_enabled in index")

        self.logger.info(
            f"Serving {len(self.title_registry)} game codes {'on port ' + str(core_cfg.title.port) if core_cfg.title.port > 0 else ''}"
        )

    def render_GET(self, request: Request, endpoints: dict) -> bytes:
        code = endpoints["title"]
        subaction = endpoints['subaction']
        
        if code not in self.title_registry:
            self.logger.warning(f"Unknown game code {code}")
            request.setResponseCode(404)
            return b""

        index = self.title_registry[code]
        handler = getattr(index, f"{subaction}", None)
        if handler is None:
            self.logger.error(f"{code} does not have handler for GET subaction {subaction}")
            request.setResponseCode(500)
            return b""

        return handler(request, code, endpoints)

    def render_POST(self, request: Request, endpoints: dict) -> bytes:
        code = endpoints["title"]
        subaction = endpoints['subaction']

        if code not in self.title_registry:
            self.logger.warning(f"Unknown game code {code}")
            request.setResponseCode(404)
            return b""

        index = self.title_registry[code]
        handler = getattr(index, f"{subaction}", None)
        if handler is None:
            self.logger.error(f"{code} does not have handler for POST subaction {subaction}")
            request.setResponseCode(500)
            return b""

        endpoints.pop("title")
        endpoints.pop("subaction")
        return handler(request, code, endpoints)
