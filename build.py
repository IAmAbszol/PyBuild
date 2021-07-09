import tempfile

from os import environ
from pathlib import Path

from pybuild.environment import Environment
from pybuild.utils import file_utils
from pybuild.virtualenv import VirtualEnv
from pybuild import git
from pybuild import pip

with Environment('pybuildenv') as environment:
    VirtualEnv(environment)
    pip.install(environment, '-e .')
    # with tempfile.TemporaryDirectory() as tmpfd:
    #     git_path = git.clone('https://github.com/IAmAbszol/Alfred.git', destination=Path(tmpfd, 'DogWater'), branch='dev')
    #     file_utils.move(git_path, '.')