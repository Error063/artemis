#!/usr/bin/env python3
import argparse
import yaml
from os import path, environ
import uvicorn
import logging
import asyncio

from core import CoreConfig, AimedbServlette

async def launch_main(cfg: CoreConfig, ssl: bool) -> None:
    if ssl:
        server_cfg = uvicorn.Config(
            "core.app:app", 
            host=cfg.server.listen_address, 
            port=cfg.server.port if args.port == 0 else args.port, 
            reload=cfg.server.is_develop,
            log_level="info" if cfg.server.is_develop else "critical",
            ssl_version=3,
            ssl_certfile=cfg.server.ssl_cert,
            ssl_keyfile=cfg.server.ssl_key
        ) 
    else:
        server_cfg = uvicorn.Config(
            "core.app:app", 
            host=cfg.server.listen_address, 
            port=cfg.server.port if args.port == 0 else args.port, 
            reload=cfg.server.is_develop,
            log_level="info" if cfg.server.is_develop else "critical"
        )
    server = uvicorn.Server(server_cfg)
    await server.serve()

async def launch_billing(cfg: CoreConfig) -> None:
    server_cfg = uvicorn.Config(
        "core.allnet:app_billing", 
        host=cfg.server.listen_address, 
        port=cfg.billing.port, 
        reload=cfg.server.is_develop,
        log_level="info" if cfg.server.is_develop else "critical",
        ssl_version=3,
        ssl_certfile=cfg.billing.ssl_cert,
        ssl_keyfile=cfg.billing.ssl_key
    )
    server = uvicorn.Server(server_cfg)
    await server.serve()

async def launch_frontend(cfg: CoreConfig) -> None:
    server_cfg = uvicorn.Config(
        "core.frontend:app", 
        host=cfg.server.listen_address, 
        port=cfg.frontend.port, 
        reload=cfg.server.is_develop,
        log_level="info" if cfg.server.is_develop else "critical",
    )
    server = uvicorn.Server(server_cfg)
    await server.serve()

async def launch_allnet(cfg: CoreConfig) -> None:
    server_cfg = uvicorn.Config(
        "core.allnet:app_allnet", 
        host=cfg.server.listen_address, 
        port=cfg.allnet.port, 
        reload=cfg.server.is_develop,
        log_level="info" if cfg.server.is_develop else "critical",
    )
    server = uvicorn.Server(server_cfg)
    await server.serve()


async def launcher(cfg: CoreConfig, ssl: bool) -> None:
    task_list = [asyncio.create_task(launch_main(cfg, ssl))]
    
    if cfg.billing.standalone:
        task_list.append(asyncio.create_task(launch_billing(cfg)))
    if cfg.frontend.enable:
        task_list.append(asyncio.create_task(launch_frontend(cfg)))
    if cfg.allnet.standalone:
        task_list.append(asyncio.create_task(launch_allnet(cfg)))
    if cfg.aimedb.enable:
        AimedbServlette(cfg).start()
    
    done, pending = await asyncio.wait(
        task_list,
        return_when=asyncio.FIRST_COMPLETED,
    )
    
    logging.getLogger("core").info("Shutdown")
    for pending_task in pending:
        pending_task.cancel("Another service died, server is shutting down")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Artemis main entry point")
    parser.add_argument(
        "--config", "-c", type=str, default="config", help="Configuration folder"
    )
    parser.add_argument(
        "--port", "-p", type=int, default=0, help="Port override"
    )
    parser.add_argument(
        "--ssl", "-s", type=bool, help="Launch with SSL"
    )
    args = parser.parse_args()

    if not path.exists(f"{args.config}/core.yaml"):
        print(
            f"The config folder you specified ({args.config}) does not exist or does not contain core.yaml. Defaults will be used.\nDid you copy the example folder?"
        )
    
    cfg: CoreConfig = CoreConfig()
    if path.exists(f"{args.config}/core.yaml"):
        cfg.update(yaml.safe_load(open(f"{args.config}/core.yaml")))

    environ["ARTEMIS_CFG_DIR"] = args.config

    asyncio.run(launcher(cfg, args.ssl))
