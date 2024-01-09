import yaml
import jinja2
from starlette.requests import Request
from os import path
from twisted.web.server import Session

from core.frontend import FE_Base, IUserSession
from core.config import CoreConfig
from titles.wacca.database import WaccaData
from titles.wacca.config import WaccaConfig
from titles.wacca.const import WaccaConstants


class WaccaFrontend(FE_Base):
    def __init__(
        self, cfg: CoreConfig, environment: jinja2.Environment, cfg_dir: str
    ) -> None:
        super().__init__(cfg, environment)
        self.data = WaccaData(cfg)
        self.game_cfg = WaccaConfig()
        if path.exists(f"{cfg_dir}/{WaccaConstants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{WaccaConstants.CONFIG_NAME}"))
            )
        self.nav_name = "Wacca"

    async def render_GET(self, request: Request) -> bytes:
        template = self.environment.get_template(
            "titles/wacca/frontend/wacca_index.jinja"
        )
        sesh: Session = request.getSession()
        usr_sesh = IUserSession(sesh)
        
        return template.render(
            title=f"{self.core_config.server.name} | {self.nav_name}",
            game_list=self.environment.globals["game_list"],
            sesh=vars(usr_sesh)
        ).encode("utf-16")
