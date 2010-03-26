"""Will attempt to get the owner and permissions of a file to be able to 
set them correctly when rebuilding"""

import pwd
import grp
import os
import stat
import database

class Permissions(object):
    """Gathers the exact metadata we need for every file or given
    directory, like owner, group ownership and the octogonal 
    representation of RWX-RWX-RWX type permissions"""

    def __init__(self, 
            path):
        self.path = path
        self.stat = os.stat(self.path)
        self.info = self.stat.st_uid

    def owner(self):
        """Return the owner of a given file or directory"""
        owner = pwd.getpwuid(self.info)[0]
        return owner

    def group(self):
        """Return the group of a give file or directory"""
        group = grp.getgrgid(self.info)[0]
        return group

    def rwx(self):
        """Numeric value for permissions on a file"""
        mode = self.stat[stat.ST_MODE]
        return oct(mode & 0777)

class Tracker(object):
    """with the information coming from the Permissions class, Tracker
    inserts the correct information to the database"""

    def __init__(self,
            path,
            database = '/opt/pacha/db/meta.db')
        self.path = path
        self.database = database

    def walker(self):
        """If we have a directory, walk every file in it"""

        for root, directory, files in os.walk(self.path):
            for f in files:
                try:
                    absollute = os.path.join(root, f)
                    metadata = Permissions(absolute)
                    if os.path.isfile(absolute):
                        own = metadata.owner()
                        grp = metadata.group()
                        permissions = metadata.rwx()
                        self.insert(absolute, own, grp, permissions,
                                    'file')
    def single_file(self):
        """If we are given a single file we get the information without
        trying to walk the whole tree"""
        if os.path.isfile(self.path):
            metadata = Permissions(self.path)
            own = metadata.owner()
            grp = metadata.group()
            permissions = metadata.rwx()
            self.insert(absolute, own, grp, permissions,
                    'dir')


    def insert(self, path, own, grp, permissions, ftype):
        """For every file, sends the info to the database"""
        db = database.Worker()
        db.insert_meta(path, own, grp, permissions, ftype)



