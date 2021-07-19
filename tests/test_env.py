import sys
import unittest

from pathlib import Path

from pybuild import pip
from pybuild.virtualenv import VirtualEnv
from pybuild.environment import Environment

class TestEnvironment(unittest.TestCase):


    def test_creation(self):
        test_env = Path('test_creation_env')
        environment = Environment(test_env.name)
        VirtualEnv(environment)
        assert test_env.exists(), 'Virtual environment wasn\'t created.'

        environment.cleanup()
        assert not test_env.exists(), 'Failed to delete virtual environment.'


    def test_with_context(self):
        test_env = Path('test_withcontext_env')
        with Environment(test_env.name) as env:
            VirtualEnv(env)
            assert test_env.exists(), 'Virtual environment wasn\'t created.'
        assert not test_env.exists(), 'Failed to delete virtual environment.'


    def test_dependency_exists(self):
        with Environment('testenv') as env:
            VirtualEnv(env)
            pip.install(env, 'matplotlib')
            dep = env.dependency_exists('matplotlib')
            assert dep[0] == 'matplotlib', 'Dependency matplotlib must exist.'
            dep = env.dependency_exists('pyinstaller')
            assert dep == (None, None), 'None must be returned.'


    def test_directories(self):
        with Environment('testenv') as env:
            VirtualEnv(env)
            executables = env.executables()
            assert len(executables) > 0, 'Executable directory must contain at least one file.'
            libs = env.libs()
            assert len(libs) > 0, 'Lib directory must contain at least one file.'


    def test_info(self):
        with Environment('testenv') as env:
            info = env.info()
            assert isinstance(info, tuple), 'Info must be of instance \'tuple\'.'
            assert isinstance(info[0], tuple), 'version_info must be of type tuple.'
            assert isinstance(info[1], int), 'Bit must be of type int.'


    def test_name(self):
        with Environment('testenv') as env:
            assert env.name() == 'testenv', 'Environment name must match instantiated name.'

    
    def test_python_func(self):
        with Environment('testenv') as env:
            assert str(env.python()) == sys.executable, 'System executable and environment executable must match.'
            VirtualEnv(env)
            assert str(env.python()) != sys.executable, 'System executable and environment executable must differ, virtual env addition.'


    def test_wipe(self):
        with Environment('testenv') as env:
            VirtualEnv(env)
            pip.install(env, 'matplotlib', 'pyinstaller', 'pandas', no_cache_dir=True)
            previous_packages = pip.list(env, log_output=False)
            env.wipe()
            current_packages = pip.list(env, log_output=False)
            assert len(previous_packages) != len(current_packages), 'Package lengths must differ after wipe.'


if __name__ == '__main__':
    unittest.main()