import hashlib
import json
import logging
from logging.handlers import TimedRotatingFileHandler
from typing import Dict

import coloredlogs
from starlette.responses import PlainTextResponse
from twisted.web.http import Request

from core.adb_handlers.base import ChimeDBStatus
from core.config import CoreConfig
from core.data import Data


class ChimeServlet:
    def __init__(self, core_cfg: CoreConfig, cfg_folder: str) -> None:
        self.config = core_cfg
        self.config_folder = cfg_folder

        self.data = Data(core_cfg)

        self.logger = logging.getLogger("chimedb")
        if not hasattr(self.logger, "initted"):
            log_fmt_str = "[%(asctime)s] Chimedb | %(levelname)s | %(message)s"
            log_fmt = logging.Formatter(log_fmt_str)

            fileHandler = TimedRotatingFileHandler(
                "{0}/{1}.log".format(self.config.server.log_dir, "chimedb"),
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
                level=core_cfg.aimedb.loglevel, logger=self.logger, fmt=log_fmt_str
            )
            self.logger.initted = True

        if not core_cfg.chimedb.key:
            self.logger.error("!!!KEY NOT SET!!!")
            exit(1)

        self.logger.info("Serving")

    async def handle_qr_alive(self, request: Request):
        return PlainTextResponse("alive")

    async def handle_qr_lookup(self, request: Request) -> bytes:
        req = json.loads(await request.body())
        access_code = req["qrCode"][-20:]
        timestamp = req["timestamp"]

        try:
            userId = await self._lookup(access_code)
            data = json.dumps({
                "userID": userId,
                "errorID": await self._lookup_user_status(access_code),
                "timestamp": timestamp,
                "key": self._hash_key(userId, timestamp)
            })
        except Exception as e:

            self.logger.error(e.with_traceback(None))

            data = json.dumps({
                "userID": -1,
                "errorID": ChimeDBStatus.DB_ACCESS_FAIL,
                "timestamp": timestamp,
                "key": self._hash_key(-1, timestamp)
            })

        return PlainTextResponse(data)


    def _hash_key(self, chip_id, timestamp):
        input_string = f"{chip_id}{timestamp}{self.config.chimedb.key}"
        hash_object = hashlib.sha256(input_string.encode('utf-8'))
        hex_dig = hash_object.hexdigest()

        formatted_hex = format(int(hex_dig, 16), '064x').upper()

        return formatted_hex

    async def _lookup(self, access_code):
        user_id = await self.data.card.get_user_id_from_card(access_code)

        self.logger.info(f"access_code {access_code} -> user_id {user_id}")

        if not user_id or user_id <= 0:
            user_id = await self._register(access_code)

        return user_id

    async def _lookup_user_status(self, access_code):
        is_banned = await self.data.card.get_card_banned(access_code)
        is_locked = await self.data.card.get_card_locked(access_code)

        if is_banned and is_locked:
            return ChimeDBStatus.LOCK_BAN_SYSTEM_USER
        elif is_banned:
            return ChimeDBStatus.LOCK_BAN_SYSTEM
        elif is_locked:
            return ChimeDBStatus.LOCK_USER

    async def _register(self, access_code):
        user_id = -1

        if self.config.server.allow_user_registration:
            user_id = await self.data.user.create_user()

            if user_id is None:
                self.logger.error("Failed to register user!")
                user_id = -1
            else:
                card_id = await self.data.card.create_card(user_id, access_code)

                if card_id is None:
                    self.logger.error("Failed to register card!")
                    user_id = -1

            self.logger.info(
                f"Register access code {access_code} -> user_id {user_id}"
            )
        else:
            self.logger.info(f"Registration blocked!: access code {access_code}")

        return user_id
