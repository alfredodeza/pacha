import sys
if '/opt/pacha/lib' not in sys.path:
    sys.path.append('/opt/pacha/lib')
import unittest
import upgrade

class TestUpgrade(unittest.TestCase):
    
    def test_is_number_true(self):
        """Pass a number and return True"""
        number = '1'
        expected = upgrade.is_number(number)
        self.assertTrue(expected)

    def test_is_number_false(self):
        """Pass a string and return False"""
        string = "foo"
        expected = upgrade.is_number(string)
        self.assertFalse(expected)

    def test_url_filename(self):
        """Pass a full url and return the filename"""
        url = 'http://pacha.googlecode.com/files/pacha-0.0.3.tar.gz'
        actual = upgrade.url_filename(url)
        expected = 'pacha-0.0.3.tar.gz'
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
