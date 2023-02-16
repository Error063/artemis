import logging, os
from typing import Any

class ServerConfig:
    def __init__(self, parent_config: "CoreConfig") -> None:
        self.__config = parent_config

    @property
    def listen_address(self) -> str:
        return CoreConfig.get_config_field(self.__config, '127.0.0.1', 'core', 'server', 'listen_address')

    @property
    def allow_user_registration(self) -> bool:
        return CoreConfig.get_config_field(self.__config, True, 'core', 'server', 'allow_user_registration')

    @property
    def allow_unregistered_games(self) -> bool:
        return CoreConfig.get_config_field(self.__config, True, 'core', 'server', 'allow_unregistered_games')

    @property
    def name(self) -> str:
        return CoreConfig.get_config_field(self.__config, "ARTEMiS", 'core', 'server', 'name')

    @property
    def is_develop(self) -> bool:
        return CoreConfig.get_config_field(self.__config, True, 'core', 'server', 'is_develop')

    @property
    def log_dir(self) -> str:
        return CoreConfig.get_config_field(self.__config, 'logs', 'core', 'server', 'log_dir')

class TitleConfig:
    def __init__(self, parent_config: "CoreConfig") -> None:
        self.__config = parent_config

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(CoreConfig.get_config_field(self.__config, "info", 'core', 'title', 'loglevel'))

    @property
    def hostname(self) -> str:
        return CoreConfig.get_config_field(self.__config, "localhost", 'core', 'title', 'hostname')

    @property
    def port(self) -> int:
        return CoreConfig.get_config_field(self.__config, 8080, 'core', 'title', 'port')

class DatabaseConfig:
    def __init__(self, parent_config: "CoreConfig") -> None:
        self.__config = parent_config

    @property
    def host(self) -> str:
        return CoreConfig.get_config_field(self.__config, "localhost", 'core', 'database', 'host')

    @property
    def username(self) -> str:
        return CoreConfig.get_config_field(self.__config, 'aime', 'core', 'database', 'username')

    @property
    def password(self) -> str:
        return CoreConfig.get_config_field(self.__config, 'aime', 'core', 'database', 'password')

    @property
    def name(self) -> str:
        return CoreConfig.get_config_field(self.__config, 'aime', 'core', 'database', 'name')

    @property
    def port(self) -> int:
        return CoreConfig.get_config_field(self.__config, 3306, 'core', 'database', 'port')

    @property
    def protocol(self) -> str:
        return CoreConfig.get_config_field(self.__config, "mysql", 'core', 'database', 'type')
    
    @property
    def sha2_password(self) -> bool:
        return CoreConfig.get_config_field(self.__config, False, 'core', 'database', 'sha2_password')
    
    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(CoreConfig.get_config_field(self.__config, "info", 'core', 'database', 'loglevel'))

    @property
    def user_table_autoincrement_start(self) -> int:
        return CoreConfig.get_config_field(self.__config, 10000, 'core', 'database', 'user_table_autoincrement_start')
    
    @property
    def memcached_host(self) -> str:
        return CoreConfig.get_config_field(self.__config, "localhost", 'core', 'database', 'memcached_host')

class FrontendConfig:
    def __init__(self, parent_config: "CoreConfig") -> None:
        self.__config = parent_config

    @property
    def enable(self) -> int:
        return CoreConfig.get_config_field(self.__config, False, 'core', 'frontend', 'enable')

    @property
    def port(self) -> int:
        return CoreConfig.get_config_field(self.__config, 8090, 'core', 'frontend', 'port')
    
    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(CoreConfig.get_config_field(self.__config, 'core', 'frontend', 'loglevel', "info"))

class AllnetConfig:
    def __init__(self, parent_config: "CoreConfig") -> None:
        self.__config = parent_config

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(CoreConfig.get_config_field(self.__config, "info", 'core', 'allnet', 'loglevel'))

    @property
    def port(self) -> int:
        return CoreConfig.get_config_field(self.__config, 80, 'core', 'allnet', 'port')
    
    @property
    def allow_online_updates(self) -> int:
        return CoreConfig.get_config_field(self.__config, False, 'core', 'allnet', 'allow_online_updates')

class BillingConfig:
    def __init__(self, parent_config: "CoreConfig") -> None:
        self.__config = parent_config

    @property
    def port(self) -> int:
        return CoreConfig.get_config_field(self.__config, 8443, 'core', 'billing', 'port')

    @property
    def ssl_key(self) -> str:
        return CoreConfig.get_config_field(self.__config, "cert/server.key", 'core', 'billing', 'ssl_key')

    @property
    def ssl_cert(self) -> str:
        return CoreConfig.get_config_field(self.__config, "cert/server.pem", 'core', 'billing', 'ssl_cert')
    
    @property
    def signing_key(self) -> str:
        return CoreConfig.get_config_field(self.__config, "cert/billing.key", 'core', 'billing', 'signing_key')

class AimedbConfig:
    def __init__(self, parent_config: "CoreConfig") -> None:
        self.__config = parent_config
    
    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(CoreConfig.get_config_field(self.__config, "info", 'core', 'aimedb', 'loglevel'))

    @property
    def port(self) -> int:
        return CoreConfig.get_config_field(self.__config, 22345, 'core', 'aimedb', 'port')

    @property
    def key(self) -> str:
        return CoreConfig.get_config_field(self.__config, "", 'core', 'aimedb', 'key')

class CoreConfig(dict):
    def __init__(self) -> None:
        self.server = ServerConfig(self)
        self.title = TitleConfig(self)
        self.database = DatabaseConfig(self)
        self.frontend = FrontendConfig(self)
        self.allnet = AllnetConfig(self)
        self.billing = BillingConfig(self)
        self.aimedb = AimedbConfig(self)

    @classmethod
    def str_to_loglevel(cls, level_str: str):
        if level_str.lower() == "error":
            return logging.ERROR
        elif level_str.lower().startswith("warn"): # Fits warn or warning
            return logging.WARN
        elif level_str.lower() == "debug":
            return logging.DEBUG
        else:
             return logging.INFO

    @classmethod
    def get_config_field(cls, __config: dict, default: Any, *path: str) -> Any:
        envKey = 'CFG_'
        for arg in path:
            envKey += arg + '_'
        
        if envKey.endswith('_'):
            envKey = envKey[:-1]

        if envKey in os.environ:
            return os.environ.get(envKey)

        read = __config

        for x in range(len(path) - 1):
            read = read.get(path[x], {})

        return read.get(path[len(path) - 1], default)
