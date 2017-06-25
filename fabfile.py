from fabric.api import *
from functools import singledispatch


@singledispatch
def true(arg):
    """
    Determine of the argument is True.
    
    Since arguments coming from the command line
    will always be interpreted as strings by fabric
    this helper function just helps us to do what is
    expected when arguments are passed to functions
    explicitly in code vs from user input.
    
    Just make sure NOT to do the following with task arguments:
    
    @task
    def foo(arg):
        if arg: ...
        
    Always wrap the conditional as so
    
    @task
    def foo(arg):
        if true(arg): ...
        
    and be aware that true('false') -> False
    
    Args:
        arg: anything

    Returns: bool

    """
    return bool(arg)


@true.register(str)
def _(arg):
    """If the lowercase string start with 't' return True."""
    return arg.lower().startswith('t')


@task
def clean_build():
    """Remove build artifacts."""
    local('rm -fr build/')
    local('rm -fr dist/')
    local('rm -rf .eggs/')
    local("find . -name '*.egg-info' -exec rm -fr {} +")
    local("find . -name '*.egg' -exec rm -f {} +")


@task
def clean_pyc():
    """Remove Python file artifacts."""
    local("find . -name '*.pyc' -exec rm -f {} +")
    local("find . -name '*.pyo' -exec rm -f {} +")
    local("find . -name '*~' -exec rm -f {} +")
    local("find . -name '__pycache__' -exec rm -fr {} +")


@task
def clean_test():
    """Remove test and coverage artifacts."""
    local('rm -fr .tox/')
    local('rm -f .coverage')
    local('rm -fr htmlcov/')


@task
def clean():
    """Remove all build, test, coverage and Python artifacts."""
    clean_build()
    clean_pyc()
    clean_test()


@task
def test():
    """Run tests quickly with default Python."""
    local('py.test')


@task(alias='tox')
def test_all():
    """Run on multiple Python versions with tox."""
    local('tox')


@task
def coverage(open_browser=True):
    """Check code coverage quickly with the default Python."""
    local('coverage run --source ninjadog -m pytest')
    local('coverage report -m')
    local('coverage html')
    if true(open_browser):
        local('open htmlcov/index.html')


@task
def docs(open_browser=True):
    """
    Generage Sphinx HTML documentation, including API docs.
    
    Args:
        open_browser: Open browser automatically after building docs
    """
    local('rm -f docs/ninjadog.rst')
    local('rm -f docs/modules.rst')
    local('sphinx-apidoc -o docs/ ninjadog')

    with lcd('docs'):
        local('make clean')
        local('make html')

    local('cp -rf docs/_build/html/ public/')

    if true(open_browser):
        local('open public/index.html')


@task
def publish_docs():
    """
    Compile docs and publish to GitHub Pages.
    
    Logic borrowed from https://gohugo.io/tutorials/github-pages-blog/
    """
    with settings(warn_only=True):
        if local('git diff-index --quiet HEAD --').failed:
            local('git status')
            abort('The working directory is dirty. Please commit any pending changes.')

    # deleting old publication
    local('rm -rf public')
    local('mkdir public')
    local('git worktree prune')
    local('rm -rf .git/worktrees/public/')
    # checkout out gh-pages branch into public
    local('git worktree add -B gh-pages public ninjadog/gh-pages')
    # generating docs
    docs(open_browser=False)
    # push to github
    with lcd('public'), settings(warn_only=True):
        local('git add .')
        local('git commit -m "Publishing to gh-pages (Fabfile)"')
        local('git push ninjadog gh-pages')


@task
def dist():
    """Build source and wheel package."""
    clean()

    local('python setup.py sdist')
    local('python setup.py bdist_wheel')


@task
def release():
    """Package and upload a release."""
    test()
    clean()
    publish_docs()

    local('python setup.py sdist upload')
    local('python stup.py bdist_wheel upload')


@task
def install(development_mode=True):
    """
    Install package.
    
    Args:
        development_mode: Install locally as opposed to site-packages
    """
    clean()

    if development_mode:
        local('pip install -e .')
    else:
        local('pip install .')
    local('pip install -r requirements_dev.txt')
