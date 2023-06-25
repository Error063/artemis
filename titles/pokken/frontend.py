import yaml
import jinja2
from twisted.web.http import Request
from os import path
from twisted.web.server import Session

from core.frontend import FE_Base, IUserSession
from core.config import CoreConfig
from .database import PokkenData
from .config import PokkenConfig
from .const import PokkenConstants


class PokkenFrontend(FE_Base):
    def __init__(
        self, cfg: CoreConfig, environment: jinja2.Environment, cfg_dir: str
    ) -> None:
        super().__init__(cfg, environment)
        self.data = PokkenData(cfg)
        self.game_cfg = PokkenConfig()
        if path.exists(f"{cfg_dir}/{PokkenConstants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{PokkenConstants.CONFIG_NAME}"))
            )
        self.nav_name = "Pokken"

    def render_GET(self, request: Request) -> bytes:
        template = self.environment.get_template(
            "titles/pokken/frontend/pokken_index.jinja"
        )

        sesh: Session = request.getSession()
        usr_sesh = IUserSession(sesh)

        return template.render(
            title=f"{self.core_config.server.name} | {self.nav_name}",
            game_list=self.environment.globals["game_list"],
            sesh=vars(usr_sesh)
        ).encode("utf-16")
