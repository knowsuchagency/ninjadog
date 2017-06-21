import subprocess as sp
import sys
from functools import partial
from pathlib import Path


def main():
    """Use npm to install the pug-cli"""
    package_basedir = Path(__file__).parent.parent
    print('installing node_modules in', package_basedir)

    run = partial(sp.Popen,
                  stdout=sys.stdout,
                  stderr=sys.stdout,
                  cwd=package_basedir,
                  )

    if not Path(package_basedir, 'package.json').exists():
        with run(('calmjs', 'npm', '--init', 'ppug')):
            print('No package.json found. Creating it now.')

    with run('npm install', shell=True):
        print('beginning installation\n')
    print('\nfinished installing pug-cli')
