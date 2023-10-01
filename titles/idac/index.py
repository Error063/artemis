import json
import traceback
import inflection
import yaml
import logging
import coloredlogs

from os import path
from typing import Dict, Tuple
from logging.handlers import TimedRotatingFileHandler
from twisted.web import server
from twisted.web.http import Request
from twisted.internet import reactor, endpoints

from core.config import CoreConfig
from core.utils import Utils
from titles.idac.base import IDACBase
from titles.idac.season2 import IDACSeason2
from titles.idac.config import IDACConfig
from titles.idac.const import IDACConstants
from titles.idac.echo import IDACEchoUDP
from titles.idac.matching import IDACMatching


class IDACServlet:
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = IDACConfig()
        self.game_cfg.update(
            yaml.safe_load(open(f"{cfg_dir}/{IDACConstants.CONFIG_NAME}"))
        )

        self.versions = [
            IDACBase(core_cfg, self.game_cfg),
            IDACSeason2(core_cfg, self.game_cfg)
        ]

        self.logger = logging.getLogger("idac")
        log_fmt_str = "[%(asctime)s] IDAC | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        fileHandler = TimedRotatingFileHandler(
            "{0}/{1}.log".format(self.core_cfg.server.log_dir, "idac"),
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

    @classmethod
    def get_allnet_info(
        cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str
    ) -> Tuple[bool, str, str]:
        game_cfg = IDACConfig()

        if path.exists(f"{cfg_dir}/{IDACConstants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{IDACConstants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return (False, "", "")

        if core_cfg.server.is_develop:
            return (
                True,
                f"",
                # requires http or else it defautls to https
                f"http://{core_cfg.title.hostname}:{core_cfg.title.port}/{game_code}/$v/",
            )

        return (
            True,
            f"",
            # requires http or else it defautls to https
            f"http://{core_cfg.title.hostname}/{game_code}/$v/",
        )

    def render_POST(self, request: Request, version: int, url_path: str) -> bytes:
        req_raw = request.content.getvalue()
        url_split = url_path.split("/")
        internal_ver = 0
        endpoint = url_split[len(url_split) - 1]
        client_ip = Utils.get_ip_addr(request)

        if version >= 100 and version < 140:  # IDAC Season 1
            internal_ver = IDACConstants.VER_IDAC_SEASON_1
        elif version >= 140 and version < 171:  # IDAC Season 2
            internal_ver = IDACConstants.VER_IDAC_SEASON_2

        if url_split[0] == "initiald":
            header_application = self.decode_header(request.getAllHeaders())

            req_data = json.loads(req_raw)

            self.logger.info(f"v{version} {endpoint} request from {client_ip}")
            self.logger.debug(f"Headers: {header_application}")
            self.logger.debug(req_data)

            # func_to_find = "handle_" + inflection.underscore(endpoint) + "_request"
            func_to_find = "handle_"
            for x in url_split:
                func_to_find += f"{x.lower()}_" if not x == "" and not x == "initiald" else ""
            func_to_find += f"request"

            if not hasattr(self.versions[internal_ver], func_to_find):
                self.logger.warning(f"Unhandled v{version} request {endpoint}")
                return '{"status_code": "0"}'.encode("utf-8")

            resp = None
            try:
                handler = getattr(self.versions[internal_ver], func_to_find)
                resp = handler(req_data, header_application)

            except Exception as e:
                traceback.print_exc()
                self.logger.error(f"Error handling v{version} method {endpoint} - {e}")
                return '{"status_code": "0"}'.encode("utf-8")

            if resp is None:
                resp = {"status_code": "0"}

            self.logger.debug(f"Response {resp}")
            return json.dumps(resp, ensure_ascii=False).encode("utf-8")

        self.logger.warning(
            f"IDAC unknown request {url_path} - {request.content.getvalue().decode()}"
        )
        return '{"status_code": "0"}'.encode("utf-8")

    def decode_header(self, data: Dict) -> Dict:
        app: str = data[b"application"].decode()
        ret = {}

        for x in app.split(", "):
            y = x.split("=")
            ret[y[0]] = y[1].replace('"', "")

        return ret

    def setup(self):
        if self.game_cfg.server.enable:
            endpoints.serverFromString(
                reactor,
                f"tcp:{self.game_cfg.server.matching}:interface={self.core_cfg.server.listen_address}",
            ).listen(server.Site(IDACMatching(self.core_cfg, self.game_cfg)))

            reactor.listenUDP(
                self.game_cfg.server.echo1,
                IDACEchoUDP(self.core_cfg, self.game_cfg, self.game_cfg.server.echo1),
            )
            reactor.listenUDP(
                self.game_cfg.server.echo2,
                IDACEchoUDP(self.core_cfg, self.game_cfg, self.game_cfg.server.echo2),
            )
