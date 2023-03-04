import yaml
import argparse
from core.config import CoreConfig
from core.data import Data

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Database utilities")
    parser.add_argument("--config", "-c", type=str, help="Config folder to use", default="config")
    parser.add_argument("--version", "-v", type=str, help="Version of the database to upgrade/rollback to")
    parser.add_argument("--game", "-g", type=str, help="Game code of the game who's schema will be updated/rolled back. Ex. SDFE")
    parser.add_argument("action", type=str, help="DB Action, create, recreate, upgrade, or rollback")
    args = parser.parse_args()

    cfg = CoreConfig()
    cfg.update(yaml.safe_load(open(f"{args.config}/core.yaml")))
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

    data.logger.info("Done")
