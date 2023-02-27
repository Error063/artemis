from twisted.web.http import Request
from twisted.web import resource, server
from twisted.internet import reactor, endpoints
import yaml
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
from titles.pokken.proto import jackal_pb2
from os import path

from core.config import CoreConfig
from titles.pokken.config import PokkenConfig
from titles.pokken.base import PokkenBase

class PokkenServlet(resource.Resource):
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        self.isLeaf = True
        self.core_cfg = core_cfg
        self.config_dir = cfg_dir
        self.game_cfg = PokkenConfig()
        self.game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/pokken.yaml")))

        self.logger = logging.getLogger("pokken")
        if not hasattr(self.logger, "inited"):
            log_fmt_str = "[%(asctime)s] Pokken | %(levelname)s | %(message)s"
            log_fmt = logging.Formatter(log_fmt_str)
            fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.core_cfg.server.log_dir, "pokken"), encoding='utf8',
                when="d", backupCount=10)

            fileHandler.setFormatter(log_fmt)
            
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(log_fmt)

            self.logger.addHandler(fileHandler)
            self.logger.addHandler(consoleHandler)
            
            self.logger.setLevel(self.game_cfg.server.loglevel)
            coloredlogs.install(level=self.game_cfg.server.loglevel, logger=self.logger, fmt=log_fmt_str)
            self.logger.inited = True

        self.base = PokkenBase(core_cfg, self.game_cfg)
    
    def setup(self):
        if self.game_cfg.server.enable:
            key_exists = path.exists(self.game_cfg.server.ssl_key)
            cert_exists = path.exists(self.game_cfg.server.ssl_cert)

            if self.core_cfg.server.is_develop and self.game_cfg.server.ssl_enable and key_exists and cert_exists:
                endpoints.serverFromString(reactor, f"ssl:{self.game_cfg.server.port}"\
                    f":interface={self.game_cfg.server.hostname}:privateKey={self.game_cfg.server.ssl_key}:"\
                        f"certKey={self.game_cfg.server.ssl_cert}")\
                        .listen(server.Site(PokkenServlet(self.core_cfg, self.config_dir)))

            elif self.core_cfg.server.is_develop and self.game_cfg.server.ssl_enable:
                self.logger.error(f"Could not find cert at {self.game_cfg.server.ssl_key} or key at {self.game_cfg.server.ssl_cert}, Pokken not running.")
                return
            
            else:
                endpoints.serverFromString(reactor, f"tcp:{self.game_cfg.server.port}"\
                    f":interface={self.game_cfg.server.hostname}")\
                        .listen(server.Site(PokkenServlet(self.core_cfg, self.config_dir)))

            self.logger.info(f"Pokken title server ready on port {self.game_cfg.server.port}")
    
    def render_POST(self, request: Request, version: int, endpoints: str) -> bytes:
        req_url = request.uri.decode()
        if req_url == "/matching":
            self.logger.info("Matching request")

        pokken_request = jackal_pb2.Request()
        pokken_request.ParseFromString(request.content.getvalue())
        endpoint = jackal_pb2.MessageType(pokken_request.type).name.lower()
        
        self.logger.info(f"{endpoint} request")

        handler = getattr(self.base, f"handle_{endpoint}", None)
        if handler is None:
            self.logger.warn(f"No handler found for message type {endpoint}")
            return self.base.handle_noop(pokken_request)
        return handler(pokken_request)
