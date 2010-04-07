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
            database = '/opt/pacha/db/pacha.db'):
        self.path = path
        self.database = database

    def walker(self):
        """If we have a directory, walk every file in it"""

        # we need to verify the directory itself first
        dir_meta = Permissions(self.path)
        self.insert(self.path, dir_meta.owner(), dir_meta.group(),
                dir_meta.rwx(), 'dir')

        for root, directories, files in os.walk(self.path):
            # do the directories first:
            for dirs in directories:
                try:
                    absolute = os.path.join(root, dirs)
                    metadata = Permissions(absolute)
                    if os.path.isdir(absolute):
                        own = metadata.owner()
                        grp = metadata.group()
                        permissions = metadata.rwx()
                        self.insert(absolute, own, grp, permissions, 'dir')
                except IOError:
                    pass # we are ok if it does not get recorded

            for f in files:
                try:
                    absolute = os.path.join(root, f)
                    metadata = Permissions(absolute)
                    if os.path.isfile(absolute):
                        own = metadata.owner()
                        grp = metadata.group()
                        permissions = metadata.rwx()
                        self.insert(absolute, own, grp, permissions, 'file')
                except IOError:
                    pass # we are ok if it does not get recorded

    def single_file(self):
        """If we are given a single file we get the information without
        trying to walk the whole tree"""

        if os.path.isfile(self.path):
            metadata = Permissions(self.path)
            own = metadata.owner()
            grp = metadata.group()
            permissions = metadata.rwx()
            self.insert(absolute, own, grp, permissions, 'dir')


    def insert(self, path, own, grp, permissions, ftype):
        """For every file, sends the info to the database"""
        db = database.Worker(self.database)
        db.insert_meta(path, own, grp, permissions, ftype)



