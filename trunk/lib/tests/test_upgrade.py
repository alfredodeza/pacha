import sys
if '/opt/pacha/lib' not in sys.path:
    sys.path.append('/opt/pacha/lib')
import unittest
from subprocess import Popen, PIPE
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

    def test_url_check_true(self):
        """Validate a working url by returning True"""
        url = 'http://www.google.com'
        expected = upgrade.url_check(url)
        self.assertTrue(expected)

    def test_url_check_false(self):
        """Return False for a non working URL"""
        url = 'http://a_non_working_url.return.false'
        expected = upgrade.url_check(url)
        self.assertFalse(expected)

    def test_current_version(self):
        """Verify the current Pacha version"""
        command = "pacha --version"
        get_version = Popen(command, shell=True, stdout=PIPE)
        # this return is a mouthful...
        expected = get_version.stdout.readlines()[0].split('\n')[0]
        actual = upgrade.current_version()
        self.assertEqual(actual, expected)

    def test_download_link_list(self):
        """Open a url and get a list"""
        url = 'http://code.google.com/p/pacha'
        actual = type(upgrade.download_link(url)) is list
        self.assertTrue(actual)

    def test_download_link(self):
        """Pass an html file object and return a valid download link"""
        html = open('/tmp/index.html', 'w')
        html.write("""<a href="http://pacha.googlecode.com/files/pacha-0.0.3.tar.gz">pacha-0.0.3.tar.gz</a>""")
        html.close()
        expected = 'http://pacha.googlecode.com/files/pacha-0.0.3.tar.gz'
        actual = upgrade.download_link('/tmp/index.html')[0]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
