import yaml
import logging
import coloredlogs
from logging.handlers import TimedRotatingFileHandler
from starlette.routing import Route
from starlette.requests import Request
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from os import environ, path, mkdir, W_OK, access
from typing import List

from core import CoreConfig, TitleServlet, MuchaServlet, AllnetServlet, BillingServlet, AimedbServlet
from core.chimedb import ChimeServlet
from core.frontend import FrontendServlet

async def dummy_rt(request: Request):
    return PlainTextResponse("Service OK")

cfg_dir = environ.get("ARTEMIS_CFG_DIR", "config")
cfg: CoreConfig = CoreConfig()
if path.exists(f"{cfg_dir}/core.yaml"):
    cfg.update(yaml.safe_load(open(f"{cfg_dir}/core.yaml")))

if not path.exists(cfg.server.log_dir):
    mkdir(cfg.server.log_dir)

if not access(cfg.server.log_dir, W_OK):
    print(
        f"Log directory {cfg.server.log_dir} NOT writable, please check permissions"
    )
    exit(1)

logger = logging.getLogger("core")
log_fmt_str = "[%(asctime)s] Core | %(levelname)s | %(message)s"
log_fmt = logging.Formatter(log_fmt_str)

fileHandler = TimedRotatingFileHandler(
    "{0}/{1}.log".format(cfg.server.log_dir, "core"), when="d", backupCount=10
)
fileHandler.setFormatter(log_fmt)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(log_fmt)

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

log_lv = logging.DEBUG if cfg.server.is_develop else logging.INFO
logger.setLevel(log_lv)
coloredlogs.install(level=log_lv, logger=logger, fmt=log_fmt_str)

logger.info(f"Artemis starting in {'develop' if cfg.server.is_develop else 'production'} mode")

title = TitleServlet(cfg, cfg_dir) # This has to be loaded first to load plugins
mucha = MuchaServlet(cfg, cfg_dir)

route_lst: List[Route] = [
    # Mucha
    Route("/mucha_front/boardauth.do", mucha.handle_boardauth, methods=["POST"]),
    Route("/mucha_front/updatacheck.do", mucha.handle_updatecheck, methods=["POST"]),
    Route("/mucha_front/downloadstate.do", mucha.handle_dlstate, methods=["POST"]),
    # General
    Route("/", dummy_rt),
    Route("/robots.txt", FrontendServlet.robots)
]

if not cfg.billing.standalone:
    billing = BillingServlet(cfg, cfg_dir)
    route_lst += [
        Route("/request", billing.handle_billing_request, methods=["POST"]),
        Route("/request/", billing.handle_billing_request, methods=["POST"]),
    ]

if not cfg.allnet.standalone:
    allnet = AllnetServlet(cfg, cfg_dir)
    route_lst += [
        Route("/sys/servlet/PowerOn", allnet.handle_poweron, methods=["GET", "POST"]),
        Route("/sys/servlet/DownloadOrder", allnet.handle_dlorder, methods=["GET", "POST"]),
        Route("/sys/servlet/LoaderStateRecorder", allnet.handle_loaderstaterecorder, methods=["GET", "POST"]),
        Route("/sys/servlet/Alive", allnet.handle_alive, methods=["GET", "POST"]),
        Route("/naomitest.html", allnet.handle_naomitest),
    ]
    
    if cfg.allnet.allow_online_updates:
        route_lst += [
            Route("/report-api/Report", allnet.handle_dlorder_report, methods=["POST"]),
            Route("/dl/ini/{file:str}", allnet.handle_dlorder_ini),
        ]

if cfg.chimedb.enable:
    chimedb = ChimeServlet(cfg, cfg_dir)
    route_lst += [
        Route("/wc_aime/api/alive_check", chimedb.handle_qr_alive, methods=["POST"]),
        Route("/qrcode/api/alive_check", chimedb.handle_qr_alive, methods=["POST"]),
        Route("/wc_aime/api/get_data", chimedb.handle_qr_lookup, methods=["POST"])
    ]


for code, game in title.title_registry.items():
    route_lst += game.get_routes()

app = Starlette(cfg.server.is_develop, route_lst)
