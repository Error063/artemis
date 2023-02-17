from core.config import CoreConfig

class OngekiServerConfig():
    def __init__(self, parent_config: "OngekiConfig") -> None:
        self.__config = parent_config
    
    @property
    def enable(self) -> bool:
        return CoreConfig.get_config_field(self.__config, 'ongeki', 'server', 'enable', default=True)
    
    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(CoreConfig.get_config_field(self.__config, 'ongeki', 'server', 'loglevel', default="info"))

class OngekiConfig(dict):
    def __init__(self) -> None:
        self.server = OngekiServerConfig(self)
