import os
import logging

PVM_ROOT = os.path.join(os.environ['LOCALAPPDATA'], '.pvm')


logger = logging.getLogger("pvm.shims")

def generate_shims(version):

    logger.debug(f"Generating shims for version: {version['version']}")

    if not version['dir']:
        logger.error(f"Version {version['version']} has no installation directory set.")
        return False
    

    shimsdir = os.path.join(PVM_ROOT, "shims")

    python_exe = os.path.join(os.path.abspath(version['dir']), 'python.exe')

    # Create python.cmd shim
    python_shim = os.path.join(shimsdir, 'python.cmd')
    with open(python_shim, 'w') as f:
        f.write(f'@echo off\n')
        f.write(f'"{python_exe}" %*\n')



    # Create pip.cmd shim
    pip_shim = os.path.join(shimsdir, 'pip.cmd')
    with open(pip_shim, 'w') as f:
        f.write(f'@echo off\n')
        f.write(f'"{python_exe}" -m pip %*\n')

    return True