import subprocess as sp
import sys
from functools import partial
from pathlib import Path

# make sure we're in temporary directory
# so that we're sure to import ppug from
# site-packages
import os
from tempfile import gettempdir
os.chdir(gettempdir())

import pkg_resources

import ppug


def main():
    """Use npm to install the pug-cli"""
    package_basedir = Path(ppug.__path__[0])

    print('installing node_modules in', package_basedir)

    run = partial(sp.Popen,
                  stdout=sys.stdout,
                  stderr=sys.stdout,
                  cwd=package_basedir,
                  )

    # install pug-cli
    with run('npm install -f', shell=True):
        print('beginning installation\n')
    print('\nfinished installing pug-cli')

