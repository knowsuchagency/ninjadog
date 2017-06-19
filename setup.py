#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'calmjs',
    'jinja2',
    'pyramid_jinja2',
]

setup_requirements = [
    'pytest-runner',
    # TODO(knowsuchagency): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

extras_calmjs = {
    'node_modules': {
        'pug': '/.bin/pug',
    }
}

setup(
    name='ppug',
    version='0.1.0',
    description="Pug template support in Python",
    long_description=readme + '\n\n' + history,
    author="Stephan Fitzpatrick",
    author_email='knowsuchagency@gmail.com',
    url='https://github.com/knowsuchagency/ppug',
    packages=find_packages(include=['ppug']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='ppug',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
    extras_calmjs=extras_calmjs,
)
