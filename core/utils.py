from typing import Dict, Any
from types import ModuleType
from twisted.web.http import Request
import logging
import importlib
from os import walk


class Utils:
    @classmethod
    def get_all_titles(cls) -> Dict[str, ModuleType]:
        ret: Dict[str, Any] = {}

        for root, dirs, files in walk("titles"):
            for dir in dirs:
                if not dir.startswith("__"):
                    try:
                        mod = importlib.import_module(f"titles.{dir}")
                        if hasattr(mod, "game_codes") and hasattr(mod, "index"): # Minimum required to function
                            ret[dir] = mod

                    except ImportError as e:
                        logging.getLogger("core").error(f"get_all_titles: {dir} - {e}")
                        raise
            return ret
    
    @classmethod
    def get_ip_addr(cls, req: Request) -> str:
        return req.getAllHeaders()[b"x-forwarded-for"].decode() if b"x-forwarded-for" in req.getAllHeaders() else req.getClientAddress().host
