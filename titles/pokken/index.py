from typing import Tuple
from twisted.web.http import Request
from twisted.web import resource
import json, ast
from datetime import datetime
import yaml
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
import inflection
from os import path
from google.protobuf.message import DecodeError

from core import CoreConfig, Utils
from titles.pokken.config import PokkenConfig
from titles.pokken.base import PokkenBase
from titles.pokken.const import PokkenConstants
from titles.pokken.proto import jackal_pb2


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
    def get_allnet_info(
        cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str
    ) -> Tuple[bool, str, str]:
        game_cfg = PokkenConfig()

        if path.exists(f"{cfg_dir}/{PokkenConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{PokkenConstants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return (False, "", "")

        return (
            True,
            f"https://{game_cfg.server.hostname}:{game_cfg.server.port}/{game_code}/$v/",
            f"{game_cfg.server.hostname}/SDAK/$v/",
        )

    @classmethod
    def get_mucha_info(
        cls, core_cfg: CoreConfig, cfg_dir: str
    ) -> Tuple[bool, str, str]:
        game_cfg = PokkenConfig()

        if path.exists(f"{cfg_dir}/{PokkenConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{PokkenConstants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return (False, "")

        return (True, "PKF2")

    def setup(self) -> None:
        # TODO: Setup stun, turn (UDP) and admission (WSS) servers
        pass

    def render_POST(
        self, request: Request, version: int = 0, endpoints: str = ""
    ) -> bytes:
        if endpoints == "matching":
            return self.handle_matching(request)

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

        endpoint = jackal_pb2.MessageType.DESCRIPTOR.values_by_number[
            pokken_request.type
        ].name.lower()

        handler = getattr(self.base, f"handle_{endpoint}", None)
        if handler is None:
            self.logger.warn(f"No handler found for message type {endpoint}")
            return self.base.handle_noop(pokken_request)
        
        self.logger.info(f"{endpoint} request from {Utils.get_ip_addr(request)}")
        self.logger.debug(pokken_request)
        
        ret = handler(pokken_request)
        self.logger.debug(f"Response: {ret}")
        return ret
    
    def handle_matching(self, request: Request) -> bytes:
        content = request.content.getvalue()
        client_ip = Utils.get_ip_addr(request)

        if content is None or content == b"":
            self.logger.info("Empty matching request")
            return json.dumps(self.base.handle_matching_noop()).encode()

        json_content = ast.literal_eval(content.decode().replace('null', 'None').replace('true', 'True').replace('false', 'False'))
        self.logger.info(f"Matching {json_content['call']} request")
        self.logger.debug(json_content)

        handler = getattr(self.base, f"handle_matching_{inflection.underscore(json_content['call'])}", None)
        if handler is None:
            self.logger.warn(f"No handler found for message type {json_content['call']}")
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
