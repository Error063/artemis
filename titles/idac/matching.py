import json
import logging

from typing import Dict
from twisted.web import resource

from core import CoreConfig
from titles.idac.season2 import IDACBase
from titles.idac.config import IDACConfig


class IDACMatching(resource.Resource):
    isLeaf = True

    def __init__(self, cfg: CoreConfig, game_cfg: IDACConfig) -> None:
        self.core_config = cfg
        self.game_config = game_cfg
        self.base = IDACBase(cfg, game_cfg)
        self.logger = logging.getLogger("idac")

        self.queue = 0

    def get_matching_state(self):
        if self.queue >= 1:
            self.queue -= 1
            return 0
        else:
            return 1

    def render_POST(self, req) -> bytes:
        url = req.uri.decode()
        req_data = json.loads(req.content.getvalue().decode())
        header_application = self.decode_header(req.getAllHeaders())
        user_id = int(header_application["session"])

        # self.getMatchingStatus(user_id)

        self.logger.info(
            f"IDAC Matching request from {req.getClientIP()}: {url} - {req_data}"
        )

        resp = {"status_code": "0"}
        if url == "/regist":
            self.queue = self.queue + 1
        elif url == "/status":
            if req_data.get("cancel_flag"):
                self.queue = self.queue - 1
                self.logger.info(
                    f"IDAC Matching endpoint {req.getClientIP()} had quited"
                )

            resp = {
                "status_code": "0",
                # Only IPv4 is supported
                "host": self.game_config.server.matching_host,
                "port": self.game_config.server.matching_p2p,
                "room_name": "INDTA",
                "state": 1,
            }

        self.logger.debug(f"Response {resp}")
        return json.dumps(resp, ensure_ascii=False).encode("utf-8")

    def decode_header(self, data: Dict) -> Dict:
        app: str = data[b"application"].decode()
        ret = {}

        for x in app.split(", "):
            y = x.split("=")
            ret[y[0]] = y[1].replace('"', "")

        return ret
