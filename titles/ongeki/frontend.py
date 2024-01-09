import yaml
import jinja2
from starlette.requests import Request
from os import path
from twisted.web.util import redirectTo
from twisted.web.server import Session

from core.frontend import FE_Base, IUserSession
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

    def render_GET(self, request: Request) -> bytes:
        template = self.environment.get_template(
            "titles/ongeki/frontend/ongeki_index.jinja"
        )
        sesh: Session = request.getSession()
        usr_sesh = IUserSession(sesh)
        self.version = usr_sesh.ongeki_version
        if getattr(usr_sesh, "userId", 0) != 0:
            profile_data =self.data.profile.get_profile_data(usr_sesh.userId, self.version)
            rival_list = self.data.profile.get_rivals(usr_sesh.userId)
            rival_data = {
                "userRivalList": rival_list,
                "userId": usr_sesh.userId
            }
            rival_info = OngekiBase.handle_get_user_rival_data_api_request(self, rival_data)

            return template.render(
                data=self.data.profile,
                title=f"{self.core_config.server.name} | {self.nav_name}",
                game_list=self.environment.globals["game_list"],
                gachas=self.game_cfg.gachas.enabled_gachas,
                profile_data=profile_data,
                rival_info=rival_info["userRivalDataList"],
                version_list=self.version_list,
                version=self.version,
                sesh=vars(usr_sesh)
            ).encode("utf-16")
        else:
            return redirectTo(b"/gate/", request)
    
    def render_POST(self, request: Request):
        uri = request.uri.decode()
        sesh: Session = request.getSession()
        usr_sesh = IUserSession(sesh)
        if hasattr(usr_sesh, "userId"):
            if uri == "/game/ongeki/rival.add":
                rival_id = request.args[b"rivalUserId"][0].decode()
                self.data.profile.put_rival(usr_sesh.userId, rival_id)
                # self.logger.info(f"{usr_sesh.userId} added a rival")
                return redirectTo(b"/game/ongeki/", request)
            
            elif uri == "/game/ongeki/rival.delete":
                rival_id = request.args[b"rivalUserId"][0].decode()
                self.data.profile.delete_rival(usr_sesh.userId, rival_id)
                # self.logger.info(f"{response}")
                return redirectTo(b"/game/ongeki/", request)
            
            elif uri == "/game/ongeki/version.change":
                ongeki_version=request.args[b"version"][0].decode()
                if(ongeki_version.isdigit()):
                    usr_sesh.ongeki_version=int(ongeki_version)
                return redirectTo(b"/game/ongeki/", request)
            
            else:
                return b"Something went wrong"
        else:
            return b"User is not logged in"
