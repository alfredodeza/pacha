import sys
if '../' not in sys.path:
    sys.path.append('../')
import unittest
import os
from lib import confparser

class TestParse(unittest.TestCase):

    def setUp(self):
        """Create a bogus config file"""
        config_file = open('test.conf', 'w')
        config_file.write('one = True\n')
        config_file.write("""two = ['a']\n""")
        config_file.write('three = {"number":"three"}\n')
        config_file.write('# a comment that should not be readi\n')
        config_file.close()

    def tearDown(self):
        os.remove('test.conf')

    def test_options(self):
        """False if IOError happens"""
        parse = confparser.Parse('test.conf')
        parse.options()

        self.assertTrue(hasattr(parse, 'one'))

if __name__ == '__main__':
    unittest.main()
