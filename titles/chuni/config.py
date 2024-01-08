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
        
    @property
    def news_msg(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "chuni", "server", "news_msg", default=""
        )


class ChuniTeamConfig:
    def __init__(self, parent_config: "ChuniConfig") -> None:
        self.__config = parent_config

    @property
    def team_name(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "chuni", "team", "name", default=""
        )
    @property
    def rank_scale(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "chuni", "team", "rank_scale", default="False"
        )


class ChuniModsConfig:
    def __init__(self, parent_config: "ChuniConfig") -> None:
        self.__config = parent_config

    @property
    def use_login_bonus(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "chuni", "mods", "use_login_bonus", default=True
        )


class ChuniVersionConfig:
    def __init__(self, parent_config: "ChuniConfig") -> None:
        self.__config = parent_config

    def version(self, version: int) -> Dict:
        """
        in the form of:
        11: {"rom": 2.00.00, "data": 2.00.00}
        """
        return CoreConfig.get_config_field(
            self.__config, "chuni", "version", default={}
        )[version]


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

class ChuniMatchingConfig:
    def __init__(self, parent_config: "ChuniConfig") -> None:
        self.__config = parent_config
    
    @property
    def enable(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "chuni", "matching", "enable", default=False
        )
    
    @property
    def stun_uri(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "chuni", "matching", "stun_uri", default="stun:stunserver.stunprotocol.org:3478"
        )
    
    @property
    def turn_uri(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "chuni", "matching", "turn_uri", default="turn:stunserver.stunprotocol.org:3478"
        )
    
    @property
    def match_time_limit(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "chuni", "matching", "match_time_limit", default=60
        )
    
    @property
    def match_error_limit(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "chuni", "matching", "match_error_limit", default=9999
        )

class ChuniConfig(dict):
    def __init__(self) -> None:
        self.server = ChuniServerConfig(self)
        self.team = ChuniTeamConfig(self)
        self.mods = ChuniModsConfig(self)
        self.version = ChuniVersionConfig(self)
        self.crypto = ChuniCryptoConfig(self)
        self.matching = ChuniMatchingConfig(self)
