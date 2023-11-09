import struct

from core.utils import Utils
from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig
from ..const import IDZConstants


class IDZHandlerLoadServerInfo(IDZHandlerBase):
    cmd_codes = [0x0006] * IDZConstants.NUM_VERS
    rsp_codes = [0x0007] * IDZConstants.NUM_VERS
    name = "load_server_info1"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x04B0

    def handle(self, data: bytes) -> bytearray:
        ret = super().handle(data)
        offset = 0
        if self.version >= IDZConstants.VER_IDZ_210:
            offset = 2
        
        t_port = Utils.get_title_port(self.core_config)

        news_str = f"http://{self.core_config.title.hostname}:{t_port}/idz/news/news80**.txt"
        err_str = f"http://{self.core_config.title.hostname}:{t_port}/idz/error"

        len_hostname = len(self.core_config.title.hostname)
        len_news = len(news_str)
        len_error = len(err_str)

        struct.pack_into("<I", ret, 0x2 + offset, 1)  # Status
        struct.pack_into(
            f"{len_hostname}s",
            ret,
            0x4 + offset,
            self.core_config.title.hostname.encode(),
        )
        struct.pack_into("<I", ret, 0x84 + offset, self.game_cfg.ports.userdb)
        struct.pack_into("<I", ret, 0x86 + offset, self.game_cfg.ports.userdb + 1)

        struct.pack_into(
            f"{len_hostname}s",
            ret,
            0x88 + offset,
            self.core_config.title.hostname.encode(),
        )
        struct.pack_into("<I", ret, 0x108 + offset, self.game_cfg.ports.match - 1)
        struct.pack_into("<I", ret, 0x10A + offset, self.game_cfg.ports.match - 3)
        struct.pack_into("<I", ret, 0x10C + offset, self.game_cfg.ports.match - 2)

        struct.pack_into("<I", ret, 0x10E + offset, self.game_cfg.ports.match + 2)
        struct.pack_into("<I", ret, 0x110 + offset, self.game_cfg.ports.match + 3)
        struct.pack_into("<I", ret, 0x112 + offset, self.game_cfg.ports.match + 1)

        struct.pack_into(
            f"{len_hostname}s",
            ret,
            0x114 + offset,
            self.core_config.title.hostname.encode(),
        )
        struct.pack_into("<I", ret, 0x194 + offset, self.game_cfg.ports.echo + 2)

        struct.pack_into(
            f"{len_hostname}s",
            ret,
            0x0199 + offset,
            self.core_config.title.hostname.encode(),
        )
        struct.pack_into("<I", ret, 0x0219 + offset, self.game_cfg.ports.echo + 3)

        struct.pack_into(
            f"{len_hostname}s",
            ret,
            0x021C + offset,
            self.core_config.title.hostname.encode(),
        )
        struct.pack_into(
            f"{len_hostname}s",
            ret,
            0x029C + offset,
            self.core_config.title.hostname.encode(),
        )
        struct.pack_into(
            f"{len_hostname}s",
            ret,
            0x031C + offset,
            self.core_config.title.hostname.encode(),
        )

        struct.pack_into("<I", ret, 0x39C + offset, self.game_cfg.ports.echo)
        struct.pack_into("<I", ret, 0x39E + offset, self.game_cfg.ports.echo + 1)

        struct.pack_into(f"{len_news}s", ret, 0x03A0 + offset, news_str.encode())
        struct.pack_into(f"{len_error}s", ret, 0x0424 + offset, err_str.encode())

        return ret
