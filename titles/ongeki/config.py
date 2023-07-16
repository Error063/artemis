from ast import Dict
from typing import List

from core.config import CoreConfig


class OngekiServerConfig:
    def __init__(self, parent_config: "OngekiConfig") -> None:
        self.__config = parent_config

    @property
    def enable(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "ongeki", "server", "enable", default=True
        )

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(
            CoreConfig.get_config_field(
                self.__config, "ongeki", "server", "loglevel", default="info"
            )
        )


class OngekiGachaConfig:
    def __init__(self, parent_config: "OngekiConfig") -> None:
        self.__config = parent_config

    @property
    def enabled_gachas(self) -> List[int]:
        return CoreConfig.get_config_field(
            self.__config, "ongeki", "gachas", "enabled_gachas", default=[]
        )


class OngekiCardMakerVersionConfig:
    def __init__(self, parent_config: "OngekiConfig") -> None:
        self.__config = parent_config

    def version(self, version: int) -> Dict:
        """
        in the form of:
        <ongeki version>: {"card_maker": <compatible card maker version>}
        6: {"card_maker": 1.30.01}
        """
        return CoreConfig.get_config_field(
            self.__config, "ongeki", "version", default={}
        ).get(version)


class OngekiConfig(dict):
    def __init__(self) -> None:
        self.server = OngekiServerConfig(self)
        self.gachas = OngekiGachaConfig(self)
        self.version = OngekiCardMakerVersionConfig(self)
