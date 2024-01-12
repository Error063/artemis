import yaml
import jinja2
from typing import List
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from starlette.routing import Route
from os import path

from core.frontend import FE_Base, UserSession
from core.config import CoreConfig
from .database import PokkenData
from .config import PokkenConfig
from .const import PokkenConstants


class PokkenFrontend(FE_Base):
    SN_PREFIX = PokkenConstants.SERIAL_IDENT
    NETID_PREFIX = PokkenConstants.NETID_PREFIX
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
    
    def get_routes(self) -> List[Route]:
        return [
            Route("/", self.render_GET, methods=['GET']),
            Route("/update.name", self.change_name, methods=['POST']),
        ]

    async def render_GET(self, request: Request) -> Response:
        template = self.environment.get_template(
            "titles/pokken/templates/pokken_index.jinja"
        )
        pf = None
        
        usr_sesh = self.validate_session(request)
        if not usr_sesh:
            usr_sesh = UserSession()
            
        else:
            profile = await self.data.profile.get_profile(usr_sesh.user_id)
            if profile is not None and profile['trainer_name']:
                pf = profile._asdict()
        
        if "e" in request.query_params:
            try:
                err = int(request.query_params.get("e", 0))
            except Exception:
                err = 0

        else:
            err = 0
        
        if "s" in request.query_params:
            try:
                succ = int(request.query_params.get("s", 0))
            except Exception:
                succ = 0

        else:
            succ = 0

        return Response(template.render(
            title=f"{self.core_config.server.name} | {self.nav_name}",
            game_list=self.environment.globals["game_list"],
            sesh=vars(usr_sesh),
            profile=pf,
            error=err,
            success=succ
        ), media_type="text/html; charset=utf-16")
    
    async def change_name(self, request: Request) -> RedirectResponse:
        usr_sesh = self.validate_session(request)
        if not usr_sesh:
            return RedirectResponse("/game/pokken/?e=9", 303)
        
        frm = await request.form()
        new_name = frm.get("new_name")
        gender = frm.get("new_gender", 1)
        
        if len(new_name) > 14:
            return RedirectResponse("/game/pokken/?e=8", 303)
        
        if not gender.isdigit():
            return RedirectResponse("/game/pokken/?e=4", 303)
        
        gender = int(gender)
        
        if gender != 1 and gender != 2:
            return RedirectResponse("/game/pokken/?e=4", 303) # no code for this yet, whatever
        
        await self.data.profile.set_profile_name(usr_sesh.user_id, new_name, gender)
        
        return RedirectResponse("/game/pokken/?s=1", 303)
