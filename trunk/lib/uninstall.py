# Author: Alfredo Deza
# Email: alfredodeza [at] gmail dot com
# License: MIT
# Copyright 2009-2010 Alfredo Deza
#
"""Removes all installation files"""
import os
import shutil

def main():
    home = os.environ.get('HOME')
    cuy_dir = home+'/.cuy'
    print "Removing Cuy install dir: %s" % cuy_dir
    try:
        shutil.rmtree(cuy_dir)
        os.remove('/usr/bin/cuy')
        print "Destroyed symlink"
    except OSError,e:
        print e

