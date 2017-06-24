from fabric.api import *

def clean_build():
    """Remove build artifacts"""
    local('rm -fr build/')
    local('rm -fr dist/')
    local('rm -rf .eggs/')
    local("find . -name '*.egg-info' -exec rm -fr {} +")
    local("find . -name '*.egg' -exec rm -f {} +")

