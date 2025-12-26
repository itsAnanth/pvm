import os
import logging
from argparse import _SubParsersAction, ArgumentParser

from src.utils.functions import validate_version_format
from src.scripts.store import Store

logger = logging.getLogger("pvm.uninstall")


def handle_uninstall(args):
    
    version = args.version
    
    # Validate version format
    if not validate_version_format(version):
        logger.error(f"Invalid version format: {version}. Expected format: X.Y.Z (e.g., 3.11.0)")
        return
    
    index, installed_version = Store.get_version(lambda v: v["version"] == version)
    if not installed_version:
        logger.error(f"Version {version} is not installed.")
        return
    
    install_dir = installed_version['dir']
    if os.path.isdir(install_dir):
        if str(input(f"[WARNING] Are you sure you want to uninstall Python {version} from {install_dir}? (y/n): ")).lower() not in ['y', 'yes']:
            logger.info("Uninstallation cancelled by user.")
            return
        
        try:
            # Remove the installation directory
            import shutil
            shutil.rmtree(install_dir)
            logger.info(f"Successfully uninstalled Python {version} from {install_dir}.")
            
            # Remove from store
            Store.remove_version(version)
        
        except Exception as e:
            logger.error(f"Failed to uninstall: {e}")
            return
    else:
        logger.error(f"Installation directory {install_dir} does not exist. cleaning up store entry.")
        Store.remove_version(version)
    


def uninstall_command(sub_parser: _SubParsersAction[ArgumentParser]):

    parser = sub_parser.add_parser(
        'uninstall',
        help='Uninstall a specific Python version'
    )

    parser.add_argument(
        'version',
        help='Python version to uninstall (e.g., 3.11.0)',
    )



    parser.set_defaults(func=handle_uninstall)

    