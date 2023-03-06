from core.config import CoreConfig

class PokkenServerConfig():
    def __init__(self, parent_config: "PokkenConfig"):
        self.__config = parent_config
    
    @property
    def hostname(self) -> str:
        return CoreConfig.get_config_field(self.__config, 'pokken', 'server', 'hostname', default="localhost")
    
    @property
    def enable(self) -> bool:
        return CoreConfig.get_config_field(self.__config, 'pokken', 'server', 'enable', default=True)

    @property
    def loglevel(self) -> int:
        return CoreConfig.str_to_loglevel(CoreConfig.get_config_field(self.__config, 'pokken', 'server', 'loglevel', default="info"))

    @property
    def port(self) -> int:
        return CoreConfig.get_config_field(self.__config, 'pokken', 'server', 'port', default=9000)

    @property
    def port_matching(self) -> int:
        return CoreConfig.get_config_field(self.__config, 'pokken', 'server', 'port_matching', default=9001)

    @property
    def port_stun(self) -> int:
        return CoreConfig.get_config_field(self.__config, 'pokken', 'server', 'port_stun', default=9002)

    @property
    def port_turn(self) -> int:
        return CoreConfig.get_config_field(self.__config, 'pokken', 'server', 'port_turn', default=9003)

    @property
    def port_admission(self) -> int:
        return CoreConfig.get_config_field(self.__config, 'pokken', 'server', 'port_admission', default=9004)
    
    @property
    def ssl_cert(self) -> str:
        return CoreConfig.get_config_field(self.__config, 'pokken', 'server', 'ssl_cert', default="cert/pokken.crt")

    @property
    def ssl_key(self) -> str:
        return CoreConfig.get_config_field(self.__config, 'pokken', 'server', 'ssl_key', default="cert/pokken.key")

class PokkenConfig(dict):
    def __init__(self) -> None:
        self.server = PokkenServerConfig(self)
