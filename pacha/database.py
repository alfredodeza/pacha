from time               import time

import sqlite3
import os

from pacha.util         import get_db_file, get_db_dir


REPOS_TABLE = """CREATE TABLE IF NOT EXISTS repos(
    id              integer primary key, 
    path            TEXT,  
    permissions     TEXT, 
    type            TEXT, 
    timestamp       TEXT
)"""


METADATA_TABLE = """CREATE TABLE IF NOT EXISTS metadata(
    id          integer primary key, 
    path        TEXT,
    owner       TEXT, 
    grp         TEXT, 
    permissions INT, 
    ftype       TEXT
)""" 


DB_FILE = get_db_file()
DB_DIR = get_db_dir()


#def is_tracked():
#    """Is this database being tracked?"""
#    hg_dir = DB_DIR+'/.hg'
#    if os.path.isdir(hg_dir):
#        return True
#    return False
#

class Worker(object):
    """CRUD Database operations"""

    def __init__(self, db = DB_FILE):
        self.db = db 
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()
        self.c.execute(REPOS_TABLE)
        self.c.execute(METADATA_TABLE)


    def is_tracked(self):
        repo = [i for i in self.get_repo(DB_DIR)]
        if repo:
            return True 
        return False

    def closedb(self):
        """Make sure the db is closed"""
        self.conn.close()


    def insert(self, path=None, permissions=None, type=None, timestamp=None):
        """Puts a new repo in the database and checks if the record
        is not already there"""
        stat = os.lstat(path)
        timestamp = int(stat.st_mtime)
                      
        values = (path, permissions, type, timestamp, path)
        command = 'INSERT INTO repos(path, permissions, type, timestamp) select ?,?,?,? WHERE NOT EXISTS(SELECT 1 FROM repos WHERE path=?)'
        self.c.execute(command, values)
        self.conn.commit()


    def insert_meta(self, path, owner, grp, permissions, ftype):
        """Gets the metadata into the corresponding table"""
        values = (path, owner, grp, permissions, ftype, path)
        command = 'INSERT INTO metadata(path, owner, grp, permissions, ftype) select ?,?,?,?,? WHERE NOT EXISTS(SELECT 1 FROM metadata WHERE path=?)'
        self.c.execute(command, values)
        self.conn.commit()


    def get_meta(self, path):
        """Gets metadata for a specific file"""
        values = (path,)
        command = "SELECT * FROM metadata WHERE path = (?)"
        return self.c.execute(command, values)


    def update_timestamp(self, path, timestamp):
        """Updates the timestamp for a repo that got modified"""
        values = (timestamp, path)
        command = 'UPDATE repos SET timestamp=? WHERE path=?'
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

