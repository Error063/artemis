from typing import Dict, List, Any, Optional, Tuple
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
from twisted.web.http import Request
from datetime import datetime
import pytz
import base64
import zlib
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from time import strptime

from core.config import CoreConfig
from core.data import Data
from core.utils import Utils
from core.const import *


class AllnetServlet:
    def __init__(self, core_cfg: CoreConfig, cfg_folder: str):
        super().__init__()
        self.config = core_cfg
        self.config_folder = cfg_folder
        self.data = Data(core_cfg)
        self.uri_registry: Dict[str, Tuple[str, str]] = {}

        self.logger = logging.getLogger("allnet")
        if not hasattr(self.logger, "initialized"):
            log_fmt_str = "[%(asctime)s] Allnet | %(levelname)s | %(message)s"
            log_fmt = logging.Formatter(log_fmt_str)

            fileHandler = TimedRotatingFileHandler(
                "{0}/{1}.log".format(self.config.server.log_dir, "allnet"),
                when="d",
                backupCount=10,
            )
            fileHandler.setFormatter(log_fmt)

            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(log_fmt)

            self.logger.addHandler(fileHandler)
            self.logger.addHandler(consoleHandler)

            self.logger.setLevel(core_cfg.allnet.loglevel)
            coloredlogs.install(
                level=core_cfg.allnet.loglevel, logger=self.logger, fmt=log_fmt_str
            )
            self.logger.initialized = True

        plugins = Utils.get_all_titles()

        if len(plugins) == 0:
            self.logger.error("No games detected!")

        for _, mod in plugins.items():
            if hasattr(mod.index, "get_allnet_info"):
                for code in mod.game_codes:
                    enabled, uri, host = mod.index.get_allnet_info(
                        code, self.config, self.config_folder
                    )

                    if enabled:
                        self.uri_registry[code] = (uri, host)

        self.logger.info(
            f"Allnet serving {len(self.uri_registry)} games on port {core_cfg.allnet.port}"
        )

    def handle_poweron(self, request: Request, _: Dict):
        request_ip = request.getClientAddress().host
        try:
            req_dict = self.allnet_req_to_dict(request.content.getvalue())
            if req_dict is None:
                raise AllnetRequestException()

            req = AllnetPowerOnRequest(req_dict[0])
            # Validate the request. Currently we only validate the fields we plan on using

            if not req.game_id or not req.ver or not req.serial or not req.ip:
                raise AllnetRequestException(
                    f"Bad auth request params from {request_ip} - {vars(req)}"
                )

        except AllnetRequestException as e:
            if e.message != "":
                self.logger.error(e)
            return b""

        if req.format_ver == "3":
            resp = AllnetPowerOnResponse3(req.token)
        else:
            resp = AllnetPowerOnResponse2()

        self.logger.debug(f"Allnet request: {vars(req)}")
        if req.game_id not in self.uri_registry:
            msg = f"Unrecognised game {req.game_id} attempted allnet auth from {request_ip}."
            self.data.base.log_event(
                "allnet", "ALLNET_AUTH_UNKNOWN_GAME", logging.WARN, msg
            )
            self.logger.warn(msg)

            resp.stat = 0
            return self.dict_to_http_form_string([vars(resp)])

        resp.uri, resp.host = self.uri_registry[req.game_id]

        machine = self.data.arcade.get_machine(req.serial)
        if machine is None and not self.config.server.allow_unregistered_serials:
            msg = f"Unrecognised serial {req.serial} attempted allnet auth from {request_ip}."
            self.data.base.log_event(
                "allnet", "ALLNET_AUTH_UNKNOWN_SERIAL", logging.WARN, msg
            )
            self.logger.warn(msg)

            resp.stat = 0
            return self.dict_to_http_form_string([vars(resp)])

        if machine is not None:
            arcade = self.data.arcade.get_arcade(machine["arcade"])
            country = (
                arcade["country"] if machine["country"] is None else machine["country"]
            )
            if country is None:
                country = AllnetCountryCode.JAPAN.value

            resp.country = country
            resp.place_id = arcade["id"]
            resp.allnet_id = machine["id"]
            resp.name = arcade["name"] if arcade["name"] is not None else ""
            resp.nickname = arcade["nickname"] if arcade["nickname"] is not None else ""
            resp.region0 = (
                arcade["region_id"]
                if arcade["region_id"] is not None
                else AllnetJapanRegionId.AICHI.value
            )
            resp.region_name0 = (
                arcade["country"]
                if arcade["country"] is not None
                else AllnetCountryCode.JAPAN.value
            )
            resp.region_name1 = (
                arcade["state"]
                if arcade["state"] is not None
                else AllnetJapanRegionId.AICHI.name
            )
            resp.region_name2 = arcade["city"] if arcade["city"] is not None else ""
            resp.client_timezone = (
                arcade["timezone"] if arcade["timezone"] is not None else "+0900"
            )

        int_ver = req.ver.replace(".", "")
        resp.uri = resp.uri.replace("$v", int_ver)
        resp.host = resp.host.replace("$v", int_ver)

        msg = f"{req.serial} authenticated from {request_ip}: {req.game_id} v{req.ver}"
        self.data.base.log_event("allnet", "ALLNET_AUTH_SUCCESS", logging.INFO, msg)
        self.logger.info(msg)
        self.logger.debug(f"Allnet response: {vars(resp)}")

        return self.dict_to_http_form_string([vars(resp)]).encode("utf-8")

    def handle_dlorder(self, request: Request, _: Dict):
        request_ip = request.getClientAddress().host
        try:
            req_dict = self.allnet_req_to_dict(request.content.getvalue())
            if req_dict is None:
                raise AllnetRequestException()

            req = AllnetDownloadOrderRequest(req_dict[0])
            # Validate the request. Currently we only validate the fields we plan on using

            if not req.game_id or not req.ver or not req.serial:
                raise AllnetRequestException(
                    f"Bad download request params from {request_ip} - {vars(req)}"
                )

        except AllnetRequestException as e:
            if e.message != "":
                self.logger.error(e)
            return b""

        resp = AllnetDownloadOrderResponse()
        if not self.config.allnet.allow_online_updates:
            return self.dict_to_http_form_string([vars(resp)])

        else:  # TODO: Actual dlorder response
            return self.dict_to_http_form_string([vars(resp)])

    def handle_billing_request(self, request: Request, _: Dict):
        req_dict = self.billing_req_to_dict(request.content.getvalue())
        request_ip = request.getClientAddress()
        if req_dict is None:
            self.logger.error(f"Failed to parse request {request.content.getvalue()}")
            return b""

        self.logger.debug(f"request {req_dict}")

        rsa = RSA.import_key(open(self.config.billing.signing_key, "rb").read())
        signer = PKCS1_v1_5.new(rsa)
        digest = SHA.new()

        kc_playlimit = int(req_dict[0]["playlimit"])
        kc_nearfull = int(req_dict[0]["nearfull"])
        kc_billigtype = int(req_dict[0]["billingtype"])
        kc_playcount = int(req_dict[0]["playcnt"])
        kc_serial: str = req_dict[0]["keychipid"]
        kc_game: str = req_dict[0]["gameid"]
        kc_date = strptime(req_dict[0]["date"], "%Y%m%d%H%M%S")
        kc_serial_bytes = kc_serial.encode()

        machine = self.data.arcade.get_machine(kc_serial)
        if machine is None and not self.config.server.allow_unregistered_serials:
            msg = f"Unrecognised serial {kc_serial} attempted billing checkin from {request_ip} for game {kc_game}."
            self.data.base.log_event(
                "allnet", "BILLING_CHECKIN_NG_SERIAL", logging.WARN, msg
            )
            self.logger.warn(msg)

            resp = BillingResponse("", "", "", "")
            resp.result = "1"
            return self.dict_to_http_form_string([vars(resp)])

        msg = (
            f"Billing checkin from {request.getClientIP()}: game {kc_game} keychip {kc_serial} playcount "
            f"{kc_playcount} billing_type {kc_billigtype} nearfull {kc_nearfull} playlimit {kc_playlimit}"
        )
        self.logger.info(msg)
        self.data.base.log_event("billing", "BILLING_CHECKIN_OK", logging.INFO, msg)

        while kc_playcount > kc_playlimit:
            kc_playlimit += 1024
            kc_nearfull += 1024

        playlimit = kc_playlimit
        nearfull = kc_nearfull + (kc_billigtype * 0x00010000)

        digest.update(playlimit.to_bytes(4, "little") + kc_serial_bytes)
        playlimit_sig = signer.sign(digest).hex()

        digest = SHA.new()
        digest.update(nearfull.to_bytes(4, "little") + kc_serial_bytes)
        nearfull_sig = signer.sign(digest).hex()

        # TODO: playhistory

        resp = BillingResponse(playlimit, playlimit_sig, nearfull, nearfull_sig)

        resp_str = self.dict_to_http_form_string([vars(resp)], True)
        if resp_str is None:
            self.logger.error(f"Failed to parse response {vars(resp)}")

        self.logger.debug(f"response {vars(resp)}")
        return resp_str.encode("utf-8")

    def handle_naomitest(self, request: Request, _: Dict) -> bytes:
        self.logger.info(f"Ping from {request.getClientAddress().host}")
        return b"naomi ok"

    def kvp_to_dict(self, kvp: List[str]) -> List[Dict[str, Any]]:
        ret: List[Dict[str, Any]] = []
        for x in kvp:
            items = x.split("&")
            tmp = {}

            for item in items:
                kvp = item.split("=")
                if len(kvp) == 2:
                    tmp[kvp[0]] = kvp[1]

            ret.append(tmp)

        return ret

    def billing_req_to_dict(self, data: bytes):
        """
        Parses an billing request string into a python dictionary
        """
        try:
            decomp = zlib.decompressobj(-zlib.MAX_WBITS)
            unzipped = decomp.decompress(data)
            sections = unzipped.decode("ascii").split("\r\n")

            return self.kvp_to_dict(sections)

        except Exception as e:
            self.logger.error(f"billing_req_to_dict: {e} while parsing {data}")
            return None

    def allnet_req_to_dict(self, data: str) -> Optional[List[Dict[str, Any]]]:
        """
        Parses an allnet request string into a python dictionary
        """
        try:
            zipped = base64.b64decode(data)
            unzipped = zlib.decompress(zipped)
            sections = unzipped.decode("utf-8").split("\r\n")

            return self.kvp_to_dict(sections)

        except Exception as e:
            self.logger.error(f"allnet_req_to_dict: {e} while parsing {data}")
            return None

    def dict_to_http_form_string(
        self,
        data: List[Dict[str, Any]],
        crlf: bool = False,
        trailing_newline: bool = True,
    ) -> Optional[str]:
        """
        Takes a python dictionary and parses it into an allnet response string
        """
        try:
            urlencode = ""
            for item in data:
                for k, v in item.items():
                    urlencode += f"{k}={v}&"

                if crlf:
                    urlencode = urlencode[:-1] + "\r\n"
                else:
                    urlencode = urlencode[:-1] + "\n"

            if not trailing_newline:
                if crlf:
                    urlencode = urlencode[:-2]
                else:
                    urlencode = urlencode[:-1]

            return urlencode

        except Exception as e:
            self.logger.error(f"dict_to_http_form_string: {e} while parsing {data}")
            return None


class AllnetPowerOnRequest:
    def __init__(self, req: Dict) -> None:
        if req is None:
            raise AllnetRequestException("Request processing failed")
        self.game_id: str = req.get("game_id", "")
        self.ver: str = req.get("ver", "")
        self.serial: str = req.get("serial", "")
        self.ip: str = req.get("ip", "")
        self.firm_ver: str = req.get("firm_ver", "")
        self.boot_ver: str = req.get("boot_ver", "")
        self.encode: str = req.get("encode", "")
        self.hops = int(req.get("hops", "0"))
        self.format_ver = req.get("format_ver", "2")
        self.token = int(req.get("token", "0"))


class AllnetPowerOnResponse3:
    def __init__(self, token) -> None:
        self.stat = 1
        self.uri = ""
        self.host = ""
        self.place_id = "123"
        self.name = ""
        self.nickname = ""
        self.region0 = "1"
        self.region_name0 = "W"
        self.region_name1 = ""
        self.region_name2 = ""
        self.region_name3 = ""
        self.country = "JPN"
        self.allnet_id = "123"
        self.client_timezone = "+0900"
        self.utc_time = datetime.now(tz=pytz.timezone("UTC")).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        self.setting = ""
        self.res_ver = "3"
        self.token = str(token)


class AllnetPowerOnResponse2:
    def __init__(self) -> None:
        self.stat = 1
        self.uri = ""
        self.host = ""
        self.place_id = "123"
        self.name = "Test"
        self.nickname = "Test123"
        self.region0 = "1"
        self.region_name0 = "W"
        self.region_name1 = "X"
        self.region_name2 = "Y"
        self.region_name3 = "Z"
        self.country = "JPN"
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.day = datetime.now().day
        self.hour = datetime.now().hour
        self.minute = datetime.now().minute
        self.second = datetime.now().second
        self.setting = "1"
        self.timezone = "+0900"
        self.res_class = "PowerOnResponseV2"


class AllnetDownloadOrderRequest:
    def __init__(self, req: Dict) -> None:
        self.game_id = req.get("game_id", "")
        self.ver = req.get("ver", "")
        self.serial = req.get("serial", "")
        self.encode = req.get("encode", "")


class AllnetDownloadOrderResponse:
    def __init__(self, stat: int = 1, serial: str = "", uri: str = "null") -> None:
        self.stat = stat
        self.serial = serial
        self.uri = uri


class BillingResponse:
    def __init__(
        self,
        playlimit: str = "",
        playlimit_sig: str = "",
        nearfull: str = "",
        nearfull_sig: str = "",
        playhistory: str = "000000/0:000000/0:000000/0",
    ) -> None:
        self.result = "0"
        self.waitime = "100"
        self.linelimit = "1"
        self.message = ""
        self.playlimit = playlimit
        self.playlimitsig = playlimit_sig
        self.protocolver = "1.000"
        self.nearfull = nearfull
        self.nearfullsig = nearfull_sig
        self.fixlogincnt = "0"
        self.fixinterval = "5"
        self.playhistory = playhistory
        # playhistory -> YYYYMM/C:...
        # YYYY -> 4 digit year, MM -> 2 digit month, C -> Playcount during that period


class AllnetRequestException(Exception):
    def __init__(self, message="") -> None:
        self.message = message
        super().__init__(self.message)
