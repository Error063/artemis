import logging, os
from typing import Any

class ServerConfig:
    def __init__(self, parent_config: "CoreConfig") -> None:
        self.__config = parent_config

    @property
    def listen_address(self) -> str:
        """
        Address Artemis will bind to and listen on
        """
        return CoreConfig.get_config_field(
            self.__config, "core", "server", "listen_address", default="127.0.0.1"
        )
    
    @property
    def hostname(self) -> str:
        """
        Hostname sent to games
        """
        return CoreConfig.get_config_field(
            self.__config, "core", "server", "hostname", default="localhost"
        )
    
    @property
    def port(self) -> int:
        """
        Port the game will listen on
        """
        return CoreConfig.get_config_field(
            self.__config, "core", "server", "port", default=8080
        )

    @property
    def ssl_key(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "server", "ssl_key", default="cert/title.key"
        )

    @property
    def ssl_cert(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "title", "ssl_cert", default="cert/title.pem"
        )

    @property
    def allow_user_registration(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "core", "server", "allow_user_registration", default=True
        )

    @property
    def allow_unregistered_serials(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "core", "server", "allow_unregistered_serials", default=True
        )

    @property
    def name(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "server", "name", default="ARTEMiS"
        )

    @property
    def is_develop(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "core", "server", "is_develop", default=True
        )

    @property
    def is_using_proxy(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "core", "server", "is_using_proxy", default=False
        )

    @property
    def proxy_port(self) -> int:
        """
        What port the proxy is listening on. This will be sent instead of 'port' if 
        is_using_proxy is True and this value is non-zero
        """
        return CoreConfig.get_config_field(
            self.__config, "core", "title", "proxy_port", default=0
        )

    @property
    def proxy_port_ssl(self) -> int:
        """
        What port the proxy is listening for secure connections on. This will be sent 
        instead of 'port' if is_using_proxy is True and this value is non-zero
        """
        return CoreConfig.get_config_field(
            self.__config, "core", "title", "proxy_port_ssl", default=0
        )

    @property
    def log_dir(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "server", "log_dir", default="logs"
        )

    @property
    def check_arcade_ip(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "core", "server", "check_arcade_ip", default=False
        )

    @property
    def strict_ip_checking(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "core", "server", "strict_ip_checking", default=False
        )

class TitleConfig:
    def __init__(self, parent_config: "CoreConfig") -> None:
        self.__config = parent_config

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(
            CoreConfig.get_config_field(
                self.__config, "core", "title", "loglevel", default="info"
            )
        )

    @property
    def reboot_start_time(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "title", "reboot_start_time", default="04:00"
        )

    @property
    def reboot_end_time(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "title", "reboot_end_time", default="05:00"
        )

class DatabaseConfig:
    def __init__(self, parent_config: "CoreConfig") -> None:
        self.__config = parent_config

    @property
    def host(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "database", "host", default="localhost"
        )

    @property
    def username(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "database", "username", default="aime"
        )

    @property
    def password(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "database", "password", default="aime"
        )

    @property
    def name(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "database", "name", default="aime"
        )

    @property
    def port(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "core", "database", "port", default=3306
        )

    @property
    def protocol(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "database", "type", default="mysql"
        )

    @property
    def sha2_password(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "core", "database", "sha2_password", default=False
        )

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(
            CoreConfig.get_config_field(
                self.__config, "core", "database", "loglevel", default="info"
            )
        )

    @property
    def enable_memcached(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "core", "database", "enable_memcached", default=True
        )

    @property
    def memcached_host(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "database", "memcached_host", default="localhost"
        )

class FrontendConfig:
    def __init__(self, parent_config: "CoreConfig") -> None:
        self.__config = parent_config

    @property
    def standalone(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "core", "frontend", "standalone", default=True
        )

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(
            CoreConfig.get_config_field(
                self.__config, "core", "frontend", "loglevel", default="info"
            )
        )
    
    @property
    def secret(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "frontend", "secret", default=""
        )

class AllnetConfig:
    def __init__(self, parent_config: "CoreConfig") -> None:
        self.__config = parent_config

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(
            CoreConfig.get_config_field(
                self.__config, "core", "allnet", "loglevel", default="info"
            )
        )

    @property
    def allow_online_updates(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "core", "allnet", "allow_online_updates", default=False
        )

    @property
    def update_cfg_folder(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "allnet", "update_cfg_folder", default=""
        )

class BillingConfig:
    def __init__(self, parent_config: "CoreConfig") -> None:
        self.__config = parent_config
    
    @property
    def standalone(self) -> bool:
        return CoreConfig.get_config_field(
            self.__config, "core", "billing", "standalone", default=True
        )

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(
            CoreConfig.get_config_field(
                self.__config, "core", "billing", "loglevel", default="info"
            )
        )

    @property
    def port(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "core", "billing", "port", default=8443
        )

    @property
    def ssl_key(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "billing", "ssl_key", default="cert/server.key"
        )

    @property
    def ssl_cert(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "billing", "ssl_cert", default="cert/server.pem"
        )

    @property
    def signing_key(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "billing", "signing_key", default="cert/billing.key"
        )

class AimedbConfig:
    def __init__(self, parent_config: "CoreConfig") -> None:
        self.__config = parent_config

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(
            CoreConfig.get_config_field(
                self.__config, "core", "aimedb", "loglevel", default="info"
            )
        )

    @property
    def port(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "core", "aimedb", "port", default=22345
        )

    @property
    def key(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "aimedb", "key", default=""
        )

    @property
    def id_secret(self) -> str:
        return CoreConfig.get_config_field(
            self.__config, "core", "aimedb", "id_secret", default=""
        )

    @property
    def id_lifetime_seconds(self) -> int:
        return CoreConfig.get_config_field(
            self.__config, "core", "aimedb", "id_lifetime_seconds", default=86400
        )

class MuchaConfig:
    def __init__(self, parent_config: "CoreConfig") -> None:
        self.__config = parent_config

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(
            CoreConfig.get_config_field(
                self.__config, "core", "mucha", "loglevel", default="info"
            )
        )

class CoreConfig(dict):
    def __init__(self) -> None:
        self.server = ServerConfig(self)
        self.title = TitleConfig(self)
        self.database = DatabaseConfig(self)
        self.frontend = FrontendConfig(self)
        self.allnet = AllnetConfig(self)
        self.billing = BillingConfig(self)
        self.aimedb = AimedbConfig(self)
        self.mucha = MuchaConfig(self)

    @classmethod
    def str_to_loglevel(cls, level_str: str):
        if level_str.lower() == "error":
            return logging.ERROR
        elif level_str.lower().startswith("warn"):  # Fits warn or warning
            return logging.WARN
        elif level_str.lower() == "debug":
            return logging.DEBUG
        else:
            return logging.INFO

    @classmethod
    def get_config_field(
        cls, __config: dict, module, *path: str, default: Any = ""
    ) -> Any:
        envKey = f"CFG_{module}_"
        for arg in path:
            envKey += arg + "_"

        if envKey.endswith("_"):
            envKey = envKey[:-1]

        if envKey in os.environ:
            return os.environ.get(envKey)

        read = __config

        for x in range(len(path) - 1):
            read = read.get(path[x], {})

        return read.get(path[len(path) - 1], default)
