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
        self.parse = confparser.Parse('test.conf')
        self.parse.options()

    def tearDown(self):
        os.remove('test.conf')

    def test_options_parse(self):
        """Should pick up the options when parsing"""
        self.assertTrue(hasattr(self.parse, 'one'))

    def test_option_string(self):
        """We should get a string from an option"""
        expected = 'True'
        actual = self.parse.one
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
