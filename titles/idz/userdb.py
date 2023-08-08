from twisted.internet.protocol import Factory, Protocol
import logging, coloredlogs
from Crypto.Cipher import AES
import struct
from typing import Dict, Optional, List, Type
from twisted.web import server, resource
from twisted.internet import reactor, endpoints
from twisted.web.http import Request
from routes import Mapper
import random
from os import walk
import importlib

from core.config import CoreConfig
from .database import IDZData
from .config import IDZConfig
from .const import IDZConstants
from .handlers import IDZHandlerBase

HANDLER_MAP: List[Dict]


class IDZKey:
    def __init__(self, n, d, e, hashN: int) -> None:
        self.N = n
        self.d = d
        self.e = e
        self.hashN = hashN


class IDZUserDBProtocol(Protocol):
    def __init__(
        self,
        core_cfg: CoreConfig,
        game_cfg: IDZConfig,
        keys: List[IDZKey],
        handlers: List[Dict],
    ) -> None:
        self.logger = logging.getLogger("idz")
        self.core_config = core_cfg
        self.game_config = game_cfg
        self.rsa_keys = keys
        self.handlers = handlers
        self.static_key = bytes.fromhex(self.game_config.server.aes_key)
        self.version = None
        self.version_internal = None
        self.skip_next = False

    def append_padding(self, data: bytes):
        """Appends 0s to the end of the data until it's at the correct size"""
        length = struct.unpack_from("<H", data, 6)
        padding_size = length[0] - len(data)
        data += bytes(padding_size)
        return data

    def connectionMade(self) -> None:
        self.logger.debug(f"{self.transport.getPeer().host} Connected")
        base = 0

        for i in range(len(self.static_key) - 1):
            shift = 8 * i
            byte = self.static_key[i]

            base |= byte << shift

        rsa_key = random.choice(self.rsa_keys)
        key_enc: int = pow(base, rsa_key.e, rsa_key.N)
        result = (
            key_enc.to_bytes(0x40, "little")
            + struct.pack("<I", 0x01020304)
            + rsa_key.hashN.to_bytes(4, "little")
        )

        self.logger.debug(f"Send handshake {result.hex()}")

        self.transport.write(result)

    def connectionLost(self, reason) -> None:
        self.logger.debug(
            f"{self.transport.getPeer().host} Disconnected - {reason.value}"
        )

    def dataReceived(self, data: bytes) -> None:
        self.logger.debug(f"Receive data {data.hex()}")
        crypt = AES.new(self.static_key, AES.MODE_ECB)
        
        try:
            data_dec = crypt.decrypt(data)
        
        except Exception as e:
            self.logger.error(f"Failed to decrypt UserDB request from {self.transport.getPeer().host} because {e} - {data.hex()}")
        
        self.logger.debug(f"Decrypt data {data_dec.hex()}")

        magic = struct.unpack_from("<I", data_dec, 0)[0]

        if magic == 0xFE78571D:
            # Ignore
            self.logger.info(f"Userdb serverbox request {data_dec.hex()}")
            self.skip_next = True

            self.transport.write(b"\x00")
            return

        elif magic == 0x01020304:
            self.version = int(data_dec[16:19].decode())

            if self.version == 110:
                self.version_internal = IDZConstants.VER_IDZ_110
            elif self.version == 130:
                self.version_internal = IDZConstants.VER_IDZ_130
            elif self.version == 210:
                self.version_internal = IDZConstants.VER_IDZ_210
            elif self.version == 230:
                self.version_internal = IDZConstants.VER_IDZ_230
            else:
                self.logger.warning(f"Bad version v{self.version}")
                self.version = None
                self.version_internal = None

            self.logger.debug(
                f"Userdb v{self.version} handshake response from {self.transport.getPeer().host}"
            )
            return

        elif self.skip_next:
            self.skip_next = False
            self.transport.write(b"\x00")
            return

        elif self.version is None:
            # We didn't get a handshake before, and this isn't one now, so we're up the creek
            self.logger.info(
                f"Bad UserDB request from from {self.transport.getPeer().host}"
            )
            self.transport.write(b"\x00")
            return

        cmd = struct.unpack_from("<H", data_dec, 0)[0]

        handler_cls: Optional[Type[IDZHandlerBase]] = self.handlers[
            self.version_internal
        ].get(cmd, None)
        if handler_cls is None:
            self.logger.warning(f"No handler for v{self.version} {hex(cmd)} cmd")
            handler_cls = IDZHandlerBase

        handler = handler_cls(self.core_config, self.game_config, self.version_internal)
        self.logger.info(
            f"Userdb v{self.version} {handler.name} request from {self.transport.getPeer().host}"
        )
        response = handler.handle(data_dec)

        self.logger.debug(f"Response: {response.hex()}")

        crypt = AES.new(self.static_key, AES.MODE_ECB)
        response_enc = crypt.encrypt(response)

        self.transport.write(response_enc)


class IDZUserDBFactory(Factory):
    protocol = IDZUserDBProtocol

    def __init__(
        self,
        cfg: CoreConfig,
        game_cfg: IDZConfig,
        keys: List[IDZKey],
        handlers: List[Dict],
    ) -> None:
        self.core_config = cfg
        self.game_config = game_cfg
        self.keys = keys
        self.handlers = handlers

    def buildProtocol(self, addr):
        return IDZUserDBProtocol(
            self.core_config, self.game_config, self.keys, self.handlers
        )


class IDZUserDBWeb(resource.Resource):
    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig):
        super().__init__()
        self.isLeaf = True
        self.core_config = core_cfg
        self.game_config = game_cfg
        self.logger = logging.getLogger("idz")

    def render_POST(self, request: Request) -> bytes:
        self.logger.info(
            f"IDZUserDBWeb POST from {request.getClientAddress().host} to {request.uri} with data {request.content.getvalue()}"
        )
        return b""

    def render_GET(self, request: Request) -> bytes:
        self.logger.info(
            f"IDZUserDBWeb GET from {request.getClientAddress().host} to {request.uri}"
        )
        return b""
