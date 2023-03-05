from typing import Tuple
from twisted.web.http import Request
from twisted.web import resource, server
from twisted.internet import reactor, endpoints
import yaml
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
from titles.pokken.proto import jackal_pb2
from os import path
from google.protobuf.message import DecodeError

from core.config import CoreConfig
from titles.pokken.config import PokkenConfig
from titles.pokken.base import PokkenBase
from titles.pokken.const import PokkenConstants

class PokkenServlet(resource.Resource):
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        self.isLeaf = True
        self.core_cfg = core_cfg
        self.config_dir = cfg_dir
        self.game_cfg = PokkenConfig()
        if path.exists(f"{cfg_dir}/pokken.yaml"):
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

    @classmethod
    def get_allnet_info(cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str) -> Tuple[bool, str, str]:
        game_cfg = PokkenConfig()
        
        if path.exists(f"{cfg_dir}/{PokkenConstants.CONFIG_NAME}"):
            game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/{PokkenConstants.CONFIG_NAME}")))

        if not game_cfg.server.enable:
            return (False, "", "")
        
        if core_cfg.server.is_develop:
            return (True, f"https://{game_cfg.server.hostname}:{game_cfg.server.port}/{game_code}/$v/", f"{game_cfg.server.hostname}:{game_cfg.server.port}/")
        
        return (True, f"https://{game_cfg.server.hostname}/{game_code}/$v/", f"{game_cfg.server.hostname}/")
    
    def setup(self):
        """
        There's currently no point in having this server on because Twisted
        won't play ball with both the fact that it's TLSv1.1, and because the 
        types of certs that pokken will accept are too flimsy for Twisted
        so it will throw a fit. Currently leaving this here in case a bypass
        is discovered in the future, but it's unlikly. For now, just use NGINX.
        """
        if self.game_cfg.server.enable and self.core_cfg.server.is_develop:    
            key_exists = path.exists(self.game_cfg.server.ssl_key)
            cert_exists = path.exists(self.game_cfg.server.ssl_cert)
            
            if key_exists and cert_exists:
                endpoints.serverFromString(reactor, f"ssl:{self.game_cfg.server.port}"\
                    f":interface={self.core_cfg.server.listen_address}:privateKey={self.game_cfg.server.ssl_key}:"\
                        f"certKey={self.game_cfg.server.ssl_cert}")\
                        .listen(server.Site(self))
                
                self.logger.info(f"Pokken title server ready on port {self.game_cfg.server.port}")

            else:
                self.logger.error(f"Could not find cert at {self.game_cfg.server.ssl_key} or key at {self.game_cfg.server.ssl_cert}, Pokken not running.")

    def render_POST(self, request: Request, version: int = 0, endpoints: str = "") -> bytes:
        if endpoints == "":
            endpoints = request.uri.decode()
        if endpoints.startswith("/matching"):
            self.logger.info("Matching request")
        
        content = request.content.getvalue()
        if content == b"":
            self.logger.info("Empty request")
            return b""

        pokken_request = jackal_pb2.Request()
        try:
            pokken_request.ParseFromString(content)
        except DecodeError as e:
            self.logger.warn(f"{e} {content}")
            return b""

        endpoint = jackal_pb2.MessageType(pokken_request.type).name.lower()
        
        self.logger.info(f"{endpoint} request")

        handler = getattr(self.base, f"handle_{endpoint}", None)
        if handler is None:
            self.logger.warn(f"No handler found for message type {endpoint}")
            return self.base.handle_noop(pokken_request)
        return handler(pokken_request)
