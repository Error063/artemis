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


class CardMakerConfig(dict):
    def __init__(self) -> None:
        self.server = CardMakerServerConfig(self)
