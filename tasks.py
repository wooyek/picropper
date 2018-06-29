# coding=utf-8
# Copyright (C) 2018 Janusz Skonieczny
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import logging
import os
import shutil
import sys
from collections import OrderedDict
from itertools import chain
from pathlib import Path

# noinspection PyPackageRequirements
from invoke import call, task

logging.basicConfig(format='%(asctime)s %(levelname)-7s %(thread)-5d %(filename)s:%(lineno)s | %(funcName)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
# logging.getLogger().setLevel(logging.INFO)
# logging.disable(logging.NOTSET)
logging.debug('Loading %s', __name__)

log = logging.getLogger(__name__)

is_win = sys.platform == 'win32'
ROOT_DIR = Path(__file__).parent.absolute()
SRC_DIR = ROOT_DIR / 'src'
VENV_DIR = ROOT_DIR / ".pve"
VENV_BIN = VENV_DIR / ("Scripts" if is_win else "bin")
PYTHON = VENV_BIN / 'python'
PIP = VENV_BIN / 'pip'
MANAGE = '{} {} '.format(PYTHON, SRC_DIR / 'manage.py')


def get_current_version():
    from configparser import ConfigParser
    cfg = ConfigParser()
    cfg.read(str(Path(ROOT_DIR) / 'setup.cfg'))
    current_version = cfg.get('bumpversion', 'current_version')
    return current_version


# noinspection PyUnusedLocal
@task
def version(ctx):
    print("Version: " + get_current_version())


@task
def clean(ctx):
    """Remote temporary files"""
    for item in chain(Path(ROOT_DIR).rglob("*.pyc"), Path(ROOT_DIR).rglob("*.pyo")):
        logging.debug("Deleting: %s", item)
        item.unlink()

    for item in Path(ROOT_DIR).rglob("__pycache__"):
        logging.debug("Deleting: %s", item)
        shutil.rmtree(str(item), ignore_errors=True)

    shutil.rmtree(str(ROOT_DIR / 'build'), ignore_errors=True)
    shutil.rmtree(str(ROOT_DIR / 'example_project' / '.eggs'), ignore_errors=True)
    shutil.rmtree(str(ROOT_DIR / '.eggs'), ignore_errors=True)
    shutil.rmtree(str(ROOT_DIR / '.tox'), ignore_errors=True)
    shutil.rmtree(str(ROOT_DIR / '.tmp'), ignore_errors=True)
    shutil.rmtree(str(ROOT_DIR / '.coverage'), ignore_errors=True)
    shutil.rmtree(str(ROOT_DIR / '.htmlcov'), ignore_errors=True)
    shutil.rmtree(str(ROOT_DIR / '.pytest_cache'), ignore_errors=True)
    shutil.rmtree(str(ROOT_DIR / '.cache'), ignore_errors=True)
    ctx.run('git checkout -- .tmp')


@task
def check(ctx):
    """Check project codebase cleanness"""
    ctx.run("flake8 src tests setup.py manage.py")
    ctx.run("isort --check-only --diff --recursive src tests setup.py")
    ctx.run("python setup.py check --strict --metadata --restructuredtext")
    ctx.run("check-manifest  --ignore .idea,.idea/* .")
    ctx.run("pytest --cov=src --cov=tests --cov-fail-under=100")


@task
def isort(ctx):
    """Check project codebase cleanness"""
    ctx.run("isort --recursive src tests setup.py")


@task
def detox(ctx):
    """Run detox with a subset of envs and report run separately"""
    envs = ctx.run("tox -l").stdout.splitlines()
    envs.remove('clean')
    envs.remove('report')
    envs = [e for e in envs if not e.startswith('py2')]
    log.info("Detox a subset of environments: %s", envs)
    ctx.run("tox -e clean")
    ctx.run("detox --skip-missing-interpreters -e " + ",".join(envs))
    ctx.run("tox -e report")


@task
def register_pypi(ctx):
    """Register project on PyPi"""
    ctx.run("git checkout master")
    ctx.run("python setup.py register -r pypi")


@task
def register_pypi_test(ctx):
    """Register project on TEST PyPi"""
    ctx.run("git checkout master")
    ctx.run("python setup.py register -r pypitest")


@task
def upload_pypi(ctx):
    """Upload to PyPi"""
    ctx.run("python setup.py sdist upload -r pypi")
    ctx.run("python setup.py bdist_wheel upload -r pypi")


@task(clean)
def dist(ctx):
    """Build setuptools dist package"""
    ctx.run("python setup.py sdist")
    ctx.run("python setup.py bdist_wheel")
    ctx.run("ls -l dist")


@task(clean)
def install(ctx):
    """Install setuptools dist package"""
    ctx.run("python setup.py install")


@task
def sync(ctx):
    """Sync master and develop branches in both directions"""
    ctx.run("git checkout develop")
    ctx.run("git pull origin develop --verbose")

    ctx.run("git checkout master")
    ctx.run("git pull origin master --verbose")

    ctx.run("git checkout develop")
    ctx.run("git merge master --verbose")

    ctx.run("git checkout develop")


@task(sync)
def sync_master(ctx):
    ctx.run("git checkout master")
    ctx.run("git merge develop --verbose")

    ctx.run("git checkout develop")
    ctx.run("git merge master --verbose")

    ctx.run("git push origin develop --verbose")
    ctx.run("git push origin master --verbose")
    ctx.run("git push --follow-tags")


@task
def bump(ctx):
    """Increment version number"""
    # ctx.run("bumpversion patch --no-tag")
    ctx.run("bumpversion patch")


@task()
def pip_compile(ctx):
    """Upgrade frozen requirements to the latest version"""
    ctx.run('pip-compile requirements/production.txt -o requirements/lock/production.txt --verbose --upgrade')
    ctx.run('sort requirements/lock/production.txt -o requirements/lock/production.txt')
    ctx.run('git add requirements/lock/*.txt')
    if ctx.run('git diff-index --quiet HEAD', warn=True).exited != 0:
        ctx.run('git commit -m "Requirements compiled by pip-compile" --allow-empty')


@task()
def pipenv(ctx):
    """Upgrade frozen requirements to the latest version"""
    ctx.run('pipenv install -r requirements/production.txt')
    ctx.run('pipenv install --dev -r requirements/development.txt')
    ctx.run('pipenv lock --requirements > requirements/lock/production.txt')
    ctx.run('pipenv lock --requirements --dev | grep -v "/multiinfo-python" -- > requirements/lock/development.txt')
    ctx.run('pipenv graph --reverse -- > requirements/lock/graph.txt')
    ctx.run('sort requirements/lock/production.txt -o requirements/lock/production.txt')
    ctx.run('sort requirements/lock/development.txt -o requirements/lock/development.txt')
    ctx.run('git add Pipfile Pipfile.lock requirements/lock/*.txt')
    ctx.run('git commit -m "Requirements locked by pipenv"')


@task
def assets(ctx):
    """
    Collect and build website assets
    """
    ctx.run("gulp")
    ctx.run("python manage.py collectstatic --noinput")  # in some cases assets build requires static to be updated
    ctx.run("python manage.py assets build")
    ctx.run("python manage.py collectstatic --noinput")  # update static with compressed assets
    ctx.run("git add --all static assets", warn=True)
    ctx.run('git commit -m "Build assets"', warn=True)


# noinspection PyUnusedLocal
@task(check, sync, detox)
def release_start(ctx):
    """Start a release cycle with publishing a release branch"""
    ctx.run("git flow release start v{}-release".format(get_current_version()))
    ctx.run("git merge master --verbose")
    ctx.run("bumpversion patch --no-tag --verbose ")
    ctx.run("git flow release --verbose publish")


# noinspection PyUnusedLocal
@task(check, sync, detox, post=[])
def release_finish(ctx):
    """Finish a release cycle with publishing a release branch"""
    ctx.run("git flow release finish --fetch --push")


# noinspection PyUnusedLocal
@task(isort, check, pip_compile, sync, detox, bump, sync_master)
def release(ctx):
    """Build new package version release and sync repo"""


# noinspection PyUnusedLocal
@task(release, post=[upload_pypi])
def publish(ctx):
    """Merge develop, create and upload new version"""
    ctx.run("git checkout master")
    ctx.run("git merge develop --verbose")


@task
def locales(ctx):
    """
    Collect and compile translation strings
    """
    # https://docs.djangoproject.com/en/dev/ref/django-admin/#django-admin-makemessages
    """
    python manage.py makemessages -v 3 --no-wrap --ignore ".*" --locale=pl_PL
    python manage.py compilemessages -v 3
    """
    tmp = ROOT_DIR / ".tmp"
    if not tmp.exists():
        os.makedirs(str(tmp))
    locale = ROOT_DIR / "src" / "locale"
    if not locale.exists():
        os.makedirs(str(locale))
    # http://babel.edgewall.org/wiki/BabelDjango
    pybabel = str(VENV_BIN / 'pybabel')
    ctx.run(pybabel + " extract -F locale/babel.cfg -o locale/django.pot --no-wrap --sort-output .")
    # create locales firs
    # pybabel init -D django -i locale/django.pot -d locale -l es
    # http://babel.edgewall.org/wiki/BabelDjango#CreatingandUpdatingTranslationsCatalogs
    # ctx.run(pybabel + " update -D django -i locale/django.pot -d locale --ignore-obsolete")
    ctx.run(pybabel + " update -D django -i locale/django.pot -d locale --previous --no-wrap")
    ctx.run(pybabel + " compile -D django -d locale --statistics")
    log.info("JavaScript locales")
    # ctx.run(pybabel + " update -D djangojs -i locale/djangojs.pot -d locale --previous --no-wrap")
    ctx.run("django-admin makemessages -d djangojs -i static -i node_modules")
    ctx.run(pybabel + " compile -D djangojs -d locale --statistics")


@task
def trigger_tests(ctx):
    """Trigger test cycle"""
    print(" #### Signaling test repo")
    ingeration_testing_root = str(Path(ROOT_DIR).parent / "integration-testing")
    print(ingeration_testing_root)
    env = {
        'GIT_WORK_TREE': ingeration_testing_root,
        'GIT_DIR': str(Path(ingeration_testing_root) / '.git'),
    }
    current_version = get_current_version()
    ctx.run("git checkout develop", env=env)
    cmd = 'git commit --allow-empty -m "Test release {}"'.format(current_version)
    print(cmd)
    ctx.run(cmd, env=env)
    ctx.run("git push origin develop", env=env)


@task(pre=[assets, release], post=[])
def deploy(ctx, remote='dev', branch='master'):
    """
    Collect and compile assets, add, commit and push to remote
    """
    ctx.run("git checkout {branch}".format(branch=branch))
    ctx.run("git push {remote} {branch}  --verbose".format(remote=remote, branch=branch))
    ctx.run("git checkout develop")
	# Uncomment this to show release script output
    # ctx.run("heroku logs -r {remote}".format(remote=remote))  
	# Uncomment this to show docker running containers
    # ctx.run("ssh developer@production.example.com docker ps")
    print("[ OK ] Deployed: " + get_current_version())


# noinspection PyUnusedLocal
@task(pre=[call(deploy, remote='production', branch='master')])
def deploy_production(ctx):
    """Deploy to production remote"""
    pass


# noinspection PyUnusedLocal
@task(pre=[call(deploy, remote='staging', branch='master')])
def deploy_staging(ctx):
    """Deploy to staging remote"""
    pass


@task
def vagrant(ctx):
    """
    Collect and compile assets, add, commit and push to production remote
    """
    ctx.run("git checkout develop")
    ctx.run("git push vagrant develop --verbose")


FIXTURES = OrderedDict((
    ("auth", (
        "auth.Group",
        "auth.User",
    )),
))


@task
def dump(ctx):
    """Dump django fixtures with initial and test data"""
    for file, what in FIXTURES.items():
        log.info("Dumping fixture: %s" % file)
        cmd = "python manage.py dumpdata --format=yaml --natural-foreign --natural-primary {} > " + str(ROOT_DIR / 'fixtures' / '{}.yaml')
        cmd = cmd.format(" ".join(what), file)
        log.debug(cmd)
        ctx.run(cmd)


@task
def reset_db(ctx):
    """Remove and reinitialize database"""
    data = ROOT_DIR / 'data'
    for p in data.glob("db.*"):
        os.remove(str(p))
    if not data.exists():
        os.makedirs(str(data))
    ctx.run("python manage.py migrate")


@task
def load_fixtures(ctx):
    """Load initial and test data fixtures"""
    for fixture in FIXTURES.keys():
        fixture = str(ROOT_DIR / 'fixtures' / (fixture + '.yaml'))
        log.info("Dumping fixture: %s" % fixture)
        cmd = "python manage.py loaddata " + fixture
        logging.debug(cmd)
        ctx.run(cmd)


@task(pre=[reset_db, load_fixtures])
def db(ctx):
    """
    Full database re-initialization
    """
    cmd = "python manage.py fill_test_data --on-empty"
    ctx.run(cmd)
