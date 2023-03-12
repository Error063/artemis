from typing import Dict, Any
from types import ModuleType
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
                        ret[dir] = mod

                    except ImportError as e:
                        logging.getLogger("core").error(f"get_all_titles: {dir} - {e}")
                        raise
            return ret
