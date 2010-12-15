import unittest

class TestImports(unittest.TestCase):


    def test_import_pacha(self):
        try:
            import pacha
            imported = True
        except:
            imported = False
        self.assertTrue(imported)

    def test_pacha_config(self):
        try:
            from pacha import config
            imported = True
        except:
            imported = False
        self.assertTrue(imported)

    def test_pacha_daemon(self):
        try:
            from pacha import daemon
            imported = True
        except:
            imported = False
        self.assertTrue(imported)

    def test_pacha_database(self):
        try:
            from pacha import database
            imported = True
        except:
            imported = False
        self.assertTrue(imported)


    def test_pacha_permissions(self):
        try:
            from pacha import permissions
            imported = True
        except:
            imported = False
        self.assertTrue(imported)


    def test_pacha_host(self):
        try:
            from pacha import host
            imported = True
        except:
            imported = False
        self.assertTrue(imported)



if __name__ == '__main__':
    unittest.main()
