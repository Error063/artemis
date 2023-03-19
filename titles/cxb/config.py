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

    @property
    def hostname(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "cxb", "server", "hostname", default="localhost"
        )

    @property
    def ssl_enable(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "cxb", "server", "ssl_enable", default=False
        )

    @property
    def port(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "cxb", "server", "port", default=8082
        )

    @property
    def port_secure(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "cxb", "server", "port_secure", default=443
        )

    @property
    def ssl_cert(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "cxb", "server", "ssl_cert", default="cert/title.crt"
        )

    @property
    def ssl_key(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "cxb", "server", "ssl_key", default="cert/title.key"
        )


class CxbConfig(dict):
    def __init__(self) -> None:
        self.server = CxbServerConfig(self)
