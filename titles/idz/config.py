from typing import List, Dict

from core.config import CoreConfig


class IDZServerConfig:
    def __init__(self, parent_config: "IDZConfig") -> None:
        self.__config = parent_config

    @property
    def enable(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "idz", "server", "enable", default=True
        )

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(
            CoreConfig.get_config_field(
                self.__config, "idz", "server", "loglevel", default="info"
            )
        )

    @property
    def hostname(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "idz", "server", "hostname", default=""
        )

    @property
    def news(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "idz", "server", "news", default=""
        )

    @property
    def aes_key(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "idz", "server", "aes_key", default=""
        )


class IDZPortsConfig:
    def __init__(self, parent_config: "IDZConfig") -> None:
        self.__config = parent_config

    @property
    def userdb(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "idz", "ports", "userdb", default=10000
        )

    @property
    def match(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "idz", "ports", "match", default=10010
        )

    @property
    def echo(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "idz", "ports", "echo", default=10020
        )


class IDZConfig(dict):
    def __init__(self) -> None:
        self.server = IDZServerConfig(self)
        self.ports = IDZPortsConfig(self)

    @property
    def rsa_keys(self) -> List[Dict]:
        return CoreConfig.get_config_field(self, "idz", "rsa_keys", default=[])
