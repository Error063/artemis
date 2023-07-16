from core.config import CoreConfig


class SaoServerConfig:
    def __init__(self, parent_config: "SaoConfig"):
        self.__config = parent_config

    @property
    def hostname(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "sao", "server", "hostname", default="localhost"
        )

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
    def port(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "sao", "server", "port", default=9000
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


class SaoConfig(dict):
    def __init__(self) -> None:
        self.server = SaoServerConfig(self)
