import yaml
import argparse
from core.config import CoreConfig
from core.data import Data
from os import path, mkdir, access, W_OK

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database utilities")
    parser.add_argument(
        "--config", "-c", type=str, help="Config folder to use", default="config"
    )
    parser.add_argument(
        "--version",
        "-v",
        type=str,
        help="Version of the database to upgrade/rollback to",
    )
    parser.add_argument(
        "--game",
        "-g",
        type=str,
        help="Game code of the game who's schema will be updated/rolled back. Ex. SDFE",
    )
    parser.add_argument("--email", "-e", type=str, help="Email for the new user")
    parser.add_argument("--old_ac", "-o", type=str, help="Access code to transfer from")
    parser.add_argument("--new_ac", "-n", type=str, help="Access code to transfer to")
    parser.add_argument("--force", "-f", type=bool, help="Force the action to happen")
    parser.add_argument(
        "action", type=str, help="DB Action, create, recreate, upgrade, or rollback"
    )
    args = parser.parse_args()

    cfg = CoreConfig()
    if path.exists(f"{args.config}/core.yaml"):
        cfg.update(yaml.safe_load(open(f"{args.config}/core.yaml")))
    
    if not path.exists(cfg.server.log_dir):
        mkdir(cfg.server.log_dir)
    
    if not access(cfg.server.log_dir, W_OK):
        print(
            f"Log directory {cfg.server.log_dir} NOT writable, please check permissions"
        )
        exit(1)

    data = Data(cfg)
    

    if args.action == "create":
        data.create_database()

    elif args.action == "recreate":
        data.recreate_database()

    elif args.action == "upgrade" or args.action == "rollback":
        if args.version is None:
            data.logger.error("Must set game and version to migrate to")
            exit(0)

        if args.game is None:
            data.logger.info("No game set, upgrading core schema")
            data.migrate_database("CORE", int(args.version), args.action)

        else:
            data.migrate_database(args.game, int(args.version), args.action)

    elif args.action == "create-owner":
        data.create_owner(args.email)

    elif args.action == "migrate-card":
        data.migrate_card(args.old_ac, args.new_ac, args.force)

    elif args.action == "cleanup":
        data.delete_hanging_users()

    data.logger.info("Done")
