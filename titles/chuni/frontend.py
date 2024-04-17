from typing import List
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from os import path
import yaml
import jinja2

from core.frontend import FE_Base, UserSession
from core.config import CoreConfig
from .database import ChuniData
from .config import ChuniConfig
from .const import ChuniConstants


class ChuniFrontend(FE_Base):
    def __init__(
        self, cfg: CoreConfig, environment: jinja2.Environment, cfg_dir: str
    ) -> None:
        super().__init__(cfg, environment)
        self.data = ChuniData(cfg)
        self.game_cfg = ChuniConfig()
        if path.exists(f"{cfg_dir}/{ChuniConstants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{ChuniConstants.CONFIG_NAME}"))
            )
        self.nav_name = "Chunithm"

    def get_routes(self) -> List[Route]:
        return [
            Route("/", self.render_GET, methods=['GET']),
            Route("/update.name", self.update_name, methods=['POST']),
        ]

    async def render_GET(self, request: Request) -> bytes:
        template = self.environment.get_template(
            "titles/chuni/templates/chuni_index.jinja"
        )
        usr_sesh = self.validate_session(request)
        if not usr_sesh:
            usr_sesh = UserSession()
        
        return Response(template.render(
            title=f"{self.core_config.server.name} | {self.nav_name}",
            game_list=self.environment.globals["game_list"],
            sesh=vars(usr_sesh)
        ), media_type="text/html; charset=utf-8")

    async def update_name(self, request: Request) -> bytes:
        usr_sesh = self.validate_session(request)
        if not usr_sesh:
            return RedirectResponse("/gate/", 303)
        
        new_name: str = request.query_params.get('new_name', '')
        new_name_full = ""
        
        if not new_name:
            return RedirectResponse("/gate/?e=4", 303)
        
        if len(new_name) > 8:
            return RedirectResponse("/gate/?e=8", 303)
        
        for x in new_name: # FIXME: This will let some invalid characters through atm
            o = ord(x)
            try:
                if o == 0x20:
                    new_name_full += chr(0x3000)
                elif o < 0x7F and o > 0x20:
                    new_name_full += chr(o + 0xFEE0)
                elif o <= 0x7F:
                    self.logger.warn(f"Invalid ascii character {o:02X}")
                    return RedirectResponse("/gate/?e=4", 303)
                else:
                    new_name_full += x
            
            except Exception as e:
                self.logger.error(f"Something went wrong parsing character {o:04X} - {e}")
                return RedirectResponse("/gate/?e=4", 303)
        
        if not await self.data.profile.update_name(usr_sesh, new_name_full):
            return RedirectResponse("/gate/?e=999", 303)

        return RedirectResponse("/gate/?s=1", 303)