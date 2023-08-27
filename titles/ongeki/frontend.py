import yaml
import jinja2
from twisted.web.http import Request
from os import path
from twisted.web.server import Session

from core.frontend import FE_Base, IUserSession
from core.config import CoreConfig

from titles.ongeki.config import OngekiConfig
from titles.ongeki.const import OngekiConstants
from titles.ongeki.database import OngekiData
# from titles.ongeki.read import OngekiReader


class OngekiFrontend(FE_Base):
    def __init__(
        self, cfg: CoreConfig, environment: jinja2.Environment, cfg_dir: str
    ) -> None:
        super().__init__(cfg, environment)
        self.data = OngekiData(cfg)
        self.game_cfg = OngekiConfig()
        if path.exists(f"{cfg_dir}/{OngekiConstants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{OngekiConstants.CONFIG_NAME}"))
            )
        self.nav_name = "O.N.G.E.K.I."

    def render_GET(self, request: Request) -> bytes:
        template = self.environment.get_template(
            "titles/ongeki/frontend/ongeki_index.jinja"
        )
        sesh: Session = request.getSession()
        usr_sesh = IUserSession(sesh)
        
        return template.render(
            title=f"{self.core_config.server.name} | {self.nav_name}",
            game_list=self.environment.globals["game_list"],
            sesh=vars(usr_sesh)
        ).encode("utf-16")
