import yaml
import jinja2
from twisted.web.http import Request

from core.frontend import FE_Base
from core.config import CoreConfig
from titles.wacca.database import WaccaData
from titles.wacca.config import WaccaConfig

class WaccaFrontend(FE_Base):
    def __init__(self, cfg: CoreConfig, environment: jinja2.Environment, cfg_dir: str) -> None:
        super().__init__(cfg, environment)
        self.data = WaccaData(cfg)
        self.game_cfg = WaccaConfig()
        self.game_cfg.update(yaml.safe_load(open(f"{cfg_dir}/wacca.yaml")))
    
    def render_GET(self, request: Request) -> bytes:
        return b""
