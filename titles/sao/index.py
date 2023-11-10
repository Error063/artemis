from typing import Tuple, Dict, List
from twisted.web.http import Request
import yaml
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
from os import path
from Crypto.Cipher import Blowfish
from hashlib import md5
import random

from core import CoreConfig, Utils
from core.title import BaseServlet
from titles.sao.config import SaoConfig
from titles.sao.const import SaoConstants
from titles.sao.base import SaoBase
from titles.sao.handlers.base import *


class SaoServlet(BaseServlet):
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        super().__init__(core_cfg, cfg_dir)
        self.config_dir = cfg_dir
        self.game_cfg = SaoConfig()
        if path.exists(f"{cfg_dir}/sao.yaml"):
            self.game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/sao.yaml")))

        self.logger = logging.getLogger("sao")
        if not hasattr(self.logger, "inited"):
            log_fmt_str = "[%(asctime)s] SAO | %(levelname)s | %(message)s"
            log_fmt = logging.Formatter(log_fmt_str)
            fileHandler = TimedRotatingFileHandler(
                "{0}/{1}.log".format(self.core_cfg.server.log_dir, "sao"),
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

        self.base = SaoBase(core_cfg, self.game_cfg)
        self.static_hash = None
        
        if self.game_cfg.hash.verify_hash:
            self.static_hash = md5(self.game_cfg.hash.hash_base.encode()).digest() # Greate hashing guys, really validates the data
    
    def get_endpoint_matchers(self) -> Tuple[List[Tuple[str, str, Dict]], List[Tuple[str, str, Dict]]]:
        return (
            [], 
            [("render_POST", "/{datecode}/proto/if/{category}/{endpoint}", {})]
        )
    
    @classmethod
    def is_game_enabled(cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str) -> bool:
        game_cfg = SaoConfig()

        if path.exists(f"{cfg_dir}/{SaoConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{SaoConstants.CONFIG_NAME}"))
            )
    
        if not game_cfg.server.enable:
            return False
        
        return True
    
    def get_allnet_info(self, game_code: str, game_ver: int, keychip: str) -> Tuple[str, str]:
        tport = Utils.get_title_port(self.core_cfg)
        return (
            f"http://{self.core_cfg.title.hostname}:{tport}/",
            f"{self.core_cfg.title.hostname}/",
        )

    def get_mucha_info(self, core_cfg: CoreConfig, cfg_dir: str) -> Tuple[bool, str]:
        if not self.game_cfg.server.enable:
            return (False, "")

        return (True, "SAO1")

    def render_POST(self, request: Request, game_code: str, matchers: Dict) -> bytes:
        endpoint = matchers.get('endpoint', '')
        request.responseHeaders.addRawHeader(b"content-type", b"text/html; charset=utf-8")
        iv = b""

        req_raw = request.content.read()
        sao_request = req_raw.hex()
        req_header = SaoRequestHeader(req_raw)
        
        cmd_str = f"{req_header.cmd:04x}"
        
        if self.game_cfg.hash.verify_hash and self.static_hash != req_header.hash:
            self.logger.error(f"Hash mismatch! Expecting {self.static_hash} but recieved {req_header.hash}")
            return b""
        
        if self.game_cfg.crypt.enable:
            iv = req_raw[40:48]
            cipher = Blowfish.new(self.game_cfg.crypt.key.encode(), Blowfish.MODE_CBC, iv)
            crypt_data = req_raw[48:]
            req_data = cipher.decrypt(crypt_data)
            self.logger.debug(f"Decrypted {req_data.hex()} with IV {iv.hex()}")
            
        else:
            req_data = req_raw[40:]

        handler = getattr(self.base, f"handle_{cmd_str}", None)
        if handler is None:
            self.logger.info(f"Generic Handler for {endpoint} - {cmd_str}")
            self.logger.debug(f"Request: {req_raw.hex()}")
            resp_thing = SaoNoopResponse(req_header.cmd + 1)
            resp = resp_thing.make()
        
        else:
            self.logger.info(f"Handler {endpoint} - {cmd_str} request")
            self.logger.debug(f"Request: {req_raw.hex()}")
            resp = handler(sao_request)
        
        self.logger.debug(f"Response: {resp.hex()}")

        if self.game_cfg.crypt.enable:
            iv = random.randbytes(8)
            data_to_crypt = resp[24:]
            while len(data_to_crypt) % 8 != 0:
                data_to_crypt += b"\x00"
            
            cipher = Blowfish.new(self.game_cfg.crypt.key.encode(), Blowfish.MODE_CBC, iv)
            data_crypt = cipher.encrypt(data_to_crypt)
            crypt_data_len = len(data_crypt)
            tmp = struct.pack("!I", crypt_data_len) # does it want the length of the encrypted response??
            resp = resp[:20] + tmp + iv + data_crypt
            self.logger.debug(f"Encrypted Response: {resp.hex()}")

        return resp