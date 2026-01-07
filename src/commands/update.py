import os
import urllib.request
import json
import logging
from argparse import _SubParsersAction, ArgumentParser

from src.utils.version import get_pvm_version

logger = logging.getLogger("pvm.update")

def get_latest_release_url(repo_owner, repo_name, asset_name):
    """Fetch the latest release download URL from GitHub API."""
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            
        # Find the asset with the matching name
        for asset in data.get('assets', []):
            if asset['name'] == asset_name:
                return asset['browser_download_url'], data['tag_name']
        
        raise ValueError(f"Asset '{asset_name}' not found in latest release")
    
    except Exception as e:
        logger.error(f"Failed to fetch latest release info: {e}")
        raise

def handle_update(args):
    
    if not os.getenv('LOCALAPPDATA'):
        logger.error("LOCALAPPDATA environment variable not set. Cannot proceed with update.")
        return
    
    install_dir = os.path.join(os.getenv('LOCALAPPDATA'), '.pvm')
    exe_path = os.path.join(install_dir, 'pvm.exe')
    
    try:
        # Get latest release URL from GitHub API
        logger.info("Fetching latest release information...")
        url, version = get_latest_release_url('itsAnanth', 'pvm', 'pvm.exe')

        if version == get_pvm_version():
            print(f"You are already using the latest version of PVM. {version}")
            return
        
        logger.info(f"Latest version: {version}")
        logger.info(f"Download URL: {url}")

        
        # Create directory if it doesn't exist
        os.makedirs(install_dir, exist_ok=True)
        logger.info(f"pvm directory: {install_dir}")
        
        # Check if file exists for update
        logger.info("Updating existing PVM installation..." if os.path.exists(exe_path) else "No existing installation found, downloading fresh copy...")
        
        # Download the file
        logger.info(f"Downloading pvm.exe from {url}...")
        urllib.request.urlretrieve(url, exe_path)
        
        print(f"\nUpdate complete! PVM {version} installed at: {exe_path}")
        
    except urllib.error.URLError as e:
        logger.error(f"Failed to download: {e}")
        print(f"Update failed")
        return
    except Exception as e:
        logger.error(f"Failed to run update: {e}")
        print(f"Update failed")
        return

def update_command(sub_parser: _SubParsersAction[ArgumentParser]):

    parser = sub_parser.add_parser(
        'update',
        help='Update pvm to latest version'
    )

    parser.set_defaults(func=handle_update)

    