from twisted.web.http import Request
import yaml
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
import zlib
import json
import urllib.parse
import base64
from os import path
from typing import Tuple, Dict, List

from core.config import CoreConfig
from core.title import BaseServlet
from core.utils import Utils
from .config import DivaConfig
from .const import DivaConstants
from .base import DivaBase


class DivaServlet(BaseServlet):
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        super().__init__(core_cfg, cfg_dir)
        self.game_cfg = DivaConfig()
        if path.exists(f"{cfg_dir}/{DivaConstants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{DivaConstants.CONFIG_NAME}"))
            )

        self.base = DivaBase(core_cfg, self.game_cfg)

        self.logger = logging.getLogger("diva")
        log_fmt_str = "[%(asctime)s] Diva | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        fileHandler = TimedRotatingFileHandler(
            "{0}/{1}.log".format(self.core_cfg.server.log_dir, "diva"),
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

    def get_endpoint_matchers(self) -> Tuple[List[Tuple[str, str, Dict]], List[Tuple[str, str, Dict]]]:
        return (
            [], 
            [("render_POST", "/DivaServlet/", {})]
        )
    
    def get_allnet_info(self, game_code: str, game_ver: int, keychip: str) -> Tuple[str, str]:
        if not self.core_cfg.server.is_using_proxy and Utils.get_title_port(self.core_cfg) != 80:
            return (f"http://{self.core_cfg.title.hostname}:{Utils.get_title_port(self.core_cfg)}/DivaServlet/", "")

        return (f"http://{self.core_cfg.title.hostname}/DivaServlet/", "")

    @classmethod
    def is_game_enabled(
        cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str
    ) -> bool:
        game_cfg = DivaConfig()
        if path.exists(f"{cfg_dir}/{DivaConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{DivaConstants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return False

        return True

    def render_POST(self, request: Request, game_code: str, matchers: Dict) -> bytes:
        req_raw = request.content.getvalue()
        url_header = request.getAllHeaders()

        # Ping Dispatch
        if "THIS_STRING_SEPARATES" in str(url_header):
            binary_request = req_raw.splitlines()
            binary_cmd_decoded = binary_request[3].decode("utf-8")
            binary_array = binary_cmd_decoded.split("&")

            bin_req_data = {}

            for kvp in binary_array:
                split_bin = kvp.split("=")
                bin_req_data[split_bin[0]] = split_bin[1]

            self.logger.info(f"Binary {bin_req_data['cmd']} Request")
            self.logger.debug(bin_req_data)

            handler = getattr(self.base, f"handle_{bin_req_data['cmd']}_request")
            resp = handler(bin_req_data)

            self.logger.debug(
                f"Response cmd={bin_req_data['cmd']}&req_id={bin_req_data['req_id']}&stat=ok{resp}"
            )
            return f"cmd={bin_req_data['cmd']}&req_id={bin_req_data['req_id']}&stat=ok{resp}".encode(
                "utf-8"
            )

        # Main Dispatch
        json_string = json.dumps(
            req_raw.decode("utf-8")
        )  # Take the response and decode as UTF-8 and dump
        b64string = json_string.replace(
            r"\n", "\n"
        )  # Remove all \n and separate them as new lines
        gz_string = base64.b64decode(b64string)  # Decompressing the base64 string

        try:
            url_data = zlib.decompress(gz_string).decode(
                "utf-8"
            )  # Decompressing the gzip
        except zlib.error as e:
            self.logger.error(f"Failed to defalte! {e} -> {gz_string}")
            return "stat=0"

        req_kvp = urllib.parse.unquote(url_data)
        req_data = {}

        # We then need to split each parts with & so we can reuse them to fill out the requests
        splitted_request = str.split(req_kvp, "&")
        for kvp in splitted_request:
            split = kvp.split("=")
            req_data[split[0]] = split[1]

        self.logger.info(f"{req_data['cmd']} Request")
        self.logger.debug(req_data)

        func_to_find = f"handle_{req_data['cmd']}_request"

        # Load the requests
        try:
            handler = getattr(self.base, func_to_find)
            resp = handler(req_data)

        except AttributeError as e:
            self.logger.warning(f"Unhandled {req_data['cmd']} request {e}")
            return f"cmd={req_data['cmd']}&req_id={req_data['req_id']}&stat=ok".encode(
                "utf-8"
            )

        except Exception as e:
            self.logger.error(f"Error handling method {func_to_find} {e}")
            return f"cmd={req_data['cmd']}&req_id={req_data['req_id']}&stat=ok".encode(
                "utf-8"
            )

        request.responseHeaders.addRawHeader(b"content-type", b"text/plain")
        self.logger.debug(
            f"Response cmd={req_data['cmd']}&req_id={req_data['req_id']}&stat=ok{resp}"
        )

        return (
            f"cmd={req_data['cmd']}&req_id={req_data['req_id']}&stat=ok{resp}".encode(
                "utf-8"
            )
        )
