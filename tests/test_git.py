import unittest

from pathlib import Path

from pybuild.virtualenv import VirtualEnv
from pybuild.environment import Environment

class TestGit(unittest.TestCase):

    
    def test_git(self):
        """
        TODO:   Add clone test here. When deleting a cloned repository, .git causes rmtree to fail.
                Recursively going through the contents of .git, bottom up, deleting the files might resolve this.
        """
        pass

if __name__ == '__main__':
    unittest.main()