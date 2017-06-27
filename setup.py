#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    name='ninjadog',
    version='0.3.2',
    description="Pug template support in Python",
    long_description=readme,
    author="Stephan Fitzpatrick",
    author_email='knowsuchagency@gmail.com',
    url='https://github.com/knowsuchagency/ninjadog',
    packages=find_packages(include=['ninjadog']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='ninjadog pug jinja2 html templating',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
    entry_points = {
        'console_scripts': ['ninjadog=ninjadog.cli:main']
    }
)
