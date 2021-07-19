import unittest

from test_env import TestEnvironment
from test_git import TestGit
from test_pdoc import TestPdoc
from test_pip import TestPip
from test_virtualenv import TestVirtualEnv


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestEnvironment))
    suite.addTest(unittest.makeSuite(TestGit))
    suite.addTest(unittest.makeSuite(TestPdoc))
    suite.addTest(unittest.makeSuite(TestPip))
    suite.addTest(unittest.makeSuite(TestVirtualEnv))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())