from twisted.internet.protocol import Factory, Protocol
import logging, coloredlogs
from Crypto.Cipher import AES
import struct
from typing import Dict, Tuple, Callable, Union
from typing_extensions import Final
from logging.handlers import TimedRotatingFileHandler

from core.config import CoreConfig
from core.data import Data
from .adb_handlers import *


class AimedbProtocol(Protocol):
    request_list: Dict[int, Tuple[Callable[[bytes, int], Union[ADBBaseResponse, bytes]], int, str]] = {}

    def __init__(self, core_cfg: CoreConfig) -> None:
        self.logger = logging.getLogger("aimedb")
        self.config = core_cfg
        self.data = Data(core_cfg)
        if core_cfg.aimedb.key == "":
            self.logger.error("!!!KEY NOT SET!!!")
            exit(1)

        self.register_handler(0x01, 0x03, self.handle_felica_lookup, 'felica_lookup')
        self.register_handler(0x02, 0x03, self.handle_felica_register, 'felica_register')

        self.register_handler(0x04, 0x06, self.handle_lookup, 'lookup')
        self.register_handler(0x05, 0x06, self.handle_register, 'register')

        self.register_handler(0x07, 0x08, self.handle_status_log, 'status_log')
        self.register_handler(0x09, 0x0A, self.handle_log, 'aime_log')       

        self.register_handler(0x0B, 0x0C, self.handle_campaign, 'campaign')
        self.register_handler(0x0D, 0x0E, self.handle_campaign_clear, 'campaign_clear')

        self.register_handler(0x0F, 0x10, self.handle_lookup_ex, 'lookup_ex')
        self.register_handler(0x11, 0x12, self.handle_felica_lookup_ex, 'felica_lookup_ex')

        self.register_handler(0x13, 0x14, self.handle_log_ex, 'aime_log_ex')
        self.register_handler(0x64, 0x65, self.handle_hello, 'hello')
        self.register_handler(0x66, 0, self.handle_goodbye, 'goodbye')
    
    def register_handler(self, cmd: int, resp:int, handler: Callable[[bytes, int], Union[ADBBaseResponse, bytes]], name: str) -> None:
        self.request_list[cmd] = (handler, resp, name)

    def append_padding(self, data: bytes):
        """Appends 0s to the end of the data until it's at the correct size"""
        length = struct.unpack_from("<H", data, 6)
        padding_size = length[0] - len(data)
        data += bytes(padding_size)
        return data

    def connectionMade(self) -> None:
        self.logger.debug(f"{self.transport.getPeer().host} Connected")

    def connectionLost(self, reason) -> None:
        self.logger.debug(
            f"{self.transport.getPeer().host} Disconnected - {reason.value}"
        )

    def dataReceived(self, data: bytes) -> None:
        cipher = AES.new(self.config.aimedb.key.encode(), AES.MODE_ECB)

        try:
            decrypted = cipher.decrypt(data)
        
        except Exception as e:
            self.logger.error(f"Failed to decrypt {data.hex()} because {e}")
            return None

        self.logger.debug(f"{self.transport.getPeer().host} wrote {decrypted.hex()}")

        try:
            head = ADBHeader.from_data(decrypted)
        
        except ADBHeaderException as e:
            self.logger.error(f"Error parsing ADB header: {e}")
            try:    
                encrypted = cipher.encrypt(ADBBaseResponse().make())
                self.transport.write(encrypted)

            except Exception as e:
                self.logger.error(f"Failed to encrypt default response because {e}")
            
            return

        handler, resp_code, name = self.request_list.get(head.cmd, (self.handle_default, None, 'default'))

        if resp_code is None:
            self.logger.warning(f"No handler for cmd {hex(head.cmd)}")
        
        elif resp_code > 0:
            self.logger.info(f"{name} from {head.keychip_id} ({head.game_id}) @ {self.transport.getPeer().host}")
        
        resp = handler(decrypted, resp_code)

        if type(resp) == ADBBaseResponse or issubclass(type(resp), ADBBaseResponse):
            resp_bytes = resp.make()
            if len(resp_bytes) != resp.head.length:
                resp_bytes = self.append_padding(resp_bytes)

        elif type(resp) == bytes:
            resp_bytes = resp
        
        elif resp is None: # Nothing to send, probably a goodbye
            return
        
        else:
            raise TypeError(f"Unsupported type returned by ADB handler for {name}: {type(resp)}")

        try:    
            encrypted = cipher.encrypt(resp_bytes)
            self.logger.debug(f"Response {resp_bytes.hex()}")
            self.transport.write(encrypted)

        except Exception as e:
            self.logger.error(f"Failed to encrypt {resp_bytes.hex()} because {e}")
        
    def handle_default(self, data: bytes, resp_code: int, length: int = 0x20) -> ADBBaseResponse:
        req = ADBHeader.from_data(data)
        return ADBBaseResponse(resp_code, length, 1, req.game_id, req.store_id, req.keychip_id, req.protocol_ver)

    def handle_hello(self, data: bytes, resp_code: int) -> ADBBaseResponse:
        return self.handle_default(data, resp_code)

    def handle_campaign(self, data: bytes, resp_code: int) -> ADBBaseResponse:
        h = ADBHeader.from_data(data)
        if h.protocol_ver >= 0x3030:
            req = h
            resp = ADBCampaignResponse.from_req(req)

        else:
            req = ADBOldCampaignRequest(data)
            
            self.logger.info(f"Legacy campaign request for campaign {req.campaign_id} (protocol version {hex(h.protocol_ver)})")
            resp = ADBOldCampaignResponse.from_req(req.head)
        
        # We don't currently support campaigns
        return resp

    def handle_lookup(self, data: bytes, resp_code: int) -> ADBBaseResponse:
        req = ADBLookupRequest(data)
        user_id = self.data.card.get_user_id_from_card(req.access_code)

        ret = ADBLookupResponse.from_req(req.head, user_id)
        
        self.logger.info(
            f"access_code {req.access_code} -> user_id {ret.user_id}"
        )
        return ret

    def handle_lookup_ex(self, data: bytes, resp_code: int) -> ADBBaseResponse:
        req = ADBLookupRequest(data)
        user_id = self.data.card.get_user_id_from_card(req.access_code)

        ret = ADBLookupExResponse.from_req(req.head, user_id)
        
        self.logger.info(
            f"access_code {req.access_code} -> user_id {ret.user_id}"
        )
        return ret

    def handle_felica_lookup(self, data: bytes, resp_code: int) -> bytes:
        """
        On official, I think a card has to be registered for this to actually work, but 
        I'm making the executive decision to not implement that and just kick back our
        faux generated access code. The real felica IDm -> access code conversion is done
        on the ADB server, which we do not and will not ever have access to. Because we can
        assure that all IDms will be unique, this basic 0-padded hex -> int conversion will
        be fine.
        """
        req = ADBFelicaLookupRequest(data)
        ac = self.data.card.to_access_code(req.idm)
        self.logger.info(
            f"idm {req.idm} ipm {req.pmm} -> access_code {ac}"
        )
        return ADBFelicaLookupResponse.from_req(req.head, ac)

    def handle_felica_register(self, data: bytes, resp_code: int) -> bytes:
        """
        I've never seen this used.
        """
        req = ADBFelicaLookupRequest(data)
        ac = self.data.card.to_access_code(req.idm)
        
        if self.config.server.allow_user_registration:
            user_id = self.data.user.create_user()

            if user_id is None:
                self.logger.error("Failed to register user!")
                user_id = -1

            else:
                card_id = self.data.card.create_card(user_id, ac)

                if card_id is None:
                    self.logger.error("Failed to register card!")
                    user_id = -1

            self.logger.info(
                f"Register access code {ac} (IDm: {req.idm} PMm: {req.pmm}) -> user_id {user_id}"
            )

        else:
            self.logger.info(
                f"Registration blocked!: access code {ac} (IDm: {req.idm} PMm: {req.pmm})"
            )

        return ADBFelicaLookupResponse.from_req(req.head, ac)

    def handle_felica_lookup_ex(self, data: bytes, resp_code: int) -> bytes:
        req = ADBFelicaLookup2Request(data)
        access_code = self.data.card.to_access_code(req.idm)
        user_id = self.data.card.get_user_id_from_card(access_code=access_code)

        if user_id is None:
            user_id = -1

        self.logger.info(
            f"idm {req.idm} ipm {req.pmm} -> access_code {access_code} user_id {user_id}"
        )

        return ADBFelicaLookup2Response.from_req(req.head, user_id, access_code)

    def handle_campaign_clear(self, data: bytes, resp_code: int) -> ADBBaseResponse:
        req = ADBCampaignClearRequest(data)

        resp = ADBCampaignClearResponse.from_req(req.head)

        # We don't support campaign stuff
        return resp

    def handle_register(self, data: bytes, resp_code: int) -> bytes:
        req = ADBLookupRequest(data)
        user_id = -1
        
        if self.config.server.allow_user_registration:
            user_id = self.data.user.create_user()

            if user_id is None:
                self.logger.error("Failed to register user!")
                user_id = -1

            else:
                card_id = self.data.card.create_card(user_id, req.access_code)

                if card_id is None:
                    self.logger.error("Failed to register card!")
                    user_id = -1

            self.logger.info(
                f"Register access code {req.access_code} -> user_id {user_id}"
            )

        else:
            self.logger.info(
                f"Registration blocked!: access code {req.access_code}"
            )

        resp = ADBLookupResponse.from_req(req.head, user_id)
        if resp.user_id <= 0:
            resp.head.status = ADBStatus.BAN_SYS # Closest we can get to a "You cannot register"

        return resp

    # TODO: Save these in some capacity, as deemed relevant
    def handle_status_log(self, data: bytes, resp_code: int) -> bytes:
        req = ADBStatusLogRequest(data)
        self.logger.info(f"User {req.aime_id} logged {req.status.name} event")
        return ADBBaseResponse(resp_code, 0x20, 1, req.head.game_id, req.head.store_id, req.head.keychip_id, req.head.protocol_ver)

    def handle_log(self, data: bytes, resp_code: int) -> bytes:
        req = ADBLogRequest(data)
        self.logger.info(f"User {req.aime_id} logged {req.status.name} event, credit_ct: {req.credit_ct} bet_ct: {req.bet_ct} won_ct: {req.won_ct}")
        return ADBBaseResponse(resp_code, 0x20, 1, req.head.game_id, req.head.store_id, req.head.keychip_id, req.head.protocol_ver)

    def handle_log_ex(self, data: bytes, resp_code: int) -> bytes:
        req = ADBLogExRequest(data)
        strs = []
        self.logger.info(f"Recieved {req.num_logs} or {len(req.logs)} logs")
        
        for x in range(req.num_logs):
            self.logger.debug(f"User {req.logs[x].aime_id} logged {req.logs[x].status.name} event, credit_ct: {req.logs[x].credit_ct} bet_ct: {req.logs[x].bet_ct} won_ct: {req.logs[x].won_ct}")
        return ADBBaseResponse(resp_code, 0x20, 1, req.head.game_id, req.head.store_id, req.head.keychip_id, req.head.protocol_ver)

    def handle_goodbye(self, data: bytes, resp_code: int) -> None:
        self.logger.info(f"goodbye from {self.transport.getPeer().host}")
        self.transport.loseConnection()
        return

class AimedbFactory(Factory):
    protocol = AimedbProtocol

    def __init__(self, cfg: CoreConfig) -> None:
        self.config = cfg
        log_fmt_str = "[%(asctime)s] Aimedb | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        self.logger = logging.getLogger("aimedb")

        fileHandler = TimedRotatingFileHandler(
            "{0}/{1}.log".format(self.config.server.log_dir, "aimedb"),
            when="d",
            backupCount=10,
        )
        fileHandler.setFormatter(log_fmt)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)

        self.logger.setLevel(self.config.aimedb.loglevel)
        coloredlogs.install(
            level=cfg.aimedb.loglevel, logger=self.logger, fmt=log_fmt_str
        )

        if self.config.aimedb.key == "":
            self.logger.error("Please set 'key' field in your config file.")
            exit(1)

        self.logger.info(f"Ready on port {self.config.aimedb.port}")

    def buildProtocol(self, addr):
        return AimedbProtocol(self.config)
