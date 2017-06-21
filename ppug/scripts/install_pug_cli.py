import subprocess as sp
import sys
from functools import partial
from pathlib import Path


def main():
    """Use yarn to install the pug-cli"""
    package_base_dir = Path(__file__).parent.parent
    uninstallation_cmd = ('yarn', 'remove', 'pug-cli')
    installation_cmd = ('yarn', 'add', 'pug-cli')

    run = partial(sp.Popen,
                  stdout=sys.stdout,
                  stderr=sys.stderr,
                  cwd=str(package_base_dir.absolute()))

    with run(uninstallation_cmd), run(installation_cmd):
        print('beginning installation'); print()
    print(); print('finished installing pug-cli')

    sys.exit(0)
