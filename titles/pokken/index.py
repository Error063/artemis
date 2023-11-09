from typing import Tuple, List, Dict
from twisted.web.http import Request
from twisted.web import resource
from twisted.internet import reactor
import json, ast
from datetime import datetime
import yaml
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
import inflection
from os import path
from google.protobuf.message import DecodeError

from core import CoreConfig, Utils
from core.title import BaseServlet
from .config import PokkenConfig
from .base import PokkenBase
from .const import PokkenConstants
from .proto import jackal_pb2
from .services import PokkenAdmissionFactory


class PokkenServlet(BaseServlet):
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        super().__init__(core_cfg, cfg_dir)
        self.config_dir = cfg_dir
        self.game_cfg = PokkenConfig()
        if path.exists(f"{cfg_dir}/pokken.yaml"):
            self.game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/pokken.yaml")))

        self.logger = logging.getLogger("pokken")
        if not hasattr(self.logger, "inited"):
            log_fmt_str = "[%(asctime)s] Pokken | %(levelname)s | %(message)s"
            log_fmt = logging.Formatter(log_fmt_str)
            fileHandler = TimedRotatingFileHandler(
                "{0}/{1}.log".format(self.core_cfg.server.log_dir, "pokken"),
                encoding="utf8",
                when="d",
                backupCount=10,
            )

            fileHandler.setFormatter(log_fmt)

            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(log_fmt)

            self.logger.addHandler(fileHandler)
            self.logger.addHandler(consoleHandler)

            self.logger.setLevel(self.game_cfg.server.loglevel)
            coloredlogs.install(
                level=self.game_cfg.server.loglevel, logger=self.logger, fmt=log_fmt_str
            )
            self.logger.inited = True

        self.base = PokkenBase(core_cfg, self.game_cfg)

    @classmethod
    def is_game_enabled(cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str) -> bool:
        game_cfg = PokkenConfig()

        if path.exists(f"{cfg_dir}/{PokkenConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{PokkenConstants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return False
        
        return True
    
    def get_endpoint_matchers(self) -> Tuple[List[Tuple[str, str, Dict]], List[Tuple[str, str, Dict]]]:
        return (
            [], 
            [
                ("render_POST", "/pokken/", {}),
                ("handle_matching", "/pokken/matching", {}),
            ]
        )
    
    def get_allnet_info(self, game_code: str, game_ver: int, keychip: str) -> Tuple[str, str]:
        if self.game_cfg.ports.game != 443:
            return (
                f"https://{self.game_cfg.server.hostname}:{self.game_cfg.ports.game}/pokken/",
                f"{self.game_cfg.server.hostname}/pokken/",
            )
        return (
            f"https://{self.game_cfg.server.hostname}/pokken/",
            f"{self.game_cfg.server.hostname}/pokken/",
        )

    def get_mucha_info(self, core_cfg: CoreConfig, cfg_dir: str) -> Tuple[bool, str]:
        game_cfg = PokkenConfig()

        if path.exists(f"{cfg_dir}/{PokkenConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{PokkenConstants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return (False, "")

        return (True, "PKF1")

    def setup(self) -> None:
        if self.game_cfg.server.enable_matching:
            reactor.listenTCP(
                self.game_cfg.ports.admission, PokkenAdmissionFactory(self.core_cfg, self.game_cfg)
            )

    def render_POST(self, request: Request, game_code: str, matchers: Dict) -> bytes:
        content = request.content.getvalue()
        if content == b"":
            self.logger.info("Empty request")
            return b""

        pokken_request = jackal_pb2.Request()
        try:
            pokken_request.ParseFromString(content)
        except DecodeError as e:
            self.logger.warning(f"{e} {content}")
            return b""

        endpoint = jackal_pb2.MessageType.DESCRIPTOR.values_by_number[
            pokken_request.type
        ].name.lower()

        self.logger.debug(pokken_request)

        handler = getattr(self.base, f"handle_{endpoint}", None)
        if handler is None:
            self.logger.warning(f"No handler found for message type {endpoint}")
            return self.base.handle_noop(pokken_request)

        self.logger.info(f"{endpoint} request from {Utils.get_ip_addr(request)}")

        ret = handler(pokken_request)
        return ret

    def handle_matching(self, request: Request, game_code: str, matchers: Dict) -> bytes:
        if not self.game_cfg.server.enable_matching:
            return b""
        
        content = request.content.getvalue()
        client_ip = Utils.get_ip_addr(request)

        if content is None or content == b"":
            self.logger.info("Empty matching request")
            return json.dumps(self.base.handle_matching_noop()).encode()

        json_content = ast.literal_eval(
            content.decode()
            .replace("null", "None")
            .replace("true", "True")
            .replace("false", "False")
        )
        self.logger.info(f"Matching {json_content['call']} request")
        self.logger.debug(json_content)

        handler = getattr(
            self.base,
            f"handle_matching_{inflection.underscore(json_content['call'])}",
            None,
        )
        if handler is None:
            self.logger.warning(
                f"No handler found for message type {json_content['call']}"
            )
            return json.dumps(self.base.handle_matching_noop()).encode()

        ret = handler(json_content, client_ip)

        if ret is None:
            ret = {}
        if "result" not in ret:
            ret["result"] = "true"
        if "data" not in ret:
            ret["data"] = {}
        if "timestamp" not in ret:
            ret["timestamp"] = int(datetime.now().timestamp() * 1000)

        self.logger.debug(f"Response {ret}")

        return json.dumps(ret).encode()
