from core.config import CoreConfig


class SaoServerConfig:
    def __init__(self, parent_config: "SaoConfig"):
        self.__config = parent_config

    @property
    def enable(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "sao", "server", "enable", default=True
        )

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(
            CoreConfig.get_config_field(
                self.__config, "sao", "server", "loglevel", default="info"
            )
        )

    @property
    def auto_register(self) -> bool:
        """
        Automatically register users in `aime_user` on first carding in with sao
        if they don't exist already. Set to false to display an error instead.
        """
        return CoreConfig.get_config_field(
            self.__config, "sao", "server", "auto_register", default=True
        )

class SaoCryptConfig:
    def __init__(self, parent_config: "SaoConfig"):
        self.__config = parent_config
    
    @property
    def enable(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "sao", "crypt", "enable", default=False
        )
    
    @property
    def key(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "sao", "crypt", "key", default=""
        )
    
    @property
    def iv(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "sao", "crypt", "iv", default=""
        )

class SaoHashConfig:
    def __init__(self, parent_config: "SaoConfig"):
        self.__config = parent_config
        
    @property
    def verify_hash(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "sao", "hash", "verify_hash", default=False
        )
    
    @property
    def hash_base(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "sao", "hash", "hash_base", default=""
        )


class SaoConfig(dict):
    def __init__(self) -> None:
        self.server = SaoServerConfig(self)
        self.crypt = SaoCryptConfig(self)
        self.hash = SaoHashConfig(self)
