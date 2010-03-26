"""Will attempt to get the owner and permissions of a file to be able to 
set them correctly when rebuilding"""

import pwd
import grp
import os

class Permissions(object):

    def __init__(self, 
            path):
        self.path = path
        self.stat = os.stat(self.path)

    def owner(self):
        """Return the owner of a given file or directory"""
        info = self.stat.st_uid
        owner = pwd.getpwuid(info)[0]
        return owner

    def group(self):
        """Return the group of a give file or directory"""
        info = self.stat.st_gid
        group = grp.getgrgid(info)[0]
        return group

