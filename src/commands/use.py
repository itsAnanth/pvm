import os
import logging
from argparse import _SubParsersAction, ArgumentParser

from src.scripts.store import Store
from src.scripts.shims import generate_shims

logger = logging.getLogger("pvm.use")

def handle_use(args):
    
    old_index, old_version = Store.get_version(lambda v: v.get("using") is True)
    
    if old_version:
        old_version['using'] = False

        Store.set_version(old_version)
    
    index, version = Store.get_version(lambda v: v["version"] == args.version)

    if not version:
        logger.error(f"Version {args.version} is not installed. Use 'pvm list --all' to see available versions.")
        return
    

    logger.debug(version)

    if generate_shims(version):
        version['using'] = True
        Store.set_version(version)
        print(f"Using Python {args.version}")





def use_command(sub_parser: _SubParsersAction[ArgumentParser]):

    parser = sub_parser.add_parser(
        'use',
        help='Use a specific version of Python which is installed.'
    )

    parser.add_argument(
        'version',
        help='Python version to use',
    )



    parser.set_defaults(func=handle_use)

    