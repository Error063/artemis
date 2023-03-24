from core.config import CoreConfig
from typing import Dict


class ChuniServerConfig:
    def __init__(self, parent_config: "ChuniConfig") -> None:
        self.__config = parent_config

    @property
    def enable(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "chuni", "server", "enable", default=True
        )

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(
            CoreConfig.get_config_field(
                self.__config, "chuni", "server", "loglevel", default="info"
            )
        )


class ChuniTeamConfig:
    def __init__(self, parent_config: "ChuniConfig") -> None:
        self.__config = parent_config

    @property
    def team_name(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "chuni", "team", "name", default=""
        )


class ChuniVersionConfig:
    def __init__(self, parent_config: "ChuniConfig") -> None:
        self.__config = parent_config

    def version_rom(self, version: int) -> str:
        return CoreConfig.get_config_field(
            self.__config, "chuni", "version", f"{version}", "rom", default="2.00.00"
        )

    def version_data(self, version: int) -> str:
        return CoreConfig.get_config_field(
            self.__config, "chuni", "version", f"{version}", "data", default="2.00.00"
        )


class ChuniCryptoConfig:
    def __init__(self, parent_config: "ChuniConfig") -> None:
        self.__config = parent_config

    @property
    def keys(self) -> Dict:
        """
        in the form of:
        internal_version: [key, iv]
        all values are hex strings
        """
        return CoreConfig.get_config_field(
            self.__config, "chuni", "crypto", "keys", default={}
        )

    @property
    def encrypted_only(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "chuni", "crypto", "encrypted_only", default=False
        )


class ChuniConfig(dict):
    def __init__(self) -> None:
        self.server = ChuniServerConfig(self)
        self.team = ChuniTeamConfig(self)
        self.version = ChuniVersionConfig(self)
        self.crypto = ChuniCryptoConfig(self)
