from twisted.web.http import Request
import json
import inflection
import yaml
import string
import logging
import coloredlogs
import zlib
from logging.handlers import TimedRotatingFileHandler

from core.config import CoreConfig
from titles.cm.config import CardMakerConfig
from titles.cm.const import CardMakerConstants
from titles.cm.base import CardMakerBase
from titles.cm.cm136 import CardMaker136


class CardMakerServlet():
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        self.core_cfg = core_cfg
        self.game_cfg = CardMakerConfig()
        self.game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/cardmaker.yaml")))

        self.versions = [
            CardMakerBase(core_cfg, self.game_cfg),
            CardMaker136(core_cfg, self.game_cfg)
        ]

        self.logger = logging.getLogger("cardmaker")
        log_fmt_str = "[%(asctime)s] Card Maker | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.core_cfg.server.log_dir, "cardmaker"), encoding='utf8',
                                               when="d", backupCount=10)

        fileHandler.setFormatter(log_fmt)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)

        self.logger.setLevel(self.game_cfg.server.loglevel)
        coloredlogs.install(level=self.game_cfg.server.loglevel,
                            logger=self.logger, fmt=log_fmt_str)

    def render_POST(self, request: Request, version: int, url_path: str) -> bytes:
        req_raw = request.content.getvalue()
        url_split = url_path.split("/")
        internal_ver = 0
        endpoint = url_split[len(url_split) - 1]

        print(f"version: {version}")

        if version >= 130 and version < 135:  # Card Maker
            internal_ver = CardMakerConstants.VER_CARD_MAKER
        elif version >= 135 and version < 140:  # Card Maker
            internal_ver = CardMakerConstants.VER_CARD_MAKER_136

        if all(c in string.hexdigits for c in endpoint) and len(endpoint) == 32:
            # If we get a 32 character long hex string, it's a hash and we're
            # doing encrypted. The likelyhood of false positives is low but
            # technically not 0
            self.logger.error("Encryption not supported at this time")

        try:
            unzip = zlib.decompress(req_raw)

        except zlib.error as e:
            self.logger.error(
                f"Failed to decompress v{version} {endpoint} request -> {e}")
            return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

        req_data = json.loads(unzip)

        self.logger.info(f"v{version} {endpoint} request - {req_data}")

        func_to_find = "handle_" + inflection.underscore(endpoint) + "_request"

        try:
            handler = getattr(self.versions[internal_ver], func_to_find)
            resp = handler(req_data)

        except AttributeError as e:
            self.logger.warning(
                f"Unhandled v{version} request {endpoint} - {e}")
            return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

        except Exception as e:
            self.logger.error(
                f"Error handling v{version} method {endpoint} - {e}")
            return zlib.compress("{\"stat\": \"0\"}".encode("utf-8"))

        if resp is None:
            resp = {'returnCode': 1}

        self.logger.info(f"Response {resp}")

        return zlib.compress(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
