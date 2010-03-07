import sys
if '../' not in sys.path:
    sys.path.append('../')
import unittest
from subprocess import Popen, PIPE
import os
import shutil
import upgrade

class TestUpgrade(unittest.TestCase):

    def tearDown(self):
        """Remove some croft"""
        try:
            shutil.rmtree('/tmp/pacha')
            shutil.rmtree('/tmp/upgrade')
            os.remove('/tmp/pacha')
        except OSError:
            pass # maybe file was not downloaded

    def test_get(self):
        """Download a Pacha tar.gz file"""
        up = upgrade.Upgrade()
        link = up.download_link()
        tar_file = '/tmp/%s' % up.url_filename(link)
        up.get()
        expected = os.path.isfile(tar_file)
        self.assertTrue(expected)

    
    def test_is_number_true(self):
        """Pass a number and return True"""
        up = upgrade.Upgrade()
        number = '1'
        expected = up.is_number(number)
        self.assertTrue(expected)

    def test_is_number_false(self):
        """Pass a string and return False"""
        up = upgrade.Upgrade()
        string = "foo"
        expected = up.is_number(string)
        self.assertFalse(expected)

    def test_url_filename(self):
        """Pass a full url and return the filename"""
        url = 'http://pacha.googlecode.com/files/pacha-0.0.3.tar.gz'
        up = upgrade.Upgrade(url)
        actual = up.url_filename(url)
        expected = 'pacha-0.0.3.tar.gz'
        self.assertEqual(actual, expected)

    def test_url_check_true(self):
        """Validate a working url by returning True"""
        url = 'http://www.google.com'
        up = upgrade.Upgrade(url)
        expected = up.url_check()
        self.assertTrue(expected)

#    def test_url_check_false(self):
#        """Return False for a non working URL"""
#        url = 'http://a_non_working_url.return.false'
#        up = upgrade.Upgrade(url)
#        expected = up.url_check()
#        self.assertFalse(expected)

    def test_current_version(self):
        """Verify the current Pacha version"""
        up = upgrade.Upgrade()
        command = "pacha --version"
        get_version = Popen(command, shell=True, stdout=PIPE)
        # this return is a mouthful...
        expected = get_version.stdout.readlines()[0].split('\n')[0]
        actual = up.current_version()
        self.assertEqual(actual, expected)

    def test_download_link_list(self):
        """Open a url and get a list"""
        url = 'http://code.google.com/p/pacha'
        up = upgrade.Upgrade(url)
        actual = type(up.download_link()) is list
        self.assertTrue(actual)

    def test_download_link(self):
        """Pass an html file object and return a valid download link"""
        up = upgrade.Upgrade('/tmp/index.html')
        html = open('/tmp/index.html', 'w')
        html.write("""<a href="http://pacha.googlecode.com/files/pacha-0.0.3.tar.gz">pacha-0.0.3.tar.gz</a>""")
        html.close()
        expected = 'http://pacha.googlecode.com/files/pacha-0.0.3.tar.gz'
        actual = up.download_link()[0]
        self.assertEqual(actual, expected)

    def test_repos_check_true(self):
        """Return True if there is a .repos file"""
        open('/tmp/.repos', 'w')
        up = upgrade.Upgrade(repo_file = '/tmp/.repos')
        actual = up.repos_check()
        self.assertTrue(actual)

    def test_repos_check_false(self):
        """Return FALSE if there is not .repos file"""
        up = upgrade.Upgrade(repo_file = '/tmp/aNONexistentrepos')
        actual = up.repos_check()
        self.assertFalse(actual)

    def test_remove_repo_file(self):
        """Remove the lingering .repos file"""
        open('/tmp/.repos', 'w')
        up = upgrade.Upgrade(repo_file = '/tmp/.repos')
        up.remove_repo_file()
        actual = os.path.isfile('/tmp/.repos')
        self.assertFalse(actual)

if __name__ == '__main__':
    unittest.main()
