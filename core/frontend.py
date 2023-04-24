import logging, coloredlogs
from typing import Any, Dict, List
from twisted.web import resource
from twisted.web.util import redirectTo
from twisted.web.http import Request
from logging.handlers import TimedRotatingFileHandler
from twisted.web.server import Session
from zope.interface import Interface, Attribute, implementer
from twisted.python.components import registerAdapter
import jinja2
import bcrypt

from core import CoreConfig, Utils
from core.data import Data


class IUserSession(Interface):
    userId = Attribute("User's ID")
    current_ip = Attribute("User's current ip address")
    permissions = Attribute("User's permission level")


@implementer(IUserSession)
class UserSession(object):
    def __init__(self, session):
        self.userId = 0
        self.current_ip = "0.0.0.0"
        self.permissions = 0


class FrontendServlet(resource.Resource):
    def getChild(self, name: bytes, request: Request):
        self.logger.debug(f"{Utils.get_ip_addr(request)} -> {name.decode()}")
        if name == b"":
            return self
        return resource.Resource.getChild(self, name, request)

    def __init__(self, cfg: CoreConfig, config_dir: str) -> None:
        self.config = cfg
        log_fmt_str = "[%(asctime)s] Frontend | %(levelname)s | %(message)s"
        log_fmt = logging.Formatter(log_fmt_str)
        self.logger = logging.getLogger("frontend")
        self.environment = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
        self.game_list: List[Dict[str, str]] = []
        self.children: Dict[str, Any] = {}

        fileHandler = TimedRotatingFileHandler(
            "{0}/{1}.log".format(self.config.server.log_dir, "frontend"),
            when="d",
            backupCount=10,
        )
        fileHandler.setFormatter(log_fmt)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_fmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)

        self.logger.setLevel(cfg.frontend.loglevel)
        coloredlogs.install(
            level=cfg.frontend.loglevel, logger=self.logger, fmt=log_fmt_str
        )
        registerAdapter(UserSession, Session, IUserSession)

        fe_game = FE_Game(cfg, self.environment)
        games = Utils.get_all_titles()
        for game_dir, game_mod in games.items():
            if hasattr(game_mod, "frontend"):
                try:
                    game_fe = game_mod.frontend(cfg, self.environment, config_dir)
                    self.game_list.append({"url": game_dir, "name": game_fe.nav_name})
                    fe_game.putChild(game_dir.encode(), game_fe)

                except Exception as e:
                    self.logger.error(
                        f"Failed to import frontend from {game_dir} because {e}"
                    )

        self.environment.globals["game_list"] = self.game_list
        self.putChild(b"gate", FE_Gate(cfg, self.environment))
        self.putChild(b"user", FE_User(cfg, self.environment))
        self.putChild(b"game", fe_game)

        self.logger.info(
            f"Ready on port {self.config.frontend.port} serving {len(fe_game.children)} games"
        )

    def render_GET(self, request):
        self.logger.debug(f"{Utils.get_ip_addr(request)} -> {request.uri.decode()}")
        template = self.environment.get_template("core/frontend/index.jinja")
        return template.render(
            server_name=self.config.server.name,
            title=self.config.server.name,
            game_list=self.game_list,
            sesh=vars(IUserSession(request.getSession())),
        ).encode("utf-16")


class FE_Base(resource.Resource):
    """
    A Generic skeleton class that all frontend handlers should inherit from
    Initializes the environment, data, logger, config, and sets isLeaf to true
    It is expected that game implementations of this class overwrite many of these
    """

    isLeaf = True

    def __init__(self, cfg: CoreConfig, environment: jinja2.Environment) -> None:
        self.core_config = cfg
        self.data = Data(cfg)
        self.logger = logging.getLogger("frontend")
        self.environment = environment
        self.nav_name = "nav_name"


class FE_Gate(FE_Base):
    def render_GET(self, request: Request):
        self.logger.debug(f"{Utils.get_ip_addr(request)} -> {request.uri.decode()}")
        uri: str = request.uri.decode()

        sesh = request.getSession()
        usr_sesh = IUserSession(sesh)
        if usr_sesh.userId > 0:
            return redirectTo(b"/user", request)

        if uri.startswith("/gate/create"):
            return self.create_user(request)

        if b"e" in request.args:
            try:
                err = int(request.args[b"e"][0].decode())
            except:
                err = 0

        else:
            err = 0

        template = self.environment.get_template("core/frontend/gate/gate.jinja")
        return template.render(
            title=f"{self.core_config.server.name} | Login Gate",
            error=err,
            sesh=vars(usr_sesh),
        ).encode("utf-16")

    def render_POST(self, request: Request):
        uri = request.uri.decode()
        ip = Utils.get_ip_addr(request)

        if uri == "/gate/gate.login":
            access_code: str = request.args[b"access_code"][0].decode()
            passwd: bytes = request.args[b"passwd"][0]
            if passwd == b"":
                passwd = None

            uid = self.data.card.get_user_id_from_card(access_code)
            if uid is None:
                return redirectTo(b"/gate?e=1", request)

            if passwd is None:
                sesh = self.data.user.check_password(uid)

                if sesh is not None:
                    return redirectTo(
                        f"/gate/create?ac={access_code}".encode(), request
                    )
                return redirectTo(b"/gate?e=1", request)

            if not self.data.user.check_password(uid, passwd):
                return redirectTo(b"/gate?e=1", request)

            self.logger.info(f"Successful login of user {uid} at {ip}")

            sesh = request.getSession()
            usr_sesh = IUserSession(sesh)
            usr_sesh.userId = uid
            usr_sesh.current_ip = ip

            return redirectTo(b"/user", request)

        elif uri == "/gate/gate.create":
            access_code: str = request.args[b"access_code"][0].decode()
            username: str = request.args[b"username"][0]
            email: str = request.args[b"email"][0].decode()
            passwd: str = request.args[b"passwd"][0]

            uid = self.data.card.get_user_id_from_card(access_code)
            if uid is None:
                return redirectTo(b"/gate?e=1", request)

            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(passwd, salt)

            result = self.data.user.create_user(
                uid, username, email, hashed.decode(), 1
            )
            if result is None:
                return redirectTo(b"/gate?e=3", request)

            if not self.data.user.check_password(uid, passwd.encode()):
                return redirectTo(b"/gate", request)

            return redirectTo(b"/user", request)

        else:
            return b""

    def create_user(self, request: Request):
        if b"ac" not in request.args or len(request.args[b"ac"][0].decode()) != 20:
            return redirectTo(b"/gate?e=2", request)

        ac = request.args[b"ac"][0].decode()

        template = self.environment.get_template("core/frontend/gate/create.jinja")
        return template.render(
            title=f"{self.core_config.server.name} | Create User",
            code=ac,
            sesh={"userId": 0},
        ).encode("utf-16")


class FE_User(FE_Base):
    def render_GET(self, request: Request):
        template = self.environment.get_template("core/frontend/user/index.jinja")

        sesh: Session = request.getSession()
        usr_sesh = IUserSession(sesh)
        if usr_sesh.userId == 0:
            return redirectTo(b"/gate", request)

        return template.render(
            title=f"{self.core_config.server.name} | Account", sesh=vars(usr_sesh)
        ).encode("utf-16")


class FE_Game(FE_Base):
    isLeaf = False
    children: Dict[str, Any] = {}

    def getChild(self, name: bytes, request: Request):
        if name == b"":
            return self
        return resource.Resource.getChild(self, name, request)

    def render_GET(self, request: Request) -> bytes:
        return redirectTo(b"/user", request)
