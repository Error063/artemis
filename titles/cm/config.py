from typing import Dict
from core.config import CoreConfig


class CardMakerServerConfig:
    def __init__(self, parent_config: "CardMakerConfig") -> None:
        self.__config = parent_config

    @property
    def enable(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "cardmaker", "server", "enable", default=True
        )

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(
            CoreConfig.get_config_field(
                self.__config, "cardmaker", "server", "loglevel", default="info"
            )
        )


class CardMakerVersionConfig:
    def __init__(self, parent_config: "CardMakerConfig") -> None:
        self.__config = parent_config

    def version(self, version: int) -> Dict:
        """
        in the form of:
        1: {"ongeki": 1.30.01, "chuni": 2.00.00, "maimai": 1.20.00}
        """
        return CoreConfig.get_config_field(
            self.__config, "cardmaker", "version", default={
                0: {    
                    "ongeki": "1.30.01",
                    "chuni": "2.00.00",
                    "maimai": "1.20.00"
                },
                1: {
                    "ongeki": "1.35.03",
                    "chuni": "2.10.00",
                    "maimai": "1.30.00"
                }
            }
        )[version]


class CardMakerConfig(dict):
    def __init__(self) -> None:
        self.server = CardMakerServerConfig(self)
        self.version = CardMakerVersionConfig(self)
