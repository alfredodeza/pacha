"""Simple database work. We do not need an ORM to do this for us."""
import sqlite3
import os

class Worker(object):
    """All database operations happen here"""

    def __init__(self,
            db = '/opt/pacha/db/pacha.db'):
        self.db = db 
        if os.path.isfile(self.db):
            self.conn = sqlite3.connect(self.db)
            self.c = self.conn.cursor()
        else:
            self.conn = sqlite3.connect(self.db)
            table = """CREATE TABLE repos(id integer primary key, path TEXT, 
 permissions TEXT, type TEXT, revision TEXT)"""
            table2 = """CREATE TABLE metadata(id integer primery key, path TEXT,
 owner TEXT, group TEXT, permissions INT, ftype TEXT)"""
            self.c = self.conn.cursor()
            self.c.execute(table)
            self.c.execute(table2)

    def insert(self, path=None, permissions=None, type=None, revision=None):
        """Puts a new repo in the database and checks if the record
        is not already there"""
        values = (path, permissions, type, revision, path)
        command = 'INSERT INTO repos(path, permissions, type, revision) select ?,?,?,? WHERE NOT EXISTS(SELECT 1 FROM repos WHERE path=?)'
        self.c.execute(command, values)
        self.conn.commit()
        self.conn.close()

    def insert_meta(self, path, owner, group, permissions, ftype):
        """Gets the metadata into the corresponding table"""
        values = (path, owner, group, permissions, ftype, path)
        command = 'INSERT INTO metadata(path, owner, group, permissions, ftype) select ?,?,?,?,? WHERE NOT EXISTS(SELECT 1 FROM metadata WHERE path=?)'
        self.c.execute(command, values)
        self.conn.commit()
        self.conn.close()

    def update_rev(self, path, revision):
        """Inserts a path with a revision and keeps updating this 
        for a comparison """
        values = (revision, path)
        command = 'UPDATE repos SET revision=? WHERE path=?'
        self.c.execute(command, values)
        self.conn.commit()

    def remove(self, path):
        """Removes a repo from the database"""
        values = (path,)
        command = "DELETE FROM repos WHERE path = (?)"
        self.c.execute(command, values)
        self.conn.commit()

    def get_repos(self):
        """Gets all the hosts"""
        command = "SELECT * FROM repos"
        return self.c.execute(command)

    def get_repo(self, host):
        """Gets attributes for a specific repo"""
        values = (host,)
        command = "SELECT * FROM repos WHERE path = (?)"
        return self.c.execute(command, values)

