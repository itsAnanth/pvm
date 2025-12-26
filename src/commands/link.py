import os
import subprocess
import logging
from argparse import _SubParsersAction, ArgumentParser

from src.scripts.store import Store
from src.scripts.arch import detect_arch, is_windows

logger = logging.getLogger("pvm.link")

def handle_link(args):
    install_dir = args.dir

    pythonexe = os.path.join(install_dir, 'python.exe')

    if not os.path.isfile(pythonexe):
        logger.error(f"No python.exe found in {install_dir}. Make sure this is a valid Python installation.")
        return
    
    result = subprocess.run(
        [pythonexe, "--version"],
        capture_output=True,
        text=True,
        check=True,
    )

    # Output is usually on stderr for --version, handle it properly :p
    version_output = result.stdout.strip() or result.stderr.strip()
    version = version_output.split(' ')[1]

    version_data = {
        'version': version,
        'dir': install_dir,
        'using': False,
    }  

    Store.set_version(version_data)
    logger.info(f"Linked Python {version} from {install_dir}.")
    


def link_command(sub_parser: _SubParsersAction[ArgumentParser]):

    parser = sub_parser.add_parser(
        'link',
        help='Link an existing Python installation to pvm'
    )

    parser.add_argument(
        'dir',
        help='Installation directory',
    )

    parser.set_defaults(func=handle_link)

    