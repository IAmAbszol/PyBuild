import shutil
import unittest

from pathlib import Path

from pybuild import virtualenv
from pybuild.environment import Environment

class TestEnvironment(unittest.TestCase):

    def test_creation(self):
        test_env = Path('test_creation_env')
        environment = Environment(test_env.name)
        virtualenv.VirtualEnv(environment)
        assert test_env.exists(), 'Virtual environment wasn\'t created.'

        environment.cleanup()
        assert not test_env.exists(), 'Failed to delete virtual environment.'


    def test_with_context(self):
        test_env = Path('test_withcontext_env')
        with Environment(test_env.name) as env:
            virtualenv.VirtualEnv(env)
            assert test_env.exists(), 'Virtual environment wasn\'t created.'
        assert not test_env.exists(), 'Failed to delete virtual environment.'


if __name__ == '__main__':
    unittest.main()