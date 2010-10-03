import logging
import pwd
import grp
import os
import stat
from pacha.database     import Worker 
from pacha.util         import get_db_file

DB_FILE = get_db_file()
rwx_log = logging.getLogger('pacha.permissions')

class Permissions(object):
    """Gathers the exact metadata we need for every file or given
    directory, like owner, group ownership and the octogonal 
    representation of RWX-RWX-RWX type permissions"""

    def __init__(self, 
            path):
        self.path = path
        self.stat = os.stat(self.path)
        self.uid = self.stat.st_uid
        self.gid = self.stat.st_gid

    def owner(self):
        """Return the owner of a given file or directory"""
        owner = pwd.getpwuid(self.uid)[0]
        return owner

    def group(self):
        """Return the group of a give file or directory"""
        group = grp.getgrgid(self.gid)[0]
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
            database = DB_FILE):
        self.path = path
        self.database = database

    def walker(self):
        """If we have a directory, walk every file in it"""

        # we need the directory itself first
        dir_meta = Permissions(self.path)
        self.insert(self.path, dir_meta.owner(), dir_meta.group(),
                dir_meta.rwx(), 'dir')
        rwx_log.debug("%s has %s %s %s" % (self.path, dir_meta.owner(),
            dir_meta.group(), dir_meta.rwx()))
        rwx_log.debug("directory stat inserted into database")

        for root, directories, files in os.walk(self.path):
            # do the directories first:
            for dirs in directories:
                try:
                    absolute = os.path.join(root, dirs)
                    metadata = Permissions(absolute)
                    rwx_log.debug("stat on subdir %s" % absolute)
                    if os.path.isdir(absolute):
                        own = metadata.owner()
                        grp = metadata.group()
                        permissions = metadata.rwx()
                        self.insert(absolute, own, grp, permissions, 'dir')
                except IOError, error:
                    rwx_log.error("grabbing permissions on dir %s" % self.path) 
                    rwx_log.error(error)

            for f in files:
                try:
                    absolute = os.path.join(root, f)
                    metadata = Permissions(absolute)
                    rwx_log.debug("stat on subdir %s" % absolute)
                    if os.path.isfile(absolute):
                        own = metadata.owner()
                        grp = metadata.group()
                        permissions = metadata.rwx()
                        self.insert(absolute, own, grp, permissions, 'file')
                except IOError:
                    rwx_log.error("grabbing permissions on file %s" % self.path) 
                    rwx_log.error(error)

    def single_file(self):
        """If we are given a single file we get the information without
        trying to walk the whole tree"""

        if os.path.isfile(self.path):
            rwx_log.debug("single file metadata for %s" % self.path)
            metadata = Permissions(self.path)
            own = metadata.owner()
            grp = metadata.group()
            permissions = metadata.rwx()
            self.insert(self.path, own, grp, permissions, 'dir')


    def insert(self, path, own, grp, permissions, ftype):
        """For every file, sends the info to the database"""
        db = Worker(self.database)
        db.insert_meta(path, own, grp, permissions, ftype)
        rwx_log.debug("inserting path to database: %s" % path)



