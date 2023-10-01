from core.config import CoreConfig


class IDACServerConfig:
    def __init__(self, parent: "IDACConfig") -> None:
        self.__config = parent

    @property
    def enable(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "idac", "server", "enable", default=True
        )

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(
            CoreConfig.get_config_field(
                self.__config, "idac", "server", "loglevel", default="info"
            )
        )

    @property
    def ssl(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "idac", "server", "ssl", default=False
        )

    @property
    def ssl_cert(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "idac", "server", "ssl_cert", default="cert/title.crt"
        )

    @property
    def ssl_key(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "idac", "server", "ssl_key", default="cert/title.key"
        )

    @property
    def matching_host(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "idac", "server", "matching_host", default="127.0.0.1"
        )

    @property
    def matching(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "idac", "server", "port_matching", default=20000
        )

    @property
    def echo1(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "idac", "server", "port_echo1", default=20001
        )

    @property
    def echo2(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "idac", "server", "port_echo2", default=20002
        )

    @property
    def matching_p2p(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "idac", "server", "port_matching_p2p", default=20003
        )


class IDACStampConfig:
    def __init__(self, parent: "IDACConfig") -> None:
        self.__config = parent

    @property
    def enable(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "idac", "stamp", "enable", default=True
        )

    @property
    def enabled_stamps(self) -> list:
        return CoreConfig.get_config_field(
            self.__config,
            "idac",
            "stamp",
            "enabled_stamps",
            default=[
                "touhou_remilia_scarlet",
                "touhou_flandre_scarlet",
                "touhou_sakuya_izayoi",
            ],
        )


class IDACTimetrialConfig:
    def __init__(self, parent: "IDACConfig") -> None:
        self.__config = parent

    @property
    def enable(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "idac", "timetrial", "enable", default=True
        )

    @property
    def enabled_timetrial(self) -> str:
        return CoreConfig.get_config_field(
            self.__config,
            "idac",
            "timetrial",
            "enabled_timetrial",
            default="touhou_remilia_scarlet",
        )


class IDACConfig(dict):
    def __init__(self) -> None:
        self.server = IDACServerConfig(self)
        self.stamp = IDACStampConfig(self)
        self.timetrial = IDACTimetrialConfig(self)
