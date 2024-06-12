from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.routing import Route
import json
import inflection
import yaml
import logging, coloredlogs
import zlib
import string
from logging.handlers import TimedRotatingFileHandler
from os import path, mkdir
from typing import Tuple, List, Dict
from Crypto.Hash import MD5

from core.config import CoreConfig
from core.utils import Utils
from core.title import BaseServlet
from core.crypto import CipherAES
from .config import Mai2Config
from .const import Mai2Constants
from .base import Mai2Base
from .finale import Mai2Finale
from .dx import Mai2DX
from .dxplus import Mai2DXPlus
from .splash import Mai2Splash
from .splashplus import Mai2SplashPlus
from .universe import Mai2Universe
from .universeplus import Mai2UniversePlus
from .festival import Mai2Festival
from .festivalplus import Mai2FestivalPlus
from .buddies import Mai2Buddies


class Mai2Servlet(BaseServlet):
    def __init__(self, core_cfg: CoreConfig, cfg_dir: str) -> None:
        super().__init__(core_cfg, cfg_dir)
        self.game_cfg = Mai2Config()
        self.hash_table: Dict[int, Dict[str, str]] = {}
        if path.exists(f"{cfg_dir}/{Mai2Constants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{Mai2Constants.CONFIG_NAME}"))
            )

        self.versions = [
            Mai2Base,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            Mai2Finale,
            Mai2DX,
            Mai2DXPlus,
            Mai2Splash,
            Mai2SplashPlus,
            Mai2Universe,
            Mai2UniversePlus,
            Mai2Festival,
            Mai2FestivalPlus,
            Mai2Buddies
        ]

        self.logger = logging.getLogger("mai2")
        if not hasattr(self.logger, "initted"):
            log_fmt_str = "[%(asctime)s] Mai2 | %(levelname)s | %(message)s"
            log_fmt = logging.Formatter(log_fmt_str)
            fileHandler = TimedRotatingFileHandler(
                "{0}/{1}.log".format(self.core_cfg.server.log_dir, "mai2"),
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
            self.logger.initted = True
        
        for version, keys in self.game_cfg.crypto.keys.items():
            if version < Mai2Constants.VER_MAIMAI_DX:
                continue

            if len(keys) < 3:
                continue

            self.hash_table[version] = {}
            method_list = [
                method
                for method in dir(self.versions[version])
                if not method.startswith("__")
            ]

            for method in method_list:
                # handle_method_api_request -> HandleMethodApiRequest
                # remove the first 6 chars and the final 7 chars to get the canonical
                # endpoint name.
                method_fixed = inflection.camelize(method)[6:-7]
                hash = MD5.new((method_fixed + keys[2]).encode())

                # truncate unused bytes like the game does
                hashed_name = hash.hexdigest()
                self.hash_table[version][hashed_name] = method_fixed

                self.logger.debug(
                    "Hashed v%s method %s with %s to get %s",
                    version, method_fixed, keys[2], hashed_name
                )


    @classmethod
    def is_game_enabled(
        cls, game_code: str, core_cfg: CoreConfig, cfg_dir: str
    ) -> bool:
        game_cfg = Mai2Config()

        if path.exists(f"{cfg_dir}/{Mai2Constants.CONFIG_NAME}"):
            game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{Mai2Constants.CONFIG_NAME}"))
            )

        if not game_cfg.server.enable:
            return False
        
        return True
    
    def get_routes(self) -> List[Route]:
        return [
            Route("/{game:str}/{version:int}/MaimaiServlet/api/movie/{endpoint:str}", self.handle_movie, methods=['GET', 'POST']),
            Route("/{game:str}/{version:int}/MaimaiServlet/old/{endpoint:str}", self.handle_old_srv),
            Route("/{game:str}/{version:int}/MaimaiServlet/old/{endpoint:str}/{placeid:str}/{keychip:str}/{userid:int}", self.handle_old_srv_userdata),
            Route("/{game:str}/{version:int}/MaimaiServlet/old/{endpoint:str}/{userid:int}", self.handle_old_srv_userdata),
            Route("/{game:str}/{version:int}/MaimaiServlet/old/{endpoint:str}/{userid:int}", self.handle_old_srv_userdata),
            Route("/{game:str}/{version:int}/MaimaiServlet/usbdl/{endpoint:str}", self.handle_usbdl),
            Route("/{game:str}/{version:int}/MaimaiServlet/deliver/{endpoint:str}", self.handle_deliver),
            Route("/{game:str}/{version:int}/MaimaiServlet/{endpoint:str}", self.handle_mai, methods=['POST']),
            Route("/{game:str}/{version:int}/Maimai2Servlet/{endpoint:str}", self.handle_mai2, methods=['POST']),
        ]
        
    def get_allnet_info(self, game_code: str, game_ver: int, keychip: str) -> Tuple[str, str]:
        if not self.core_cfg.server.is_using_proxy and Utils.get_title_port(self.core_cfg) != 80:
            return (
                f"http://{self.core_cfg.server.hostname}:{Utils.get_title_port(self.core_cfg)}/{game_code}/{game_ver}/",
                f"{self.core_cfg.server.hostname}",
            )

        return (
            f"http://{self.core_cfg.server.hostname}/{game_code}/{game_ver}/",
            f"{self.core_cfg.server.hostname}",
        )

    def setup(self):
        if (
            self.game_cfg.uploads.photos
            and self.game_cfg.uploads.photos_dir
            and not path.exists(self.game_cfg.uploads.photos_dir)
        ):
            try:
                mkdir(self.game_cfg.uploads.photos_dir)
            except Exception:
                self.logger.error(
                    f"Failed to make photo upload directory at {self.game_cfg.uploads.photos_dir}"
                )

        if (
            self.game_cfg.uploads.movies
            and self.game_cfg.uploads.movies_dir
            and not path.exists(self.game_cfg.uploads.movies_dir)
        ):
            try:
                mkdir(self.game_cfg.uploads.movies_dir)
            except Exception:
                self.logger.error(
                    f"Failed to make movie upload directory at {self.game_cfg.uploads.movies_dir}"
                )

    async def handle_movie(self, request: Request):
        return JSONResponse()
    
    async def handle_usbdl(self, request: Request):
        return Response("OK")

    async def handle_deliver(self, request: Request):
        return Response(status_code=404)

    async def handle_mai(self, request: Request) -> bytes:
        endpoint: str = request.path_params.get('endpoint')
        version: int = request.path_params.get('version')
        if endpoint.lower() == "ping":
            return Response(zlib.compress(b'{"returnCode": "1"}'))
        
        req_raw = await request.body()
        internal_ver = 0
        client_ip = Utils.get_ip_addr(request)
        
        if version < 110:  # 1.0
            internal_ver = Mai2Constants.VER_MAIMAI
        elif version >= 110 and version < 120:  # Plus
            internal_ver = Mai2Constants.VER_MAIMAI_PLUS
        elif version >= 120 and version < 130:  # Green
            internal_ver = Mai2Constants.VER_MAIMAI_GREEN
        elif version >= 130 and version < 140:  # Green Plus
            internal_ver = Mai2Constants.VER_MAIMAI_GREEN_PLUS
        elif version >= 140 and version < 150:  # Orange
            internal_ver = Mai2Constants.VER_MAIMAI_ORANGE
        elif version >= 150 and version < 160:  # Orange Plus
            internal_ver = Mai2Constants.VER_MAIMAI_ORANGE_PLUS
        elif version >= 160 and version < 170:  # Pink
            internal_ver = Mai2Constants.VER_MAIMAI_PINK
        elif version >= 170 and version < 180:  # Pink Plus
            internal_ver = Mai2Constants.VER_MAIMAI_PINK_PLUS
        elif version >= 180 and version < 185:  # Murasaki
            internal_ver = Mai2Constants.VER_MAIMAI_MURASAKI
        elif version >= 185 and version < 190:  # Murasaki Plus
            internal_ver = Mai2Constants.VER_MAIMAI_MURASAKI_PLUS
        elif version >= 190 and version < 195:  # Milk
            internal_ver = Mai2Constants.VER_MAIMAI_MILK
        elif version >= 195 and version < 197:  # Milk Plus
            internal_ver = Mai2Constants.VER_MAIMAI_MILK_PLUS
        elif version >= 197:  # Finale
            internal_ver = Mai2Constants.VER_MAIMAI_FINALE

        try:
            unzip = zlib.decompress(req_raw)

        except zlib.error as e:
            self.logger.error(
                f"Failed to decompress v{version} {endpoint} request -> {e}"
            )
            return Response(zlib.compress(b'{"stat": "0"}'))

        req_data = json.loads(unzip)

        self.logger.info(f"v{version} {endpoint} request from {client_ip}")
        self.logger.debug(req_data)

        func_to_find = "handle_" + inflection.underscore(endpoint) + "_request"
        handler_cls = self.versions[internal_ver](self.core_cfg, self.game_cfg)

        if not hasattr(handler_cls, func_to_find):
            self.logger.warning(f"Unhandled v{version} request {endpoint}")
            resp = {"returnCode": 1}

        else:
            try:
                handler = getattr(handler_cls, func_to_find)
                resp = await handler(req_data)

            except Exception as e:
                self.logger.error(f"Error handling v{version} method {endpoint} - {e}")
                return Response(zlib.compress(b'{"returnCode": "0"}'))

        if resp is None:
            resp = {"returnCode": 1}

        self.logger.debug(f"Response {resp}")

        return Response(zlib.compress(json.dumps(resp, ensure_ascii=False).encode("utf-8")))

    async def handle_mai2(self, request: Request) -> bytes:
        endpoint: str = request.path_params.get('endpoint')
        version: int = request.path_params.get('version')
        game_code = request.path_params.get('game')

        if endpoint.lower() == "ping":
            return Response(zlib.compress(b'{"returnCode": "1"}'))

        req_raw = await request.body()
        internal_ver = 0
        client_ip = Utils.get_ip_addr(request)
        encrypted = False
        
        if game_code == "SDEZ": # JP
          if version < 110:  # 1.0
              internal_ver = Mai2Constants.VER_MAIMAI_DX
          elif version >= 110 and version < 114:  # PLUS
              internal_ver = Mai2Constants.VER_MAIMAI_DX_PLUS
          elif version >= 114 and version < 117:  # Splash
              internal_ver = Mai2Constants.VER_MAIMAI_DX_SPLASH
          elif version >= 117 and version < 120:  # Splash PLUS
              internal_ver = Mai2Constants.VER_MAIMAI_DX_SPLASH_PLUS
          elif version >= 120 and version < 125:  # UNiVERSE
              internal_ver = Mai2Constants.VER_MAIMAI_DX_UNIVERSE
          elif version >= 125 and version < 130:  # UNiVERSE PLUS
              internal_ver = Mai2Constants.VER_MAIMAI_DX_UNIVERSE_PLUS
          elif version >= 130 and version < 135:  # FESTiVAL
              internal_ver = Mai2Constants.VER_MAIMAI_DX_FESTIVAL
          elif version >= 135 and version < 140:  # FESTiVAL PLUS
              internal_ver = Mai2Constants.VER_MAIMAI_DX_FESTIVAL_PLUS
          elif version >= 140:  # BUDDiES
              internal_ver = Mai2Constants.VER_MAIMAI_DX_BUDDIES
        elif game_code == "SDGA": # Int
          if version < 105:  # 1.0
              internal_ver = Mai2Constants.VER_MAIMAI_DX
          elif version >= 105 and version < 110:  # PLUS
              internal_ver = Mai2Constants.VER_MAIMAI_DX_PLUS
          elif version >= 110 and version < 115:  # Splash
              internal_ver = Mai2Constants.VER_MAIMAI_DX_SPLASH
          elif version >= 115 and version < 120:  # Splash PLUS
              internal_ver = Mai2Constants.VER_MAIMAI_DX_SPLASH_PLUS
          elif version >= 120 and version < 125:  # UNiVERSE
              internal_ver = Mai2Constants.VER_MAIMAI_DX_UNIVERSE
          elif version >= 125 and version < 130:  # UNiVERSE PLUS
              internal_ver = Mai2Constants.VER_MAIMAI_DX_UNIVERSE_PLUS
          elif version >= 130 and version < 135:  # FESTiVAL
              internal_ver = Mai2Constants.VER_MAIMAI_DX_FESTIVAL
          elif version >= 135 and version < 140:  # FESTiVAL PLUS
              internal_ver = Mai2Constants.VER_MAIMAI_DX_FESTIVAL_PLUS
        elif game_code == "SDGB": # CN
            if version < 130:  # Maimai DX CN 2023 (FESTiVAL)
                internal_ver = Mai2Constants.VER_MAIMAI_DX
            if 130 <= version < 135:  # Maimai DX CN 2023 (FESTiVAL)
                internal_ver = Mai2Constants.VER_MAIMAI_DX_FESTIVAL
            if 140 <= version < 145:  # Maimai DX CN 2023 (FESTiVAL)
                internal_ver = Mai2Constants.VER_MAIMAI_DX_BUDDIES

        try:
            unzip = zlib.decompress(req_raw)

        except zlib.error as e:
            self.logger.error(
                f"Failed to decompress v{version} {endpoint} request -> {e}"
            )
            return Response(zlib.compress(b'{"stat": "0"}'))


        if all(c in string.hexdigits for c in endpoint) and len(endpoint) == 32:
            # If we get a 32 character long hex string, it's a hash and we're
            # dealing with an encrypted request. False positives shouldn't happen
            # as long as requests are suffixed with `Api`.
            if internal_ver not in self.hash_table:
                self.logger.error(
                    "v%s does not support encryption or no keys entered",
                    version,
                )
                return Response(zlib.compress(b'{"stat": "0"}'))
            elif endpoint.lower() not in self.hash_table[internal_ver]:
                self.logger.error(
                    "No hash found for v%s endpoint %s",
                    version, endpoint
                )
                return Response(zlib.compress(b'{"stat": "0"}'))
            
            endpoint = self.hash_table[internal_ver][endpoint.lower()]

            try:
                crypt = CipherAES(
                    bytes.fromhex(self.game_cfg.crypto.keys[internal_ver][0]),
                    bytes.fromhex(self.game_cfg.crypto.keys[internal_ver][1]),
                )

                decrypted = crypt.decrypt(unzip)

            except Exception as e:
                self.logger.error(
                    "Failed to decrypt v%s request to %s",
                    version, endpoint,
                    exc_info=e,
                )
                return Response(zlib.compress(b'{"stat": "0"}'))

            encrypted = True


        req_data = json.loads(decrypted if encrypted else unzip)

        
        if (
            not encrypted
            and self.game_cfg.crypto.encrypted_only
            and version >= 110
        ):
            self.logger.error(
                "Unencrypted v%s %s request, but config is set to encrypted only: %r",
                version, endpoint, req_raw
            )
            return Response(zlib.compress(b'{"stat": "0"}'))            



        self.logger.info(f"v{version} {endpoint} request from {client_ip}")
        self.logger.debug(req_data)

        if game_code == Mai2Constants.GAME_CODE_DX_INT:
            endpoint = endpoint.replace("MaimaiExp", "")
        elif game_code == Mai2Constants.GAME_CODE_DX_CHN:
            endpoint = endpoint.replace("MaimaiChn", "")


        func_to_find = "handle_" + inflection.underscore(endpoint) + "_request"
        handler_cls = self.versions[internal_ver](self.core_cfg, self.game_cfg)

        if not hasattr(handler_cls, func_to_find):
            self.logger.warning(f"Unhandled v{version} request {endpoint}")
            resp = {"returnCode": 1}

        else:
            try:
                handler = getattr(handler_cls, func_to_find)
                resp = await handler(req_data)

            except Exception as e:
                self.logger.error(f"Error handling v{version} method {endpoint} - {e}")
                return Response(zlib.compress(b'{"stat": "0"}'))

        if resp is None:
            resp = {"returnCode": 1}

        self.logger.debug(f"Response {resp}")

        if not encrypted or version < 110:
            return Response(zlib.compress(json.dumps(resp, ensure_ascii=False).encode("utf-8")))
        
        # padded = pad(zipped, 16)

        crypt = CipherAES(
            bytes.fromhex(self.game_cfg.crypto.keys[internal_ver][0]),
            bytes.fromhex(self.game_cfg.crypto.keys[internal_ver][1]),
        )

        return Response(
            zlib.compress(crypt.encrypt(json.dumps(resp, ensure_ascii=False).encode("utf-8")))
        )


    async def handle_old_srv(self, request: Request) -> bytes:
        endpoint = request.path_params.get('endpoint')
        version = request.path_params.get('version')
        self.logger.info(f"v{version} old server {endpoint}")
        return Response(zlib.compress(b"ok"))

    async def handle_old_srv_userdata(self, request: Request) -> bytes:
        endpoint = request.path_params.get('endpoint')
        version = request.path_params.get('version')
        self.logger.info(f"v{version} old server {endpoint}")
        return Response(zlib.compress(b"{}"))
