from core.config import CoreConfig


class PokkenServerConfig:
    def __init__(self, parent_config: "PokkenConfig"):
        self.__config = parent_config

    @property
    def hostname(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "pokken", "server", "hostname", default="localhost"
        )

    @property
    def enable(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "pokken", "server", "enable", default=True
        )

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(
            CoreConfig.get_config_field(
                self.__config, "pokken", "server", "loglevel", default="info"
            )
        )

    @property
    def port(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "pokken", "server", "port", default=9000
        )

    @property
    def port_stun(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "pokken", "server", "port_stun", default=9001
        )

    @property
    def port_turn(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "pokken", "server", "port_turn", default=9002
        )

    @property
    def port_admission(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "pokken", "server", "port_admission", default=9003
        )

    @property
    def auto_register(self) -> bool:
        """
        Automatically register users in `aime_user` on first carding in with pokken
        if they don't exist already. Set to false to display an error instead.
        """
        return CoreConfig.get_config_field(
            self.__config, "pokken", "server", "auto_register", default=True
        )

class PokkenConfig(dict):
    def __init__(self) -> None:
        self.server = PokkenServerConfig(self)
