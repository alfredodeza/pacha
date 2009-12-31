# Author: Alfredo Deza
# Email: alfredodeza [at] gmail dot com
# License: MIT
# Copyright 2009-2010 Alfredo Deza
#
"""Copies all files and directories to the current user home folder."""
import os
import shutil
from subprocess import call
import database

def main():
    """Create the directory and copy all the files"""
    pacha_dir = '/opt/pacha'
    try:
        #    print "Installing CUY..."
        shutil.copytree(cwd_abs, cuy_dir)
        #print "copied files to: %s" % cuy_dir
        absolute_cuy = cuy_dir+'/cuy.py'
        executable = '/usr/bin/cuy'
        os.symlink(absolute_cuy, executable)
        #print "created symlink at: %s" % executable
        #Initialize the database
        db = database.Worker()
        #print "initialized the database"


    except OSError, e:
        if e.errno == 13:
            print "You need to run with sudo privileges"
        if e.errno == 17:
            pass
        else:
            print e

    finally:
        # Get correct permissions
        user = os.getlogin()
        command = "chown -R %s:%s %s" % (user,user,cuy_dir)
        call(command, shell=True)
        print "checked correct permissions in install directory"
        print "install done!"
