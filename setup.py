#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from pathlib import Path
from configparser import ConfigParser

from setuptools import setup, find_packages


def get_requirements(config: ConfigParser, section: str) -> list:
    def gen():
        for item in config.items(section):
            lib, version = item
            lib, version = lib.strip('"'), version.strip('"')
            # ungracefully handle wildcard requirements
            if version == '*': version = ''
            yield lib + version

    return list(gen())


pip_config = ConfigParser()
pip_config.read('Pipfile')

packages = get_requirements(pip_config, 'packages')
dev_packages = get_requirements(pip_config, 'dev-packages')

setup(
    name='ninjadog',
    version='0.5.1',
    description="Pug template support in Python",
    long_description=Path('README.rst').read_text(),
    author="Stephan Fitzpatrick",
    author_email='knowsuchagency@gmail.com',
    url='https://github.com/knowsuchagency/ninjadog',
    packages=find_packages(include=['ninjadog']),
    include_package_data=True,
    install_requires=packages,
    license="MIT license",
    zip_safe=False,
    keywords='ninjadog pug jinja2 html templating',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=dev_packages,
    setup_requires='pytest-runner',
    entry_points={
        'console_scripts': ['ninjadog=ninjadog.cli:main'],
    },
    extras_require={
        'dev': dev_packages,
    },
)
