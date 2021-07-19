import unittest

from pathlib import Path

from pybuild.virtualenv import VirtualEnv
from pybuild.environment import Environment

class TestVirtualEnv(unittest.TestCase):

    
    def test_virtualenv(self):
        with Environment('testenv') as env:
            VirtualEnv(env)
            assert Path('testenv').exists(), 'Failed to find virtual environment folder.'
            

if __name__ == '__main__':
    unittest.main()