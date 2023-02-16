#!/usr/bin/env python3
import argparse
import yaml
from os import path, mkdir, access, W_OK
from core import *

from twisted.web import server
from twisted.internet import reactor, endpoints

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ARTEMiS main entry point")
    parser.add_argument("--config", "-c", type=str, default="config", help="Configuration folder")
    args = parser.parse_args()

    if not path.exists(f"{args.config}/core.yaml"):
        print(f"The config folder you specified ({args.config}) does not exist or does not contain core.yaml.\nDid you copy the example folder?")
        exit(1)

    cfg: CoreConfig = CoreConfig()
    cfg.update(yaml.safe_load(open(f"{args.config}/core.yaml")))

    if not path.exists(cfg.server.log_dir):
        mkdir(cfg.server.log_dir)
    
    if not access(cfg.server.log_dir, W_OK):
        print(f"Log directory {cfg.server.log_dir} NOT writable, please check permissions")
        exit(1)

    if cfg.aimedb.key == "":
        print("!!AIMEDB KEY BLANK, SET KEY IN CORE.YAML!!")
        exit(1)
    
    print(f"ARTEMiS starting in {'develop' if cfg.server.is_develop else 'production'} mode")

    allnet_server_str = f"tcp:{cfg.allnet.port}:interface={cfg.server.listen_address}"    
    title_server_str = f"tcp:{cfg.billing.port}:interface={cfg.server.listen_address}"
    adb_server_str = f"tcp:{cfg.aimedb.port}:interface={cfg.server.listen_address}"

    billing_server_str = f"tcp:{cfg.billing.port}:interface={cfg.server.listen_address}"
    if cfg.server.is_develop:
        billing_server_str = f"ssl:{cfg.billing.port}:interface={cfg.server.listen_address}"\
            f":privateKey={cfg.billing.ssl_key}:certKey={cfg.billing.ssl_cert}"
    
    endpoints.serverFromString(reactor, allnet_server_str).listen(server.Site(AllnetServlet(cfg, args.config)))
    endpoints.serverFromString(reactor, adb_server_str).listen(AimedbFactory(cfg))

    if cfg.billing.port > 0:
        endpoints.serverFromString(reactor, billing_server_str).listen(server.Site(BillingServlet(cfg)))
    
    if cfg.title.port > 0:        
        endpoints.serverFromString(reactor, title_server_str).listen(server.Site(TitleServlet(cfg, args.config)))
    
    reactor.run() # type: ignore