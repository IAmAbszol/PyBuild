import shutil
import sys
import unittest

from pathlib import Path

from pybuild import pip
from pybuild import virtualenv
from pybuild.virtualenv import VirtualEnv
from pybuild.environment import Environment

class TestPip(unittest.TestCase):

    
    def test_freeze(self):
        req_file = 'test_freeze_req.txt'
        with Environment('testenv') as env:
            requirements_path = pip.freeze(env, req_file)
            assert requirements_path.exists(), f'Missing frozen file {req_file}.'
            requirements_path.unlink()


    def test_list(self):
        with Environment('testenv') as env:
            assert len(pip.list(env, log_output=False)) > 0, 'List must return at least one package.'


    def test_install(self):
        with Environment('testenv') as env:
            VirtualEnv(env)
            packages = pip.list(env, log_output=False)
            pip.install(env, 'matplotlib')
            assert len(packages) != len(pip.list(env, log_output=False)), 'Packages currently installed hasn\'t changed.'
            package, _ = env.dependency_exists('matplotlib')
            assert package == 'matplotlib', 'Missing dependency matplotlib.'


    def test_uninstall(self):
        with Environment('testenv') as env:
            VirtualEnv(env)
            pip.install(env, 'matplotlib')
            package, _ = env.dependency_exists('matplotlib')
            assert package is not None, 'Matplotlib failed to install.'
            pip.uninstall(env, 'matplotlib')
            package, _ = env.dependency_exists('matplotlib')
            assert package is None, 'Matplotlib failed to uninstall.'


if __name__ == '__main__':
    unittest.main()