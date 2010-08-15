import os
import shutil
import unittest
from subprocess import Popen, PIPE
from pacha import main




class TestCommandLine(unittest.TestCase):

    def test_no_arguments(self):
        command = "pacha"
        run = Popen(command, shell=True, stdout=PIPE)
        actual = run.stdout.readlines()
        warning_msg = 'Warning! You have not set a configuration file for Pacha.\n'
        if warning_msg in actual:
            warning = True
        else:
            warning = False
        self.assertTrue(warning)



if __name__ == '__main__':
    unittest.main()
