#!/usr/bin/env python3
import argparse
import logging, coloredlogs
from logging.handlers import TimedRotatingFileHandler
from typing import Dict
import yaml
from os import path, mkdir, access, W_OK
from core import *

from twisted.web import server, resource
from twisted.internet import reactor, endpoints
from twisted.web.http import Request
from routes import Mapper


class HttpDispatcher(resource.Resource):
    def __init__(self, cfg: CoreConfig, config_dir: str):
        super().__init__()
        self.config = cfg
        self.isLeaf = True
        self.map_get = Mapper()
        self.map_post = Mapper()
        self.logger = logging.getLogger("core")

        self.allnet = AllnetServlet(cfg, config_dir)
        self.title = TitleServlet(cfg, config_dir)
        self.mucha = MuchaServlet(cfg, config_dir)

        self.map_get.connect(
            "allnet_downloadorder_ini",
            "/dl/ini/{file}",
            controller="allnet",
            action="handle_dlorder_ini",
            conditions=dict(method=["GET"]),
        )

        self.map_post.connect(
            "allnet_downloadorder_report",
            "/dl/report",
            controller="allnet",
            action="handle_dlorder_report",
            conditions=dict(method=["POST"]),
        )

        self.map_get.connect(
            "allnet_ping",
            "/naomitest.html",
            controller="allnet",
            action="handle_naomitest",
            conditions=dict(method=["GET"]),
        )
        self.map_post.connect(
            "allnet_poweron",
            "/sys/servlet/PowerOn",
            controller="allnet",
            action="handle_poweron",
            conditions=dict(method=["POST"]),
        )
        self.map_post.connect(
            "allnet_downloadorder",
            "/sys/servlet/DownloadOrder",
            controller="allnet",
            action="handle_dlorder",
            conditions=dict(method=["POST"]),
        )
        self.map_post.connect(
            "allnet_loaderstaterecorder",
            "/sys/servlet/LoaderStateRecorder",
            controller="allnet",
            action="handle_loaderstaterecorder",
            conditions=dict(method=["POST"]),
        )
        self.map_post.connect(
            "allnet_alive",
            "/sys/servlet/Alive",
            controller="allnet",
            action="handle_alive",
            conditions=dict(method=["POST"]),
        )
        self.map_get.connect(
            "allnet_alive",
            "/sys/servlet/Alive",
            controller="allnet",
            action="handle_alive",
            conditions=dict(method=["GET"]),
        )
        self.map_post.connect(
            "allnet_billing",
            "/request",
            controller="allnet",
            action="handle_billing_request",
            conditions=dict(method=["POST"]),
        )
        self.map_post.connect(
            "allnet_billing",
            "/request/",
            controller="allnet",
            action="handle_billing_request",
            conditions=dict(method=["POST"]),
        )

        self.map_post.connect(
            "mucha_boardauth",
            "/mucha/boardauth.do",
            controller="mucha",
            action="handle_boardauth",
            conditions=dict(method=["POST"]),
        )
        self.map_post.connect(
            "mucha_updatacheck",
            "/mucha/updatacheck.do",
            controller="mucha",
            action="handle_updatecheck",
            conditions=dict(method=["POST"]),
        )

        self.map_get.connect(
            "title_get",
            "/{game}/{version}/{endpoint:.*?}",
            controller="title",
            action="render_GET",
            conditions=dict(method=["GET"]),
            requirements=dict(game=R"S..."),
        )
        self.map_post.connect(
            "title_post",
            "/{game}/{version}/{endpoint:.*?}",
            controller="title",
            action="render_POST",
            conditions=dict(method=["POST"]),
            requirements=dict(game=R"S..."),
        )

    def render_GET(self, request: Request) -> bytes:
        self.logger.debug(request.uri)
        test = self.map_get.match(request.uri.decode())
        client_ip = Utils.get_ip_addr(request)

        if test is None:
            self.logger.debug(
                f"Unknown GET endpoint {request.uri.decode()} from {client_ip} to port {request.getHost().port}"
            )
            request.setResponseCode(404)
            return b"Endpoint not found."

        return self.dispatch(test, request)

    def render_POST(self, request: Request) -> bytes:
        test = self.map_post.match(request.uri.decode())
        client_ip = Utils.get_ip_addr(request)

        if test is None:
            self.logger.debug(
                f"Unknown POST endpoint {request.uri.decode()} from {client_ip} to port {request.getHost().port}"
            )
            request.setResponseCode(404)
            return b"Endpoint not found."

        return self.dispatch(test, request)

    def dispatch(self, matcher: Dict, request: Request) -> bytes:
        controller = getattr(self, matcher["controller"], None)
        if controller is None:
            self.logger.error(
                f"Controller {matcher['controller']} not found via endpoint {request.uri.decode()}"
            )
            request.setResponseCode(404)
            return b"Endpoint not found."

        handler = getattr(controller, matcher["action"], None)
        if handler is None:
            self.logger.error(
                f"Action {matcher['action']} not found in controller {matcher['controller']} via endpoint {request.uri.decode()}"
            )
            request.setResponseCode(404)
            return b"Endpoint not found."

        url_vars = matcher
        url_vars.pop("controller")
        url_vars.pop("action")
        ret = handler(request, url_vars)

        if type(ret) == str:
            return ret.encode()
        elif type(ret) == bytes:
            return ret
        else:
            return b""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ARTEMiS main entry point")
    parser.add_argument(
        "--config", "-c", type=str, default="config", help="Configuration folder"
    )
    args = parser.parse_args()

    if not path.exists(f"{args.config}/core.yaml"):
        print(
            f"The config folder you specified ({args.config}) does not exist or does not contain core.yaml.\nDid you copy the example folder?"
        )
        exit(1)

    cfg: CoreConfig = CoreConfig()
    if path.exists(f"{args.config}/core.yaml"):
        cfg.update(yaml.safe_load(open(f"{args.config}/core.yaml")))

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

    if not cfg.aimedb.key:
        logger.error("!!AIMEDB KEY BLANK, SET KEY IN CORE.YAML!!")
        exit(1)

    logger.info(
        f"ARTEMiS starting in {'develop' if cfg.server.is_develop else 'production'} mode"
    )

    allnet_server_str = f"tcp:{cfg.allnet.port}:interface={cfg.server.listen_address}"
    title_server_str = f"tcp:{cfg.title.port}:interface={cfg.server.listen_address}"
    adb_server_str = f"tcp:{cfg.aimedb.port}:interface={cfg.server.listen_address}"
    frontend_server_str = (
        f"tcp:{cfg.frontend.port}:interface={cfg.server.listen_address}"
    )

    billing_server_str = f"tcp:{cfg.billing.port}:interface={cfg.server.listen_address}"
    if cfg.server.is_develop:
        billing_server_str = (
            f"ssl:{cfg.billing.port}:interface={cfg.server.listen_address}"
            f":privateKey={cfg.billing.ssl_key}:certKey={cfg.billing.ssl_cert}"
        )

    dispatcher = HttpDispatcher(cfg, args.config)

    endpoints.serverFromString(reactor, allnet_server_str).listen(
        server.Site(dispatcher)
    )
    endpoints.serverFromString(reactor, adb_server_str).listen(AimedbFactory(cfg))

    if cfg.frontend.enable:
        endpoints.serverFromString(reactor, frontend_server_str).listen(
            server.Site(FrontendServlet(cfg, args.config))
        )

    if cfg.billing.port > 0:
        endpoints.serverFromString(reactor, billing_server_str).listen(
            server.Site(dispatcher)
        )

    if cfg.title.port > 0:
        endpoints.serverFromString(reactor, title_server_str).listen(
            server.Site(dispatcher)
        )

    reactor.run()  # type: ignore
