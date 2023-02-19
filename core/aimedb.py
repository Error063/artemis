from twisted.internet.protocol import Factory, Protocol
import logging, coloredlogs
from Crypto.Cipher import AES
import struct
from typing import Dict, Any
from logging.handlers import TimedRotatingFileHandler

from core.config import CoreConfig
from core.data import Data

class AimedbProtocol(Protocol):
    AIMEDB_RESPONSE_CODES = {
        "felica_lookup": 0x03,
        "lookup": 0x06,
        "log": 0x0a,
        "campaign": 0x0c,
        "touch": 0x0e,
        "lookup2": 0x10,
        "felica_lookup2": 0x12,
        "log2": 0x14,
        "hello": 0x65
    }

    request_list: Dict[int, Any] = {}

    def __init__(self, core_cfg: CoreConfig) -> None:
        self.logger = logging.getLogger("aimedb")
        self.config = core_cfg
        self.data = Data(core_cfg)
        if core_cfg.aimedb.key == "":
            self.logger.error("!!!KEY NOT SET!!!")
            exit(1)
        
        self.request_list[0x01] = self.handle_felica_lookup
        self.request_list[0x04] = self.handle_lookup
        self.request_list[0x05] = self.handle_register
        self.request_list[0x09] = self.handle_log        
        self.request_list[0x0b] = self.handle_campaign
        self.request_list[0x0d] = self.handle_touch
        self.request_list[0x0f] = self.handle_lookup2
        self.request_list[0x11] = self.handle_felica_lookup2
        self.request_list[0x13] = self.handle_log2
        self.request_list[0x64] = self.handle_hello

    def append_padding(self, data: bytes):
        """Appends 0s to the end of the data until it's at the correct size"""
        length = struct.unpack_from("<H", data, 6)
        padding_size = length[0] - len(data)
        data += bytes(padding_size)
        return data

    def connectionMade(self) -> None:
        self.logger.debug(f"{self.transport.getPeer().host} Connected")

    def connectionLost(self, reason) -> None:
        self.logger.debug(f"{self.transport.getPeer().host} Disconnected - {reason.value}")
    
    def dataReceived(self, data: bytes) -> None:
        cipher = AES.new(self.config.aimedb.key.encode(), AES.MODE_ECB)

        try:
            decrypted = cipher.decrypt(data)
        except:
            self.logger.error(f"Failed to decrypt {data.hex()}")
            return None

        self.logger.debug(f"{self.transport.getPeer().host} wrote {decrypted.hex()}")

        if not decrypted[1] == 0xa1 and not decrypted[0] == 0x3e:
            self.logger.error(f"Bad magic")
            return None

        req_code = decrypted[4]

        if req_code == 0x66:
            self.logger.info(f"goodbye from {self.transport.getPeer().host}")
            self.transport.loseConnection()
            return

        try:
            resp = self.request_list[req_code](decrypted)
            encrypted = cipher.encrypt(resp)
            self.logger.debug(f"Response {resp.hex()}")
            self.transport.write(encrypted)

        except KeyError:
            self.logger.error(f"Unknown command code {hex(req_code)}")
            return None

        except ValueError as e:
            self.logger.error(f"Failed to encrypt {resp.hex()} because {e}")
            return None
    
    def handle_campaign(self, data: bytes) -> bytes:
        self.logger.info(f"campaign from {self.transport.getPeer().host}")
        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["campaign"], 0x0200, 0x0001)
        return self.append_padding(ret)
    
    def handle_hello(self, data: bytes) -> bytes:
        self.logger.info(f"hello from {self.transport.getPeer().host}")
        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["hello"], 0x0020, 0x0001)
        return self.append_padding(ret)

    def handle_lookup(self, data: bytes) -> bytes:
        luid = data[0x20: 0x2a].hex()
        user_id = self.data.card.get_user_id_from_card(access_code=luid)

        if user_id is None: user_id = -1

        self.logger.info(f"lookup from {self.transport.getPeer().host}: luid {luid} -> user_id {user_id}")

        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["lookup"], 0x0130, 0x0001)
        ret += bytes(0x20 - len(ret))

        if user_id is None: ret += struct.pack("<iH", -1, 0)
        else: ret += struct.pack("<l", user_id)
        return self.append_padding(ret)

    def handle_lookup2(self, data: bytes) -> bytes:
        self.logger.info(f"lookup2")

        ret = bytearray(self.handle_lookup(data))
        ret[4] = self.AIMEDB_RESPONSE_CODES["lookup2"]

        return bytes(ret)

    def handle_felica_lookup(self, data: bytes) -> bytes:
        idm = data[0x20: 0x28].hex()
        pmm = data[0x28: 0x30].hex()
        access_code = self.data.card.to_access_code(idm)
        self.logger.info(f"felica_lookup from {self.transport.getPeer().host}: idm {idm} pmm {pmm} -> access_code {access_code}")

        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["felica_lookup"], 0x0030, 0x0001)
        ret += bytes(26)
        ret += bytes.fromhex(access_code)

        return self.append_padding(ret)

    def handle_felica_lookup2(self, data: bytes) -> bytes:
        idm = data[0x30: 0x38].hex()
        pmm = data[0x38: 0x40].hex()
        access_code = self.data.card.to_access_code(idm)
        user_id = self.data.card.get_user_id_from_card(access_code=access_code)

        if user_id is None: user_id = -1

        self.logger.info(f"felica_lookup2 from {self.transport.getPeer().host}: idm {idm} ipm {pmm} -> access_code {access_code} user_id {user_id}")

        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["felica_lookup2"], 0x0140, 0x0001)
        ret += bytes(22)
        ret += struct.pack("<lq", user_id, -1) # first -1 is ext_id, 3rd is access code
        ret += bytes.fromhex(access_code)
        ret += struct.pack("<l", 1)
        
        return self.append_padding(ret)
    
    def handle_touch(self, data: bytes) -> bytes:
        self.logger.info(f"touch from {self.transport.getPeer().host}")
        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["touch"], 0x0050, 0x0001)
        ret += bytes(5)
        ret += struct.pack("<3H", 0x6f, 0, 1)

        return self.append_padding(ret)

    def handle_register(self, data: bytes) -> bytes:        
        luid = data[0x20: 0x2a].hex()
        if self.config.server.allow_user_registration:
            user_id = self.data.user.create_user()

            if user_id is None: 
                user_id = -1
                self.logger.error("Failed to register user!")

            else:
                card_id = self.data.card.create_card(user_id, luid)

                if card_id is None: 
                    user_id = -1
                    self.logger.error("Failed to register card!")

            self.logger.info(f"register from {self.transport.getPeer().host}: luid {luid} -> user_id {user_id}")
        
        else:
            self.logger.info(f"register from {self.transport.getPeer().host} blocked!: luid {luid}")
            user_id = -1

        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["lookup"], 0x0030, 0x0001 if user_id > -1 else 0)
        ret += bytes(0x20 - len(ret))
        ret += struct.pack("<l", user_id)

        return self.append_padding(ret)

    def handle_log(self, data: bytes) -> bytes:
        # TODO: Save aimedb logs
        self.logger.info(f"log from {self.transport.getPeer().host}")
        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["log"], 0x0020, 0x0001)
        return self.append_padding(ret)

    def handle_log2(self, data: bytes) -> bytes:
        self.logger.info(f"log2 from {self.transport.getPeer().host}")
        ret = struct.pack("<5H", 0xa13e, 0x3087, self.AIMEDB_RESPONSE_CODES["log2"], 0x0040, 0x0001)
        ret += bytes(22)
        ret += struct.pack("H", 1)

        return self.append_padding(ret)

class AimedbFactory(Factory):
    protocol = AimedbProtocol
    def __init__(self, cfg: CoreConfig) -> None:
        self.config = cfg
        log_fmt_str = "[%(asctime)s] Aimedb | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        self.logger = logging.getLogger("aimedb")

        fileHandler = TimedRotatingFileHandler("{0}/{1}.log".format(self.config.server.log_dir, "aimedb"), when="d", backupCount=10)
        fileHandler.setFormatter(log_fmt)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        
        self.logger.setLevel(self.config.aimedb.loglevel)
        coloredlogs.install(level=cfg.aimedb.loglevel, logger=self.logger, fmt=log_fmt_str)
        
        if self.config.aimedb.key == "":
            self.logger.error("Please set 'key' field in your config file.")
            exit(1)

        self.logger.info(f"Ready on port {self.config.aimedb.port}")
    
    def buildProtocol(self, addr):
        return AimedbProtocol(self.config)
