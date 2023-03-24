# vim: set fileencoding=utf-8
import argparse
import re
import os
import yaml
from os import path
import logging
import coloredlogs

from logging.handlers import TimedRotatingFileHandler
from typing import List, Optional

from core import CoreConfig, Utils


class BaseReader:
    def __init__(
        self,
        config: CoreConfig,
        version: int,
        bin_dir: Optional[str],
        opt_dir: Optional[str],
        extra: Optional[str],
    ) -> None:
        self.logger = logging.getLogger("reader")
        self.config = config
        self.bin_dir = bin_dir
        self.opt_dir = opt_dir
        self.version = version
        self.extra = extra

    def get_data_directories(self, directory: str) -> List[str]:
        ret: List[str] = []

        for root, dirs, files in os.walk(directory):
            for dir in dirs:
                if re.fullmatch("[A-Z0-9]{4,4}", dir) is not None:
                    ret.append(f"{root}/{dir}")

        return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import Game Information")
    parser.add_argument(
        "--series",
        action="store",
        type=str,
        required=True,
        help="The game series we are importing.",
    )
    parser.add_argument(
        "--version",
        dest="version",
        action="store",
        type=int,
        required=True,
        help="The game version we are importing.",
    )
    parser.add_argument(
        "--binfolder",
        dest="bin",
        action="store",
        type=str,
        help="Folder containing A000 base data",
    )
    parser.add_argument(
        "--optfolder",
        dest="opt",
        action="store",
        type=str,
        help="Folder containing Option data folders",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config",
        help="Folder containing the core configuration for importing to DB. Defaults to 'config'.",
    )
    parser.add_argument(
        "--extra",
        type=str,
        help="Any extra data that a reader might require.",
    )

    # Parse args, validate invariants.
    args = parser.parse_args()

    config = CoreConfig()
    if path.exists(f"{args.config}/core.yaml"):
        config.update(yaml.safe_load(open(f"{args.config}/core.yaml")))

    log_fmt_str = "[%(asctime)s] Reader | %(levelname)s | %(message)s"
    log_fmt = logging.Formatter(log_fmt_str)
    logger = logging.getLogger("reader")

    fileHandler = TimedRotatingFileHandler(
        "{0}/{1}.log".format(config.server.log_dir, "reader"), when="d", backupCount=10
    )
    fileHandler.setFormatter(log_fmt)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(log_fmt)

    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    log_lv = logging.DEBUG if config.server.is_develop else logging.INFO
    logger.setLevel(log_lv)
    coloredlogs.install(level=log_lv, logger=logger, fmt=log_fmt_str)

    if args.series is None or args.version is None:
        logger.error("Game or version not specified")
        parser.print_help()
        exit(1)

    if args.bin is None and args.opt is None:
        logger.error("Must specify either bin or opt directory")
        parser.print_help()
        exit(1)

    if args.bin is not None and (args.bin.endswith("\\") or args.bin.endswith("/")):
        bin_arg = args.bin[:-1]
    else:
        bin_arg = args.bin

    if args.opt is not None and (args.opt.endswith("\\") or args.opt.endswith("/")):
        opt_arg = args.opt[:-1]
    else:
        opt_arg = args.opt

    logger.info("Starting importer...")

    titles = Utils.get_all_titles()

    for dir, mod in titles.items():
        if args.series in mod.game_codes:
            handler = mod.reader(config, args.version,
                                 bin_arg, opt_arg, args.extra)
            handler.read()

    logger.info("Done")
