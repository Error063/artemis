from typing import Dict, List, Any, Optional
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
from twisted.web.http import Request
from datetime import datetime
import pytz
import base64
import zlib

from core.config import CoreConfig
from core.data import Data
from core.utils import Utils

class AllnetServlet:
    def __init__(self, core_cfg: CoreConfig, cfg_folder: str):        
        super().__init__()
        self.config = core_cfg
        self.config_folder = cfg_folder
        self.data = Data(core_cfg)

        self.logger = logging.getLogger("allnet")
        if not hasattr(self.logger, "initialized"):
            log_fmt_str = "[%(asctime)s] Allnet | %(levelname)s | %(message)s"
            log_fmt = logging.Formatter(log_fmt_str)        

            fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.config.server.log_dir, "allnet"), when="d", backupCount=10)
            fileHandler.setFormatter(log_fmt)
            
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(log_fmt)

            self.logger.addHandler(fileHandler)
            self.logger.addHandler(consoleHandler)
            
            self.logger.setLevel(core_cfg.allnet.loglevel)
            coloredlogs.install(level=core_cfg.allnet.loglevel, logger=self.logger, fmt=log_fmt_str)
            self.logger.initialized = True

        if "game_registry" not in globals():
            globals()["game_registry"] = Utils.get_all_titles()

        if len(globals()["game_registry"]) == 0:
            self.logger.error("No games detected!")

    def handle_poweron(self, request: Request):
        try:
            req = AllnetPowerOnRequest(self.allnet_req_to_dict(request.content.getvalue()))
            # Validate the request. Currently we only validate the fields we plan on using

            if not req.game_id or not req.ver or not req.token or not req.serial or not req.ip:
                raise AllnetRequestException(f"Bad request params {vars(req)}")
        except AllnetRequestException as e:
            self.logger.error(e)
            return b""

    def handle_dlorder(self, request: Request):
        pass

    def handle_billing_request(self, request: Request):
        pass

    def kvp_to_dict(self, *kvp: str) -> List[Dict[str, Any]]:
        ret: List[Dict[str, Any]] = []
        for x in kvp:
            items = x.split('&')
            tmp = {}

            for item in items:
                kvp = item.split('=')
                if len(kvp) == 2:
                    tmp[kvp[0]] = kvp[1]

            ret.append(tmp)

    def allnet_req_to_dict(self, data: bytes):
        """
        Parses an billing request string into a python dictionary
        """
        try:
            decomp = zlib.decompressobj(-zlib.MAX_WBITS)
            unzipped = decomp.decompress(data)
            sections = unzipped.decode('ascii').split('\r\n')
            
            return Utils.kvp_to_dict(sections)

        except Exception as e:
            print(e)
            return None

    def billing_req_to_dict(self, data: str) -> Optional[List[Dict[str, Any]]]:
        """
        Parses an allnet request string into a python dictionary
        """    
        try:
            zipped = base64.b64decode(data)
            unzipped = zlib.decompress(zipped)
            sections = unzipped.decode('utf-8').split('\r\n')
            
            return Utils.kvp_to_dict(sections)

        except Exception as e:
            print(e)
            return None

    def dict_to_http_form_string(self, data:List[Dict[str, Any]], crlf: bool = False, trailing_newline: bool = True) -> Optional[str]:
        """
        Takes a python dictionary and parses it into an allnet response string
        """
        try:
            urlencode = ""
            for item in data:
                for k,v in item.items():
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
            print(e)
            return None

class AllnetPowerOnRequest():
    def __init__(self, req: Dict) -> None:
        if req is None:
            raise AllnetRequestException("Request processing failed")
        self.game_id: str = req["game_id"] if "game_id" in req else ""
        self.ver: str = req["ver"] if "ver" in req else ""
        self.serial: str  = req["serial"] if "serial" in req else ""
        self.ip: str  = req["ip"] if "ip" in req else ""
        self.firm_ver: str = req["firm_ver"] if "firm_ver" in req else ""
        self.boot_ver: str = req["boot_ver"] if "boot_ver" in req else ""
        self.encode: str = req["encode"] if "encode" in req else ""
        
        try:
            self.hops = int(req["hops"]) if "hops" in req else 0
            self.format_ver = int(req["format_ver"]) if "format_ver" in req else 2
            self.token = int(req["token"]) if "token" in req else 0
        except ValueError as e:
            raise AllnetRequestException(f"Failed to parse int: {e}")

class AllnetPowerOnResponse3():
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
        self.utc_time = datetime.now(tz=pytz.timezone('UTC')).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.setting = ""
        self.res_ver = "3"
        self.token = str(token)

class AllnetPowerOnResponse2():
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

class AllnetDownloadOrderRequest():
    def __init__(self, req: Dict) -> None:
        self.game_id = req["game_id"] if "game_id" in req else ""
        self.ver = req["ver"] if "ver" in req else ""
        self.serial = req["serial"] if "serial" in req else ""
        self.encode = req["encode"] if "encode" in req else ""

class AllnetDownloadOrderResponse():
    def __init__(self, stat: int = 1, serial: str = "", uri: str = "null") -> None:
        self.stat = stat
        self.serial = serial
        self.uri = uri

class BillingResponse():
    def __init__(self, playlimit: str, playlimit_sig: str, nearfull: str, nearfull_sig: str, 
        playhistory: str = "000000/0:000000/0:000000/0") -> None:

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
    pass
