import shutil
import unittest

from pathlib import Path

from pybuild import pdoc
from pybuild.environment import Environment

class TestPdoc(unittest.TestCase):

    
    def test_pdoc(self):
        with Environment('testenv') as env:
            doc_path = pdoc.make(env, 'pybuild', force=True, output_dir='test_doc')
            assert doc_path.exists(), 'Failed to create out directory for pdoc.'
            shutil.rmtree(doc_path)


if __name__ == '__main__':
    unittest.main()