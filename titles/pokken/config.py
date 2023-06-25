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
    def auto_register(self) -> bool:
        """
        Automatically register users in `aime_user` on first carding in with pokken
        if they don't exist already. Set to false to display an error instead.
        """
        return CoreConfig.get_config_field(
            self.__config, "pokken", "server", "auto_register", default=True
        )

    @property
    def enable_matching(self) -> bool:
        """
        If global matching should happen
        """
        return CoreConfig.get_config_field(
            self.__config, "pokken", "server", "enable_matching", default=False
        )
    
    @property
    def stun_server_host(self) -> str:
        """
        Hostname of the EXTERNAL stun server the game should connect to. This is not handled by artemis.
        """
        return CoreConfig.get_config_field(
            self.__config, "pokken", "server", "stun_server_host", default="stunserver.stunprotocol.org"
        )

    @property
    def stun_server_port(self) -> int:
        """
        Port of the EXTERNAL stun server the game should connect to. This is not handled by artemis.
        """
        return CoreConfig.get_config_field(
            self.__config, "pokken", "server", "stun_server_port", default=3478
        )

class PokkenPortsConfig:
    def __init__(self, parent_config: "PokkenConfig"):
        self.__config = parent_config
    
    @property
    def game(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "pokken", "ports", "game", default=9000
        )

    @property
    def admission(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "pokken", "ports", "admission", default=9001
        )
    

class PokkenConfig(dict):
    def __init__(self) -> None:
        self.server = PokkenServerConfig(self)
        self.ports = PokkenPortsConfig(self)
