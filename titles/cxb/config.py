from core.config import CoreConfig


class CxbServerConfig:
    def __init__(self, parent_config: "CxbConfig"):
        self.__config = parent_config

    @property
    def enable(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "cxb", "server", "enable", default=True
        )

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(
            CoreConfig.get_config_field(
                self.__config, "cxb", "server", "loglevel", default="info"
            )
        )


class CxbConfig(dict):
    def __init__(self) -> None:
        self.server = CxbServerConfig(self)
