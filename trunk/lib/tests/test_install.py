# only way to import stuff from where ever we are
import sys
sys.path.append('../')

import os
import unittest
import install
import uninstall

class TestMain(unittest.TestCase):
   
    def setUp(self):
        install.main()

    def test_pacha_dir(self):
        """We should have a pacha dir"""
        dir_created = os.path.isdir('/opt/pacha')
        self.assertTrue(dir_created)

    def test_absolute_pacha(self):
        """pacha.py should have been copied"""
        absolute_pacha = os.path.isfile('/opt/pacha/pacha.py')
        self.assertTrue(absolute_pacha)

    def test_daemon(self):
        """We should have copied the daemon to init"""
        daemon = os.path.isfile('/etc/init.d/pacha')
        self.assertTrue(daemon)

#    def test_main(self):
        # self.assertEqual(expected, main())
#        assert False # TODO: implement your test here

    def tearDown(self):
        uninstall.main()

if __name__ == '__main__':
    unittest.main()
