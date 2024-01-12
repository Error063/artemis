import pytz
import base64
import zlib
import json
import yaml
import logging
import coloredlogs
import urllib.parse
import math
from typing import Dict, List, Any, Optional, Union, Final
from logging.handlers import TimedRotatingFileHandler
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.applications import Starlette
from starlette.routing import Route
from datetime import datetime
from enum import Enum
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from os import path, environ, mkdir, access, W_OK

from .config import CoreConfig
from .utils import Utils
from .data import Data
from .const import *
from .title import TitleServlet

BILLING_DT_FORMAT: Final[str] = "%Y%m%d%H%M%S"

class DLIMG_TYPE(Enum):
    app = 0
    opt = 1

class ALLNET_STAT(Enum):
    ok = 0
    bad_game = -1
    bad_machine = -2
    bad_shop = -3

class DLI_STATUS(Enum):
    START = 0
    GET_DOWNLOAD_CONFIGURATION = 1
    WAIT_DOWNLOAD = 2
    DOWNLOADING = 3

    NOT_SPECIFY_DLI = 100
    ONLY_POST_REPORT = 101
    STOPPED_BY_APP_RELEASE = 102
    STOPPED_BY_OPT_RELEASE = 103

    DOWNLOAD_COMPLETE_RECENTLY = 110

    DOWNLOAD_COMPLETE_WAIT_RELEASE_TIME = 120
    DOWNLOAD_COMPLETE_BUT_NOT_SYNC_SERVER = 121
    DOWNLOAD_COMPLETE_BUT_NOT_FIRST_RESUME = 122
    DOWNLOAD_COMPLETE_BUT_NOT_FIRST_LAUNCH = 123
    DOWNLOAD_COMPLETE_WAIT_UPDATE = 124

    DOWNLOAD_COMPLETE_AND_ALREADY_UPDATE = 130

    ERROR_AUTH_FAILURE = 200

    ERROR_GET_DLI_HTTP = 300
    ERROR_GET_DLI = 301
    ERROR_PARSE_DLI = 302
    ERROR_INVALID_GAME_ID = 303
    ERROR_INVALID_IMAGE_LIST = 304
    ERROR_GET_DLI_APP = 305

    ERROR_GET_BOOT_ID = 400
    ERROR_ACCESS_SERVER = 401
    ERROR_NO_IMAGE = 402
    ERROR_ACCESS_IMAGE = 403

    ERROR_DOWNLOAD_APP = 500
    ERROR_DOWNLOAD_OPT = 501

    ERROR_DISK_FULL = 600
    ERROR_UNINSTALL = 601
    ERROR_INSTALL_APP = 602
    ERROR_INSTALL_OPT = 603

    ERROR_GET_DLI_INTERNAL = 900
    ERROR_ICF = 901
    ERROR_CHECK_RELEASE_INTERNAL = 902
    UNKNOWN = 999 # Not the actual enum val but it needs to be here as a catch-all

    @classmethod
    def from_int(cls, num: int) -> "DLI_STATUS":
        try:
            return cls(num)
        except ValueError:
            return cls.UNKNOWN

class AllnetServlet:
    def __init__(self, core_cfg: CoreConfig, cfg_folder: str):
        self.config = core_cfg
        self.config_folder = cfg_folder
        self.data = Data(core_cfg)

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

    def startup(self) -> None:
        self.logger.info(f"Ready on port {self.config.allnet.port if self.config.allnet.standalone else self.config.server.port}")

    async def handle_poweron(self, request: Request):
        request_ip = Utils.get_ip_addr(request)
        pragma_header = request.headers.get('Pragma', "")
        is_dfi = pragma_header is not None and pragma_header == "DFI"
        data = await request.body()
        
        try:
            if is_dfi:
                req_urlencode = self.from_dfi(data)
            else:
                req_urlencode = data

            req_dict = self.allnet_req_to_dict(req_urlencode)
            if req_dict is None:
                raise AllnetRequestException()

            req = AllnetPowerOnRequest(req_dict[0])
            # Validate the request. Currently we only validate the fields we plan on using

            if not req.game_id or not req.ver or not req.serial or not req.ip or not req.firm_ver or not req.boot_ver:
                raise AllnetRequestException(
                    f"Bad auth request params from {request_ip} - {vars(req)}"
                )

        except AllnetRequestException as e:
            if e.message != "":
                self.logger.error(e)
            return PlainTextResponse()

        if req.format_ver == 3:
            resp = AllnetPowerOnResponse3(req.token)
        elif req.format_ver == 2:
            resp = AllnetPowerOnResponse2()
        else:
            resp = AllnetPowerOnResponse()

        self.logger.debug(f"Allnet request: {vars(req)}")

        machine = await self.data.arcade.get_machine(req.serial)        
        if machine is None and not self.config.server.allow_unregistered_serials:
            msg = f"Unrecognised serial {req.serial} attempted allnet auth from {request_ip}."
            await self.data.base.log_event(
                "allnet", "ALLNET_AUTH_UNKNOWN_SERIAL", logging.WARN, msg
            )
            self.logger.warning(msg)

            resp.stat = ALLNET_STAT.bad_machine.value
            resp_dict = {k: v for k, v in vars(resp).items() if v is not None}
            return PlainTextResponse(urllib.parse.unquote(urllib.parse.urlencode(resp_dict)) + "\n")

        if machine is not None:
            arcade = await self.data.arcade.get_arcade(machine["arcade"])
            if self.config.server.check_arcade_ip:
                if arcade["ip"] and arcade["ip"] is not None and arcade["ip"] != req.ip:
                    msg = f"Serial {req.serial} attempted allnet auth from bad IP {req.ip} (expected {arcade['ip']})."
                    await self.data.base.log_event(
                        "allnet", "ALLNET_AUTH_BAD_IP", logging.ERROR, msg
                    )
                    self.logger.warning(msg)

                    resp.stat = ALLNET_STAT.bad_shop.value
                    resp_dict = {k: v for k, v in vars(resp).items() if v is not None}
                    return PlainTextResponse(urllib.parse.unquote(urllib.parse.urlencode(resp_dict)) + "\n")
                
                elif (not arcade["ip"] or arcade["ip"] is None) and self.config.server.strict_ip_checking:
                    msg = f"Serial {req.serial} attempted allnet auth from bad IP {req.ip}, but arcade {arcade['id']} has no IP set! (strict checking enabled)."
                    await self.data.base.log_event(
                        "allnet", "ALLNET_AUTH_NO_SHOP_IP", logging.ERROR, msg
                    )
                    self.logger.warning(msg)

                    resp.stat = ALLNET_STAT.bad_shop.value
                    resp_dict = {k: v for k, v in vars(resp).items() if v is not None}
                    return PlainTextResponse(urllib.parse.unquote(urllib.parse.urlencode(resp_dict)) + "\n")


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
                arcade["state"]
                if arcade["state"] is not None
                else AllnetJapanRegionId.AICHI.name
            )
            resp.region_name1 = (
                arcade["country"]
                if arcade["country"] is not None
                else AllnetCountryCode.JAPAN.value
            )
            resp.region_name2 = arcade["city"] if arcade["city"] is not None else ""
            resp.client_timezone = ( # lmao
                arcade["timezone"] if arcade["timezone"] is not None else "+0900" if req.format_ver == 3 else "+09:00"
            )
        
        if req.game_id not in TitleServlet.title_registry:
            if not self.config.server.is_develop:
                msg = f"Unrecognised game {req.game_id} attempted allnet auth from {request_ip}."
                await self.data.base.log_event(
                    "allnet", "ALLNET_AUTH_UNKNOWN_GAME", logging.WARN, msg
                )
                self.logger.warning(msg)

                resp.stat = ALLNET_STAT.bad_game.value
                resp_dict = {k: v for k, v in vars(resp).items() if v is not None}
                return PlainTextResponse(urllib.parse.unquote(urllib.parse.urlencode(resp_dict)) + "\n")

            else:
                self.logger.info(
                    f"Allowed unknown game {req.game_id} v{req.ver} to authenticate from {request_ip} due to 'is_develop' being enabled. S/N: {req.serial}"
                )
                resp.uri = f"http://{self.config.server.hostname}:{self.config.server.port}/{req.game_id}/{req.ver.replace('.', '')}/"
                resp.host = f"{self.config.server.hostname}:{self.config.server.port}"
                
                resp_dict = {k: v for k, v in vars(resp).items() if v is not None}
                resp_str = urllib.parse.unquote(urllib.parse.urlencode(resp_dict))
                
                self.logger.debug(f"Allnet response: {resp_str}")
                return PlainTextResponse(resp_str + "\n")

        
        int_ver = req.ver.replace(".", "")
        resp.uri, resp.host = TitleServlet.title_registry[req.game_id].get_allnet_info(req.game_id, int(int_ver), req.serial)

        msg = f"{req.serial} authenticated from {request_ip}: {req.game_id} v{req.ver}"
        await self.data.base.log_event("allnet", "ALLNET_AUTH_SUCCESS", logging.INFO, msg)
        self.logger.info(msg)

        resp_dict = {k: v for k, v in vars(resp).items() if v is not None}
        resp_str = urllib.parse.unquote(urllib.parse.urlencode(resp_dict))
        self.logger.debug(f"Allnet response: {resp_dict}")        
        resp_str += "\n"

        """if is_dfi:
            request.responseHeaders.addRawHeader('Pragma', 'DFI')
            return self.to_dfi(resp_str)"""

        return PlainTextResponse(resp_str)

    async def handle_dlorder(self, request: Request):
        request_ip = Utils.get_ip_addr(request)
        pragma_header = request.headers.get('Pragma', "")
        is_dfi = pragma_header is not None and pragma_header == "DFI"
        data = await request.body()
        
        try:
            if is_dfi:
                req_urlencode = self.from_dfi(data)
            else:
                req_urlencode = data.decode()

            req_dict = self.allnet_req_to_dict(req_urlencode)
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
            return PlainTextResponse()

        self.logger.info(
            f"DownloadOrder from {request_ip} -> {req.game_id} v{req.ver} serial {req.serial}"
        )
        resp = AllnetDownloadOrderResponse(serial=req.serial)

        if (
            not self.config.allnet.allow_online_updates
            or not self.config.allnet.update_cfg_folder
        ):
            return PlainTextResponse(urllib.parse.unquote(urllib.parse.urlencode(vars(resp))) + "\n")

        else:  # TODO: Keychip check
            if path.exists(
                f"{self.config.allnet.update_cfg_folder}/{req.game_id}-{req.ver.replace('.', '')}-app.ini"
            ):
                resp.uri = f"http://{self.config.server.hostname}:{self.config.server.port}/dl/ini/{req.game_id}-{req.ver.replace('.', '')}-app.ini"

            if path.exists(
                f"{self.config.allnet.update_cfg_folder}/{req.game_id}-{req.ver.replace('.', '')}-opt.ini"
            ):
                resp.uri += f"|http://{self.config.server.hostname}:{self.config.server.port}/dl/ini/{req.game_id}-{req.ver.replace('.', '')}-opt.ini"

            self.logger.debug(f"Sending download uri {resp.uri}")
            await self.data.base.log_event("allnet", "DLORDER_REQ_SUCCESS", logging.INFO, f"{Utils.get_ip_addr(request)} requested DL Order for {req.serial} {req.game_id} v{req.ver}")

            res_str = urllib.parse.unquote(urllib.parse.urlencode(vars(resp))) + "\n"
            """if is_dfi:
                request.responseHeaders.addRawHeader('Pragma', 'DFI')
                return self.to_dfi(res_str)"""

            return PlainTextResponse(res_str)

    async def handle_dlorder_ini(self, request: Request) -> bytes:
        req_file = request.path_params.get("file", "").replace("%0A", "").replace("\n", "")

        if not req_file:
            return PlainTextResponse(status_code=404)

        if path.exists(f"{self.config.allnet.update_cfg_folder}/{req_file}"):
            self.logger.info(f"Request for DL INI file {req_file} from {Utils.get_ip_addr(request)} successful")
            await self.data.base.log_event("allnet", "DLORDER_INI_SENT", logging.INFO, f"{Utils.get_ip_addr(request)} successfully recieved {req_file}")
            
            return PlainTextResponse(open(
                f"{self.config.allnet.update_cfg_folder}/{req_file}", "r", encoding="utf-8"
            ).read())

        self.logger.info(f"DL INI File {req_file} not found")
        return PlainTextResponse()

    async def handle_dlorder_report(self, request: Request) -> bytes:
        req_raw = await request.body()
        client_ip = Utils.get_ip_addr(request)
        try:
            req_dict: Dict = json.loads(req_raw)
        except Exception as e:
            self.logger.warning(f"Failed to parse DL Report: {e}")
            return PlainTextResponse("NG")
        
        dl_data_type = DLIMG_TYPE.app
        dl_data = req_dict.get("appimage", {})
        
        if dl_data is None or not dl_data:
            dl_data_type = DLIMG_TYPE.opt
            dl_data = req_dict.get("optimage", {})
        
        if dl_data is None or not dl_data:
            self.logger.warning(f"Failed to parse DL Report: Invalid format - contains neither appimage nor optimage")
            return PlainTextResponse("NG")

        rep = DLReport(dl_data, dl_data_type)

        if not rep.validate():
            self.logger.warning(f"Failed to parse DL Report: Invalid format - {rep.err}")
            return PlainTextResponse("NG")
        
        msg = f"{rep.serial} @ {client_ip} reported {rep.rep_type.name} download state {rep.rf_state.name} for {rep.gd} v{rep.dav}:"\
              f" {rep.tdsc}/{rep.tsc} segments downloaded for working files {rep.wfl} with {rep.dfl if rep.dfl else 'none'} complete."
        
        await self.data.base.log_event("allnet", "DL_REPORT", logging.INFO, msg, dl_data)
        self.logger.info(msg)

        return PlainTextResponse("OK")

    async def handle_loaderstaterecorder(self, request: Request) -> bytes:
        req_data = await request.body()
        sections = req_data.decode("utf-8").split("\r\n")
        
        req_dict = dict(urllib.parse.parse_qsl(sections[0]))

        serial: Union[str, None] = req_dict.get("serial", None)
        num_files_to_dl: Union[str, None] = req_dict.get("nb_ftd", None)
        num_files_dld: Union[str, None] = req_dict.get("nb_dld", None)
        dl_state: Union[str, None] = req_dict.get("dld_st", None)
        ip = Utils.get_ip_addr(request)

        if serial is None or num_files_dld is None or num_files_to_dl is None or dl_state is None:
            return PlainTextResponse("NG")

        self.logger.info(f"LoaderStateRecorder Request from {ip} {serial}: {num_files_dld}/{num_files_to_dl} Files download (State: {dl_state})")
        return PlainTextResponse("OK")
    
    async def handle_alive(self, request: Request) -> bytes:
        return PlainTextResponse("OK")

    async def handle_naomitest(self, request: Request) -> bytes:
        self.logger.info(f"Ping from {Utils.get_ip_addr(request)}")
        return PlainTextResponse("naomi ok")

    def allnet_req_to_dict(self, data: str) -> Optional[List[Dict[str, Any]]]:
        """
        Parses an allnet request string into a python dictionary
        """
        try:
            sections = data.split("\r\n")

            ret = []
            for x in sections:
                ret.append(dict(urllib.parse.parse_qsl(x)))
            return ret

        except Exception as e:
            self.logger.error(f"allnet_req_to_dict: {e} while parsing {data}")
            return None

    def from_dfi(self, data: bytes) -> str:
        zipped = base64.b64decode(data)
        unzipped = zlib.decompress(zipped)
        return unzipped.decode("utf-8")

    def to_dfi(self, data: str) -> bytes:
        unzipped = data.encode('utf-8')
        zipped = zlib.compress(unzipped)
        return base64.b64encode(zipped)

class BillingServlet:
    def __init__(self, core_cfg: CoreConfig, cfg_folder: str) -> None:
        self.config = core_cfg
        self.config_folder = cfg_folder
        self.data = Data(core_cfg)

        self.logger = logging.getLogger("billing")
        if not hasattr(self.logger, "initialized"):
            log_fmt_str = "[%(asctime)s] Billing | %(levelname)s | %(message)s"
            log_fmt = logging.Formatter(log_fmt_str)

            fileHandler = TimedRotatingFileHandler(
                "{0}/{1}.log".format(self.config.server.log_dir, "billing"),
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
                level=core_cfg.billing.loglevel, logger=self.logger, fmt=log_fmt_str
            )
            self.logger.initialized = True
    
    def startup(self) -> None:
        self.logger.info(f"Ready on port {self.config.billing.port if self.config.billing.standalone else self.config.server.port}")

    def billing_req_to_dict(self, data: bytes):
        """
        Parses an billing request string into a python dictionary
        """
        try:
            sections = data.decode("ascii").split("\r\n")

            ret = []
            for x in sections:
                ret.append(dict(urllib.parse.parse_qsl(x)))
            return ret

        except Exception as e:
            self.logger.error(f"billing_req_to_dict: {e} while parsing {data}")
            return None
    
    async def handle_billing_request(self, request: Request):
        req_raw = await request.body()
        
        if request.headers.get('Content-Type', '') == "application/octet-stream":
            req_unzip = zlib.decompressobj(-zlib.MAX_WBITS).decompress(req_raw)
        else:
            req_unzip = req_raw
        
        req_dict = self.billing_req_to_dict(req_unzip)
        request_ip = Utils.get_ip_addr(request)
        
        if req_dict is None:
            self.logger.error(f"Failed to parse request {req_raw}")
            return PlainTextResponse()

        self.logger.debug(f"request {req_dict}")

        rsa = RSA.import_key(open(self.config.billing.signing_key, "rb").read())
        signer = PKCS1_v1_5.new(rsa)
        digest = SHA.new()
        traces: List[TraceData] = []
        try:
            req = BillingInfo(req_dict[0])
        except KeyError as e:
            self.logger.error(f"Billing request failed to parse: {e}")
            return PlainTextResponse("result=5&linelimit=&message=field is missing or formatting is incorrect\r\n")

        for x in range(1, len(req_dict)):
            if not req_dict[x]:
                continue
            
            try:
                tmp = TraceData(req_dict[x])
                if tmp.trace_type == TraceDataType.CHARGE:
                    tmp = TraceDataCharge(req_dict[x])
                elif tmp.trace_type == TraceDataType.EVENT:
                    tmp = TraceDataEvent(req_dict[x])
                elif tmp.trace_type == TraceDataType.CREDIT:
                    tmp = TraceDataCredit(req_dict[x])
                
                traces.append(tmp)
            
            except KeyError as e:
                self.logger.warn(f"Tracelog failed to parse: {e}")

        kc_serial_bytes = req.keychipid.encode()
        

        machine = await self.data.arcade.get_machine(req.keychipid)
        if machine is None and not self.config.server.allow_unregistered_serials:
            msg = f"Unrecognised serial {req.keychipid} attempted billing checkin from {request_ip} for {req.gameid} v{req.gamever}."
            await self.data.base.log_event(
                "allnet", "BILLING_CHECKIN_NG_SERIAL", logging.WARN, msg
            )
            self.logger.warning(msg)

            return PlainTextResponse(f"result=1&requestno={req.requestno}&message=Keychip Serial bad\r\n")

        msg = (
            f"Billing checkin from {request_ip}: game {req.gameid} ver {req.gamever} keychip {req.keychipid} playcount "
            f"{req.playcnt} billing_type {req.billingtype.name} nearfull {req.nearfull} playlimit {req.playlimit}"
        )
        self.logger.info(msg)
        await self.data.base.log_event("billing", "BILLING_CHECKIN_OK", logging.INFO, msg)
        if req.traceleft > 0:
            self.logger.warn(f"{req.traceleft} unsent tracelogs")
        kc_playlimit = req.playlimit
        kc_nearfull = req.nearfull

        while req.playcnt > req.playlimit:
            kc_playlimit += 1024
            kc_nearfull += 1024

        playlimit = kc_playlimit
        nearfull = kc_nearfull + (req.billingtype.value * 0x00010000)

        digest.update(playlimit.to_bytes(4, "little") + kc_serial_bytes)
        playlimit_sig = signer.sign(digest).hex()

        digest = SHA.new()
        digest.update(nearfull.to_bytes(4, "little") + kc_serial_bytes)
        nearfull_sig = signer.sign(digest).hex()

        # TODO: playhistory

        resp = BillingResponse(playlimit, playlimit_sig, nearfull, nearfull_sig, req.requestno, req.protocolver)

        resp_str = urllib.parse.unquote(urllib.parse.urlencode(vars(resp))) + "\r\n"

        self.logger.debug(f"response {vars(resp)}")
        if req.traceleft > 0:
            self.logger.info(f"Requesting 20 more of {req.traceleft} unsent tracelogs")
            return PlainTextResponse("result=6&waittime=0&linelimit=20\r\n")
        
        return PlainTextResponse(resp_str)

class AllnetPowerOnRequest:
    def __init__(self, req: Dict) -> None:
        if req is None:
            raise AllnetRequestException("Request processing failed")
        self.game_id: str = req.get("game_id", None)
        self.ver: str = req.get("ver", None)
        self.serial: str = req.get("serial", None)
        self.ip: str = req.get("ip", None)
        self.firm_ver: str = req.get("firm_ver", None)
        self.boot_ver: str = req.get("boot_ver", None)
        self.encode: str = req.get("encode", "EUC-JP")
        self.hops = int(req.get("hops", "-1"))
        self.format_ver = float(req.get("format_ver", "1.00"))
        self.token: str = req.get("token", "0")

class AllnetPowerOnResponse:
    def __init__(self) -> None:
        self.stat = 1
        self.uri = ""
        self.host = ""
        self.place_id = "0123"
        self.name = "ARTEMiS"
        self.nickname = "ARTEMiS"
        self.region0 = "1"
        self.region_name0 = "W"
        self.region_name1 = ""
        self.region_name2 = ""
        self.region_name3 = ""        
        self.setting = "1"
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.day = datetime.now().day
        self.hour = datetime.now().hour
        self.minute = datetime.now().minute
        self.second = datetime.now().second

class AllnetPowerOnResponse3(AllnetPowerOnResponse):
    def __init__(self, token) -> None:
        super().__init__()

        # Added in v3
        self.country = "JPN"
        self.allnet_id = "123"
        self.client_timezone = "+0900"
        self.utc_time = datetime.now(tz=pytz.timezone("UTC")).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        self.res_ver = "3"
        self.token = token

        # Removed in v3
        self.year = None
        self.month = None
        self.day = None
        self.hour = None
        self.minute = None
        self.second = None

class AllnetPowerOnResponse2(AllnetPowerOnResponse):
    def __init__(self) -> None:
        super().__init__()

        # Added in v2
        self.country = "JPN"
        self.timezone = "+09:00"
        self.res_class = "PowerOnResponseV2"

class AllnetDownloadOrderRequest:
    def __init__(self, req: Dict) -> None:
        self.game_id = req.get("game_id", "")
        self.ver = req.get("ver", "")
        self.serial = req.get("serial", "")
        self.encode = req.get("encode", "")

class AllnetDownloadOrderResponse:
    def __init__(self, stat: int = 1, serial: str = "", uri: str = "") -> None:
        self.stat = stat
        self.serial = serial
        self.uri = uri

class TraceDataType(Enum):
    CHARGE = 0
    EVENT = 1
    CREDIT = 2

class BillingType(Enum):
    A = 1
    B = 0

class float5:
    def __init__(self, n: str = "0") -> None:
        nf = float(n)
        if nf > 999.9 or nf < 0:
            raise ValueError('float5 must be between 0.000 and 999.9 inclusive')
        
        return nf
    
    @classmethod
    def to_str(cls, f: float):
        return f"%.{2 - int(math.log10(f))+1}f" % f

class BillingInfo:
    def __init__(self, data: Dict) -> None:
        try:
            self.keychipid = str(data.get("keychipid", None))
            self.functype = int(data.get("functype", None))
            self.gameid = str(data.get("gameid", None))
            self.gamever = float(data.get("gamever", None))
            self.boardid = str(data.get("boardid", None))
            self.tenpoip = str(data.get("tenpoip", None))
            self.libalibver = float(data.get("libalibver", None))
            self.data.max = int(data.get("datamax", None))
            self.billingtype = BillingType(int(data.get("billingtype", None)))
            self.protocolver = float(data.get("protocolver", None))
            self.operatingfix = bool(data.get("operatingfix", None))
            self.traceleft = int(data.get("traceleft", None))
            self.requestno = int(data.get("requestno", None))
            self.datesync = bool(data.get("datesync", None))
            self.timezone = str(data.get("timezone", None))
            self.date = datetime.strptime(data.get("date", None), BILLING_DT_FORMAT)
            self.crcerrcnt = int(data.get("crcerrcnt", None))
            self.memrepair = bool(data.get("memrepair", None))
            self.playcnt = int(data.get("playcnt", None))
            self.playlimit = int(data.get("playlimit", None))
            self.nearfull = int(data.get("nearfull", None))
        except Exception as e:
            raise KeyError(e)

class TraceData:
    def __init__(self, data: Dict) -> None:
        try:
            self.crc_err_flg = bool(data.get("cs", None))
            self.record_number = int(data.get("rn", None))
            self.seq_number = int(data.get("sn", None))
            self.trace_type = TraceDataType(int(data.get("tt", None)))
            self.date_sync_flg = bool(data.get("ds", None))
            
            dt = data.get("dt", None)
            if dt is None:
                raise KeyError("dt not present")
            if dt == "20000000000000": # Not sure what causes it to send like this...
                self.date = datetime(2000, 1, 1, 0, 0, 0, 0)
            else:
                self.date = datetime.strptime(data.get("dt", None), BILLING_DT_FORMAT)
            
            self.keychip = str(data.get("kn", None))
            self.lib_ver = float(data.get("alib", 0))
        except Exception as e:
            raise KeyError(e)

class TraceDataCharge(TraceData):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        try:
            self.game_id = str(data.get("gi", None)) # these seem optional...?
            self.game_version = float(data.get("gv", 0))
            self.board_serial = str(data.get("bn", None))
            self.shop_ip = str(data.get("ti", None))
            self.play_count = int(data.get("pc", None))
            self.play_limit = int(data.get("pl", None))
            self.product_code = int(data.get("ic", None))
            self.product_count = int(data.get("in", None))
            self.func_type = int(data.get("kk", None))
            self.player_number = int(data.get("playerno", None))
        except Exception as e:
            raise KeyError(e)

class TraceDataEvent(TraceData):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        try:
            self.message = str(data.get("me", None))
        except Exception as e:
            raise KeyError(e)

class TraceDataCredit(TraceData):
    def __init__(self, data: Dict) -> None:
        super().__init__(data)
        try:
            self.chute_type = int(data.get("cct", None))
            self.service_type = int(data.get("cst", None))
            self.operation_type = int(data.get("cop", None))
            self.coin_rate0 = int(data.get("cr0", None))
            self.coin_rate1 = int(data.get("cr1", None))
            self.bonus_addition = int(data.get("cba", None))
            self.credit_rate = int(data.get("ccr", None))
            self.credit0 = int(data.get("cc0", None))
            self.credit1 = int(data.get("cc1", None))
            self.credit2 = int(data.get("cc2", None))
            self.credit3 = int(data.get("cc3", None))
            self.credit4 = int(data.get("cc4", None))
            self.credit5 = int(data.get("cc5", None))
            self.credit6 = int(data.get("cc6", None))
            self.credit7 = int(data.get("cc7", None))
        except Exception as e:
            raise KeyError(e)

class BillingResponse:
    def __init__(
        self,
        playlimit: str = "",
        playlimit_sig: str = "",
        nearfull: str = "",
        nearfull_sig: str = "",
        request_num: int = 1,
        protocol_ver: float = 1.000,
        playhistory: str = "000000/0:000000/0:000000/0",
    ) -> None:
        self.result = 0
        self.requestno = request_num
        self.traceerase = 1
        self.fixinterval = 120
        self.fixlogcnt = 100
        self.playlimit = playlimit
        self.playlimitsig = playlimit_sig
        self.playhistory = playhistory
        self.nearfull = nearfull
        self.nearfullsig = nearfull_sig
        self.linelimit = 100
        self.protocolver = float5.to_str(protocol_ver)
        # playhistory -> YYYYMM/C:...
        # YYYY -> 4 digit year, MM -> 2 digit month, C -> Playcount during that period

class AllnetRequestException(Exception):
    def __init__(self, message="") -> None:
        self.message = message
        super().__init__(self.message)

class DLReport:
    def __init__(self, data: Dict, report_type: DLIMG_TYPE) -> None:
        self.serial = data.get("serial")
        self.dfl = data.get("dfl")
        self.wfl = data.get("wfl")
        self.tsc = data.get("tsc")
        self.tdsc = data.get("tdsc")
        self.at = data.get("at")
        self.ot = data.get("ot")
        self.rt = data.get("rt")
        self.as_ = data.get("as")
        self.rf_state = DLI_STATUS.from_int(data.get("rf_state"))
        self.gd = data.get("gd")
        self.dav = data.get("dav")
        self.wdav = data.get("wdav") # app only
        self.dov = data.get("dov")
        self.wdov = data.get("wdov") # app only
        self.rep_type = report_type
        self.err = ""
    
    def validate(self) -> bool:
        if  self.serial is None:
            self.err = "serial not provided"
            return False
        
        if self.tsc is None:
            self.err = "tsc not provided"
            return False
        
        if self.tdsc is None:
            self.err = "tdsc not provided"
            return False
        
        if self.as_ is None:
            self.err = "as not provided"
            return False
        
        if self.rf_state is None:
            self.err = "rf_state not provided"
            return False
        
        if self.gd is None:
            self.err = "gd not provided"
            return False
        
        if self.dav is None:
            self.err = "dav not provided"
            return False
        
        if self.dov is None:
            self.err = "dov not provided"
            return False
        
        if (self.wdav is None or self.wdov is None) and self.rep_type == DLIMG_TYPE.app:
            self.err = "wdav or wdov not provided in app image"
            return False
        
        if (self.wdav is not None or self.wdov is not None) and self.rep_type == DLIMG_TYPE.opt:
            self.err = "wdav or wdov provided in opt image"
            return False
        
        return True

cfg_dir = environ.get("DIANA_CFG_DIR", "config")
cfg: CoreConfig = CoreConfig()
if path.exists(f"{cfg_dir}/core.yaml"):
    cfg.update(yaml.safe_load(open(f"{cfg_dir}/core.yaml")))

if not path.exists(cfg.server.log_dir):
    mkdir(cfg.server.log_dir)

if not access(cfg.server.log_dir, W_OK):
    print(
        f"Log directory {cfg.server.log_dir} NOT writable, please check permissions"
    )
    exit(1)

billing = BillingServlet(cfg, cfg_dir)
app_billing = Starlette(
    cfg.server.is_develop, 
    [        
        Route("/request", billing.handle_billing_request, methods=["POST"]),
        Route("/request/", billing.handle_billing_request, methods=["POST"]),
    ],
    on_startup=[billing.startup]
)

allnet = AllnetServlet(cfg, cfg_dir)
route_lst = [
    Route("/sys/servlet/PowerOn", allnet.handle_poweron, methods=["GET", "POST"]),
    Route("/sys/servlet/DownloadOrder", allnet.handle_dlorder, methods=["GET", "POST"]),
    Route("/sys/servlet/LoaderStateRecorder", allnet.handle_loaderstaterecorder, methods=["GET", "POST"]),
    Route("/sys/servlet/Alive", allnet.handle_alive, methods=["GET", "POST"]),
    Route("/naomitest.html", allnet.handle_naomitest),
]

if cfg.allnet.allow_online_updates:
    route_lst += [
        Route("/report-api/Report", allnet.handle_dlorder_report, methods=["POST"]),
        Route("/dl/ini/{file:str}", allnet.handle_dlorder_ini),
    ]

app_allnet = Starlette(
    cfg.server.is_develop, 
    route_lst,
    on_startup=[allnet.startup]
)
