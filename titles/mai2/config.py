from core.config import CoreConfig


class Mai2ServerConfig:
    def __init__(self, parent: "Mai2Config") -> None:
        self.__config = parent

    @property
    def enable(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "mai2", "server", "enable", default=True
        )

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(
            CoreConfig.get_config_field(
                self.__config, "mai2", "server", "loglevel", default="info"
            )
        )


class Mai2Config(dict):
    def __init__(self) -> None:
        self.server = Mai2ServerConfig(self)
