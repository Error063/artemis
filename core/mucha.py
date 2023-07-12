from typing import Dict, Any, Optional, List
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
from twisted.web import resource
from twisted.web.http import Request
from datetime import datetime
from Crypto.Cipher import Blowfish
import pytz

from core import CoreConfig
from core.utils import Utils


class MuchaServlet:
    def __init__(self, cfg: CoreConfig, cfg_dir: str) -> None:
        self.config = cfg
        self.config_dir = cfg_dir
        self.mucha_registry: List[str] = []

        self.logger = logging.getLogger("mucha")
        log_fmt_str = "[%(asctime)s] Mucha | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)

        fileHandler = TimedRotatingFileHandler(
            "{0}/{1}.log".format(self.config.server.log_dir, "mucha"),
            when="d",
            backupCount=10,
        )
        fileHandler.setFormatter(log_fmt)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)

        self.logger.setLevel(cfg.mucha.loglevel)
        coloredlogs.install(level=cfg.mucha.loglevel, logger=self.logger, fmt=log_fmt_str)

        all_titles = Utils.get_all_titles()

        for _, mod in all_titles.items():
            if hasattr(mod, "index") and hasattr(mod.index, "get_mucha_info"):
                enabled, game_cd = mod.index.get_mucha_info(
                    self.config, self.config_dir
                )
                if enabled:
                    self.mucha_registry.append(game_cd)

        self.logger.info(f"Serving {len(self.mucha_registry)} games")

    def handle_boardauth(self, request: Request, _: Dict) -> bytes:
        req_dict = self.mucha_preprocess(request.content.getvalue())
        client_ip = Utils.get_ip_addr(request)

        if req_dict is None:
            self.logger.error(
                f"Error processing mucha request {request.content.getvalue()}"
            )
            return b"RESULTS=000"

        req = MuchaAuthRequest(req_dict)
        self.logger.info(f"Boardauth request from {client_ip} for {req.gameVer}")        
        self.logger.debug(f"Mucha request {vars(req)}")

        if req.gameCd not in self.mucha_registry:
            self.logger.warn(f"Unknown gameCd {req.gameCd}")
            return b"RESULTS=000"

        # TODO: Decrypt S/N

        #cipher = Blowfish.new(req.sendDate.encode(), Blowfish.MODE_ECB)
        #sn_decrypt = cipher.decrypt(bytes.fromhex(req.serialNum))
        #self.logger.debug(f"Decrypt SN to {sn_decrypt.hex()}")

        resp = MuchaAuthResponse(
            f"{self.config.mucha.hostname}{':' + str(self.config.allnet.port) if self.config.server.is_develop else ''}"
        )

        self.logger.debug(f"Mucha response {vars(resp)}")

        return self.mucha_postprocess(vars(resp))

    def handle_updatecheck(self, request: Request, _: Dict) -> bytes:
        req_dict = self.mucha_preprocess(request.content.getvalue())
        client_ip = Utils.get_ip_addr(request)

        if req_dict is None:
            self.logger.error(
                f"Error processing mucha request {request.content.getvalue()}"
            )
            return b"RESULTS=000"

        req = MuchaUpdateRequest(req_dict)
        self.logger.info(f"Updatecheck request from {client_ip} for {req.gameVer}")        
        self.logger.debug(f"Mucha request {vars(req)}")

        if req.gameCd not in self.mucha_registry:
            self.logger.warn(f"Unknown gameCd {req.gameCd}")
            return b"RESULTS=000"

        resp = MuchaUpdateResponse(req.gameVer, f"{self.config.mucha.hostname}{':' + str(self.config.allnet.port) if self.config.server.is_develop else ''}")

        self.logger.debug(f"Mucha response {vars(resp)}")

        return self.mucha_postprocess(vars(resp))

    def handle_dlstate(self, request: Request, _: Dict) -> bytes:
        req_dict = self.mucha_preprocess(request.content.getvalue())
        client_ip = Utils.get_ip_addr(request)

        if req_dict is None:
            self.logger.error(
                f"Error processing mucha request {request.content.getvalue()}"
            )
            return b""
        
        req = MuchaDownloadStateRequest(req_dict)
        self.logger.info(f"DownloadState request from {client_ip} for {req.gameCd} -> {req.updateVer}")        
        self.logger.debug(f"request {vars(req)}")
        return b"RESULTS=001"

    def mucha_preprocess(self, data: bytes) -> Optional[Dict]:
        try:
            ret: Dict[str, Any] = {}

            for x in data.decode().split("&"):
                kvp = x.split("=")
                if len(kvp) == 2:
                    ret[kvp[0]] = kvp[1]

            return ret

        except:
            self.logger.error(f"Error processing mucha request {data}")
            return None

    def mucha_postprocess(self, data: dict) -> Optional[bytes]:
        try:
            urlencode = ""
            for k, v in data.items():
                urlencode += f"{k}={v}&"

            return urlencode.encode()

        except:
            self.logger.error("Error processing mucha response")
            return None


class MuchaAuthRequest:
    def __init__(self, request: Dict) -> None:
        # gameCd + boardType + countryCd + version
        self.gameVer = request.get("gameVer", "")
        self.sendDate = request.get("sendDate", "")  # %Y%m%d
        self.serialNum = request.get("serialNum", "")
        self.gameCd = request.get("gameCd", "")
        self.boardType = request.get("boardType", "")
        self.boardId = request.get("boardId", "")
        self.mac = request.get("mac", "")
        self.placeId = request.get("placeId", "")
        self.storeRouterIp = request.get("storeRouterIp", "")
        self.countryCd = request.get("countryCd", "")
        self.useToken = request.get("useToken", "")
        self.allToken = request.get("allToken", "")


class MuchaAuthResponse:
    def __init__(self, mucha_url: str) -> None:
        self.RESULTS = "001"
        self.AUTH_INTERVAL = "86400"
        self.SERVER_TIME = datetime.strftime(datetime.now(), "%Y%m%d%H%M")
        self.UTC_SERVER_TIME = datetime.strftime(datetime.now(pytz.UTC), "%Y%m%d%H%M")

        self.CHARGE_URL = f"https://{mucha_url}/charge/"
        self.FILE_URL = f"https://{mucha_url}/file/"
        self.URL_1 = f"https://{mucha_url}/url1/"
        self.URL_2 = f"https://{mucha_url}/url2/"
        self.URL_3 = f"https://{mucha_url}/url3/"

        self.PLACE_ID = "JPN123"
        self.COUNTRY_CD = "JPN"
        self.SHOP_NAME = "TestShop!"
        self.SHOP_NICKNAME = "TestShop"
        self.AREA_0 = "008"
        self.AREA_1 = "009"
        self.AREA_2 = "010"
        self.AREA_3 = "011"
        self.AREA_FULL_0 = ""
        self.AREA_FULL_1 = ""
        self.AREA_FULL_2 = ""
        self.AREA_FULL_3 = ""

        self.SHOP_NAME_EN = "TestShop!"
        self.SHOP_NICKNAME_EN = "TestShop"
        self.AREA_0_EN = "008"
        self.AREA_1_EN = "009"
        self.AREA_2_EN = "010"
        self.AREA_3_EN = "011"
        self.AREA_FULL_0_EN = ""
        self.AREA_FULL_1_EN = ""
        self.AREA_FULL_2_EN = ""
        self.AREA_FULL_3_EN = ""

        self.PREFECTURE_ID = "1"
        self.EXPIRATION_DATE = "null"
        self.USE_TOKEN = "0"
        self.CONSUME_TOKEN = "0"
        self.DONGLE_FLG = "1"
        self.FORCE_BOOT = "0"


class MuchaUpdateRequest:
    def __init__(self, request: Dict) -> None:
        self.gameVer = request.get("gameVer", "")
        self.gameCd = request.get("gameCd", "")
        self.serialNum = request.get("serialNum", "")
        self.countryCd = request.get("countryCd", "")
        self.placeId = request.get("placeId", "")
        self.storeRouterIp = request.get("storeRouterIp", "")


class MuchaUpdateResponse:
    def __init__(self, game_ver: str, mucha_url: str) -> None:
        self.RESULTS = "001"        
        self.EXE_VER = game_ver

        self.UPDATE_VER_1 = game_ver
        self.UPDATE_URL_1 = f"http://{mucha_url}/updUrl1/"
        self.UPDATE_SIZE_1 = "20"

        self.CHECK_CRC_1 = "0000000000000000"
        self.CHECK_URL_1 = f"http://{mucha_url}/checkUrl/"
        self.CHECK_SIZE_1 = "20"

        self.INFO_SIZE_1 = "0"
        self.COM_SIZE_1 = "0"
        self.COM_TIME_1 = "0"
        self.LAN_INFO_SIZE_1 = "0"

        self.USER_ID = ""
        self.PASSWORD = ""

"""
RESULTS
EXE_VER

UPDATE_VER_%d
UPDATE_URL_%d
UPDATE_SIZE_%d

CHECK_CRC_%d
CHECK_URL_%d
CHECK_SIZE_%d

INFO_SIZE_1
COM_SIZE_1
COM_TIME_1
LAN_INFO_SIZE_1

USER_ID
PASSWORD
"""
class MuchaUpdateResponseStub:
    def __init__(self, game_ver: str) -> None:
        self.RESULTS = "001"
        self.UPDATE_VER_1 = game_ver

class MuchaDownloadStateRequest:
    def __init__(self, request: Dict) -> None:        
        self.gameCd = request.get("gameCd", "")
        self.updateVer = request.get("updateVer", "")
        self.serialNum = request.get("serialNum", "")
        self.fileSize = request.get("fileSize", "")
        self.compFileSize = request.get("compFileSize", "")
        self.boardId = request.get("boardId", "")
        self.placeId = request.get("placeId", "")
        self.storeRouterIp = request.get("storeRouterIp", "")
