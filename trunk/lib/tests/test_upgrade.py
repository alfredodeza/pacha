import sys
if '/opt/pacha/lib' not in sys.path:
    sys.path.append('/opt/pacha/lib')
import unittest
import upgrade

class TestHost(unittest.TestCase):
    
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

if __name__ == '__main__':
    unittest.main()
