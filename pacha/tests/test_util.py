import unittest
import sys

from mock import MockSys
from pacha.util import run_command

class RunCommand(unittest.TestCase):

    def test_run_command_stdout(self):
        sys.stderr = MockSys()
        actual = run_command(std="stdout", cmd="""echo "foo" """)
        expected = ['foo\n']
        self.assertEqual(actual, expected) 

    def test_run_command_stderr(self):
        sys.stderr = MockSys()
        actual = run_command(std="stderr", cmd=""" echo "error message" 1>&2 """)
        expected = ['error message\n']
        self.assertEqual(actual, expected) 

if __name__ == '__main__':
    unittest.main()
