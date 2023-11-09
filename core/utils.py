from typing import Dict, Any
from types import ModuleType
from twisted.web.http import Request
import logging
import importlib
from os import walk

from .config import CoreConfig

class Utils:
    real_title_port = None
    real_title_port_ssl = None
    @classmethod
    def get_all_titles(cls) -> Dict[str, ModuleType]:
        ret: Dict[str, Any] = {}

        for root, dirs, files in walk("titles"):
            for dir in dirs:
                if not dir.startswith("__"):
                    try:
                        mod = importlib.import_module(f"titles.{dir}")
                        if hasattr(mod, "game_codes") and hasattr(
                            mod, "index"
                        ):  # Minimum required to function
                            ret[dir] = mod

                    except ImportError as e:
                        logging.getLogger("core").error(f"get_all_titles: {dir} - {e}")
                        raise
            return ret

    @classmethod
    def get_ip_addr(cls, req: Request) -> str:
        return (
            req.getAllHeaders()[b"x-forwarded-for"].decode()
            if b"x-forwarded-for" in req.getAllHeaders()
            else req.getClientAddress().host
        )
    
    @classmethod
    def get_title_port(cls, cfg: CoreConfig):
        if cls.real_title_port is not None: return cls.real_title_port

        if cfg.title.port == 0:
            cls.real_title_port = cfg.allnet.port
        
        else:
            cls.real_title_port = cfg.title.port
        
        return cls.real_title_port

    @classmethod
    def get_title_port_ssl(cls, cfg: CoreConfig):
        if cls.real_title_port_ssl is not None: return cls.real_title_port_ssl

        if cfg.title.port_ssl == 0:
            cls.real_title_port_ssl = 443
        
        else:
            cls.real_title_port_ssl = cfg.title.port_ssl
        
        return cls.real_title_port_ssl
