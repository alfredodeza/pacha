import unittest

class TestDependencies(unittest.TestCase):


    def test_hg(self):
        try:
            import mercurial 
            imported = True
        except:
            imported = False
        self.assertTrue(imported)

    def test_hg_commands(self):
        try:
            from mercurial import commands
            imported = True
        except:
            imported = False
        self.assertTrue(imported)

    def test_hg_ui(self):
        try:
            from mercurial import ui
            imported = True
        except:
            imported = False
        self.assertTrue(imported)

    def test_hg_hg(self):
        try:
            from mercurial import hg
            imported = True
        except:
            imported = False
        self.assertTrue(imported)


if __name__ == '__main__':
    unittest.main()
