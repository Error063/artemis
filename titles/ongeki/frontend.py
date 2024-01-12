from typing import List
from starlette.routing import Route
import yaml
import jinja2
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from os import path

from core.frontend import FE_Base, UserSession
from core.config import CoreConfig

from titles.ongeki.config import OngekiConfig
from titles.ongeki.const import OngekiConstants
from titles.ongeki.database import OngekiData
from titles.ongeki.base import OngekiBase


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
        self.version_list = OngekiConstants.VERSION_NAMES
    
    def get_routes(self) -> List[Route]:
        return [
            Route("/", self.render_GET)
        ]

    async def render_GET(self, request: Request) -> bytes:
        template = self.environment.get_template(
            "titles/ongeki/templates/ongeki_index.jinja"
        )
        usr_sesh = self.validate_session(request)
        if not usr_sesh:
            usr_sesh = UserSession()

        self.version = usr_sesh.ongeki_version
        if usr_sesh.user_id > 0:
            profile_data =self.data.profile.get_profile_data(usr_sesh.user_id, self.version)
            rival_list = await self.data.profile.get_rivals(usr_sesh.user_id)
            rival_data = {
                "userRivalList": rival_list,
                "userId": usr_sesh.user_id
            }

            # Hay1tsme 01/09/2024: ??????????????????????????????????????????????????????????????
            rival_info = await OngekiBase.handle_get_user_rival_data_api_request(self, rival_data)

            return Response(template.render(
                data=self.data.profile,
                title=f"{self.core_config.server.name} | {self.nav_name}",
                game_list=self.environment.globals["game_list"],
                gachas=self.game_cfg.gachas.enabled_gachas,
                profile_data=profile_data,
                rival_info=rival_info["userRivalDataList"],
                version_list=self.version_list,
                version=self.version,
                sesh=vars(usr_sesh)
            ), media_type="text/html; charset=utf-16")
        else:
            return RedirectResponse("/gate/", 303)
    
    async def render_POST(self, request: Request):
        uri = request.uri.decode()
        usr_sesh = self.validate_session(request)
        if not usr_sesh:
            usr_sesh = UserSession()

        if usr_sesh.user_id > 0:
            if uri == "/game/ongeki/rival.add":
                rival_id = request.args[b"rivalUserId"][0].decode()
                await self.data.profile.put_rival(usr_sesh.user_id, rival_id)
                # self.logger.info(f"{usr_sesh.user_id} added a rival")
                return RedirectResponse(b"/game/ongeki/", 303)
            
            elif uri == "/game/ongeki/rival.delete":
                rival_id = request.args[b"rivalUserId"][0].decode()
                await self.data.profile.delete_rival(usr_sesh.user_id, rival_id)
                # self.logger.info(f"{response}")
                return RedirectResponse(b"/game/ongeki/", 303)
            
            elif uri == "/game/ongeki/version.change":
                ongeki_version=request.args[b"version"][0].decode()
                if(ongeki_version.isdigit()):
                    usr_sesh.ongeki_version=int(ongeki_version)
                return RedirectResponse("/game/ongeki/", 303)
            
            else:
                Response("Something went wrong", status_code=500)
        else:
            return RedirectResponse("/gate/", 303)
