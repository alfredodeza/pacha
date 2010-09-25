from sqlite3 import Row
import sqlite3
import os

# Fixes Database Absolute Location
FILE_CWD =  os.path.abspath(__file__)
FILE_DIR = os.path.dirname(FILE_CWD)
DB_FILE = FILE_DIR+'/db/pacha.db'


CONFIG_TABLE = """CREATE TABLE IF NOT EXISTS config(
    path            TEXT, 
    frequency       INT, 
    master          VARCHAR(12), 
    host            VARCHAR(32),
    ssh_user        VARCHAR(32),
    ssh_port        INT,
    hosts_path      TEXT,
    hg_autocorrect  VARCHAR(12),
    log_enable      VARCHAR(12),
    log_path        VARCHAR(12),
    log_level       VARCHAR(12),
    log_format      TEXT,
    log_datefmt     TEXT 
)"""


REPOS_TABLE = """CREATE TABLE IF NOT EXISTS repos(
    id              integer primary key, 
    path            TEXT,  
    permissions     TEXT, 
    type            TEXT, 
    revision        TEXT
)"""


METADATA_TABLE = """CREATE TABLE IF NOT EXISTS metadata(
    id          integer primary key, 
    path        TEXT,
    owner       TEXT, 
    grp         TEXT, 
    permissions INT, 
    ftype       TEXT
)""" #sqlite does not like 'group'



def is_tracked():
    """Is this database being tracked?"""
    hg_dir = FILE_DIR+'/db/.hg'
    if os.path.isdir(hg_dir):
        return True
    return False


class Worker(object):
    """All database operations happen here"""

    def __init__(self,
            db = DB_FILE):
        self.db = db 
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()
        self.c.execute(REPOS_TABLE)
        self.c.execute(METADATA_TABLE)
        self.c.execute(CONFIG_TABLE)


    def closedb(self):
        """Make sure the db is closed"""
        self.conn.close()


    def insert(self, path=None, permissions=None, type=None, revision=None):
        """Puts a new repo in the database and checks if the record
        is not already there"""
        values = (path, permissions, type, revision, path)
        command = 'INSERT INTO repos(path, permissions, type, revision) select ?,?,?,? WHERE NOT EXISTS(SELECT 1 FROM repos WHERE path=?)'
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

