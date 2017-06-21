import subprocess as sp
from pathlib import Path
from sys import stdout, stderr
from functools import partial


def main():
    """Use yarn to install the pug-cli"""
    package_base_dir = Path(__file__).parent.parent
    uninstallation_cmd = ('yarn', 'remove', 'pug-cli')
    installation_cmd = ('yarn', 'install', 'pug-cli')

    run = partial(sp.Popen,
                  stdout=stdout,
                  stderr=stderr,
                  cwd=str(package_base_dir.absolute()))

    run(uninstallation_cmd)
    run(installation_cmd)
