from typing import Dict, Any, Optional
from types import ModuleType
from starlette.requests import Request
import logging
import importlib
from os import walk
import jwt
from base64 import b64decode
from datetime import datetime, timezone

from .config import CoreConfig

class Utils:
    real_title_port = None
    real_title_port_ssl = None
    @classmethod
    def get_all_titles(cls) -> Dict[str, ModuleType]:
        ret: Dict[str, Any] = {}

        for root, dirs, files in walk("titles"):
            for dir in dirs:
                if not dir.startswith("__"):
                    try:
                        mod = importlib.import_module(f"titles.{dir}")
                        if hasattr(mod, "game_codes") and hasattr(
                            mod, "index"
                        ):  # Minimum required to function
                            ret[dir] = mod

                    except ImportError as e:
                        logging.getLogger("core").error(f"get_all_titles: {dir} - {e}")
                        raise
            return ret

    @classmethod
    def get_ip_addr(cls, req: Request) -> str:
        ip = req.headers.get("x-forwarded-for", req.client.host)
        return ip.split(", ")[0]
    
    @classmethod
    def get_title_port(cls, cfg: CoreConfig):
        if cls.real_title_port is not None: return cls.real_title_port

        cls.real_title_port = cfg.server.proxy_port if cfg.server.is_using_proxy and cfg.server.proxy_port else cfg.server.port
        
        return cls.real_title_port
    
    @classmethod
    def get_title_port_ssl(cls, cfg: CoreConfig):
        if cls.real_title_port_ssl is not None: return cls.real_title_port_ssl

        cls.real_title_port_ssl = cfg.server.proxy_port_ssl if cfg.server.is_using_proxy and cfg.server.proxy_port_ssl else Utils.get_title_port(cfg)
        
        return cls.real_title_port_ssl

def create_sega_auth_key(aime_id: int, game: str, place_id: int, keychip_id: str, b64_secret: str, exp_seconds: int = 86400, err_logger: str = 'aimedb') -> Optional[str]:
    logger = logging.getLogger(err_logger)
    try:
        return jwt.encode({ "aime_id": aime_id, "game": game, "place_id": place_id, "keychip_id": keychip_id, "exp": int(datetime.now(tz=timezone.utc).timestamp()) + exp_seconds }, b64decode(b64_secret), algorithm="HS256")
    except jwt.InvalidKeyError:
        logger.error("Failed to encode Sega Auth Key because the secret is invalid!")
        return None
    except Exception as e:
        logger.error(f"Unknown exception occoured when encoding Sega Auth Key! {e}")
        return None

def decode_sega_auth_key(token: str, b64_secret: str, err_logger: str = 'aimedb') -> Optional[Dict]:
    logger = logging.getLogger(err_logger)
    try:
        return jwt.decode(token, "secret", b64decode(b64_secret), algorithms=["HS256"], options={"verify_signature": True})
    except jwt.ExpiredSignatureError:
        logger.error("Sega Auth Key failed to validate due to an expired signature!")
        return None
    except jwt.InvalidSignatureError:
        logger.error("Sega Auth Key failed to validate due to an invalid signature!")
        return None
    except jwt.DecodeError as e:
        logger.error(f"Sega Auth Key failed to decode! {e}")
        return None
    except jwt.InvalidTokenError as e:
        logger.error(f"Sega Auth Key is invalid! {e}")
        return None
    except Exception as e:
        logger.error(f"Unknown exception occoured when decoding Sega Auth Key! {e}")
        return None
    