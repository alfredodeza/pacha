import sys
if '../' not in sys.path:
    sys.path.append('../')
import unittest
import os
from lib import confparser

class TestParseText(unittest.TestCase):

    def setUp(self):
        """Create a text file to read"""
        txt = open('txt.conf', 'w')
        txt.write('one\n')
        txt.close()

    def tearDown(self):
        os.remove('txt.conf')

    def test_text_append(self):
        """Append a line to the end of the file"""
        parse = confparser.Parse('txt.conf',
                new_value = 'lastline')
        parse.text_append()
        txt = open('txt.conf')
        actual = txt.readlines()[-1]
        expected = 'lastline\n'
        self.assertEqual(actual, expected)

    def test_text_read_list(self):
        """Get a list of all the values in the txt file"""
        parse = confparser.Parse('txt.conf')
        actual = parse.text_read()
        expected = ['one']
        self.assertEqual(actual, expected)

class TestParse(unittest.TestCase):

    def setUp(self):
        """Create a bogus config file"""
        config_file = open('test.conf', 'w')
        config_file.write('one = True\n')
        config_file.write("""two = ['a']\n""")
        config_file.write('three = {"number":"three"}\n')
        config_file.write('#comment =\n')
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

    def test_option_list(self):
        """We should get a list from an option"""
        expected = ['a']
        actual = self.parse.two
        self.assertEqual(actual, expected)

    def test_option_list_value(self):
        """We should get an item from a value list"""
        expected = 'a'
        actual = self.parse.two[0]
        self.assertEqual(actual, expected)

    def test_option_dictionary(self):
        """We should get a dictionary from an option"""
        expected = {"number":"three"}
        actual = self.parse.three
        self.assertEqual(actual, expected)

    def test_option_dictionary_value(self):
        """We should get an item from a value dictionary"""
        expected = "three"
        actual = self.parse.three['number']
        self.assertEqual(actual, expected)

    def test_option_comment(self):
        """A comment should not be evaluated"""
        actual = hasattr(self.parse, 'comment')
        self.assertFalse(actual)


if __name__ == '__main__':
    unittest.main()
