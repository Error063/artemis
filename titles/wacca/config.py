from typing import Dict, List
from core.config import CoreConfig

class WaccaServerConfig():
    def __init__(self, parent_config: "WaccaConfig") -> None:
        self.__config = parent_config
    
    @property
    def enable(self) -> bool:
        return CoreConfig.get_config_field(self.__config, 'wacca', 'server', 'enable', default=True)
    
    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(CoreConfig.get_config_field(self.__config, 'wacca', 'server', 'loglevel', default="info"))

    @property
    def prefecture_name(self) -> str:
        return CoreConfig.get_config_field(self.__config, 'wacca', 'server', 'prefecture_name', default="Hokkaido")

class WaccaModsConfig():
    def __init__(self, parent_config: "WaccaConfig") -> None:
        self.__config = parent_config
    
    @property
    def always_vip(self) -> bool:
        return CoreConfig.get_config_field(self.__config, 'wacca', 'mods', 'always_vip', default=True)
    
    @property
    def infinite_tickets(self) -> bool:
        return CoreConfig.get_config_field(self.__config, 'wacca', 'mods', 'infinite_tickets', default=True)

    @property
    def infinite_wp(self) -> bool:
        return CoreConfig.get_config_field(self.__config, 'wacca', 'mods', 'infinite_wp', default=True)

class WaccaGateConfig():
    def __init__(self, parent_config: "WaccaConfig") -> None:
        self.__config = parent_config

    @property
    def enabled_gates(self) -> List[int]:
        return CoreConfig.get_config_field(self.__config, 'wacca', 'gates', 'enabled_gates', default=[])

class WaccaConfig(dict):
    def __init__(self) -> None:
        self.server = WaccaServerConfig(self)
        self.mods = WaccaModsConfig(self)
        self.gates = WaccaGateConfig(self)
