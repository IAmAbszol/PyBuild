import tempfile

from os import environ
from pathlib import Path

from pybuild.environment import Environment
from pybuild import pdoc
from pybuild.utils import file_utils
from pybuild.virtualenv import VirtualEnv
from pybuild import git
from pybuild import pip

# Bug: Doesn't change python interpreter when running from base system rather than virtualenv to virtualenv
# environment = Environment('pybuildenv')
with Environment('pybuildenv') as environment:
    VirtualEnv(environment)
    pip.install(environment, 'pyinstaller', no_cache_dir=True)
    pip.list(environment)