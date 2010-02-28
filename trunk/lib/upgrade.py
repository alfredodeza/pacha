# Copyright 2009-2010 Alfredo Deza
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Upgrades to the next newest version, replacing files."""

from subprocess import call,Popen, PIPE
from time import strftime
import shutil
import os
import urllib
import log


class Replace(object):
    """methods to perform different changes for the upgrade"""

    def __init__(self):
        self.stable = "https://pacha.googlecode.com/hg/branches/stable"
        self.tmp = "/tmp/upgrade/branches/stable"
        self.daemon_dest = "/tmp/daemon"+strftime("%H%M%S")
        self.lib_dest = "/tmp/lib"+strftime("%H%M%S")
        self.pacha_dest = "/tmp/pacha"+strftime("%H%M%S")

    def get(self):
        """Grab the latest version from code.google.com"""
        command = "hg clone %s /tmp/upgrade" % self.stable
        log.append(module='upgrade', type='INFO', line="checking out pacha stable")
        call(command, shell=True, stdout=PIPE)
        log.append(module='upgrade', type='INFO', line="finished cloning for upgrade")
    
    def lib(self):
        """Replaces all lib and test files"""
        # first move lib
        lib_location = "/opt/pacha/lib"
        lib_clone = "/tmp/upgrade/branches/stable/lib"
        shutil.move(lib_location, self.lib_dest)
        log.append(module='upgrade', type='INFO', line="moved lib to tmp")
        # now we move the new lib into place
        shutil.copytree(lib_clone, lib_location)
        log.append(module='upgrade', type='INFO', line="moved new lib into /opt/pacha")


    def daemon(self):
        """updates the init.d file"""
        # move daemon
        daemon_location = "/etc/init.d/pacha"
        daemon_clone = "/tmp/upgrade/branches/stable/lib/daemon/pacha"
        shutil.move(daemon_location, self.daemon_dest)
        log.append(module='upgrade', type='INFO', line="moved daemon to tmp")
        # new daemon goes into place
        shutil.move(daemon_clone, daemon_location)
        log.append(module='upgrade', type='INFO', line="moved new daemon to init.d")


    def pacha(self):
        """updates pacha.py"""
        # move pacha.py out
        pacha_location = "/opt/pacha/pacha.py"
        pacha_clone = "/tmp/upgrade/branches/stable/pacha.py"
        shutil.move(pacha_location, self.pacha_dest)
        log.append(module='upgrade', type='INFO', line="moved pacha.py to tmp")
        # new pacha.py into place
        shutil.move(pacha_clone, pacha_location)
        log.append(module='upgrade', type='INFO', line="moved new pacha.py to /opt/pacha")

    def cleanup(self):
        """All files should be cleaned even if something fails"""
        # remove upgrade dir
        shutil.rmtree("/tmp/upgrade")
        log.append(module='upgrade', type='INFO', line="removing the tmp files in /tmp/upgrade")

def download_link(url='http://code.google.com/p/pacha'):
    """Return a list with the available download links"""
    source = urllib.urlopen(url)
    links = []
    for line in source:
        if 'files/pacha-' in line:
            links.append(line.split('"')[1])
    return links

def current_version():
    """Return the current Pacha version"""
    command = "pacha --version"
    get_version = Popen(command, shell=True, stdout=PIPE)
    # this return is a mouthful...
    return get_version.stdout.readlines()[0].split('\n')[0]

def url_check(url):
    """Validate a url, returning False is it is not available"""
    try:
        address = urllib.urlopen(url)
        return True
    except IOError:
        return False

def is_number(number):
    """Determines if any part of a string is a valid number or not"""
    try:
        float(number)
        return True
    except ValueError:
        return False

def url_filename(url):
    """Return the filename from a url"""
    file = url.split('/')[-1]
    return file

def main():
    """does the upgrade step by step"""
    try:
        # grab the latest
        upgrade = Replace()
        upgrade.get()
        # replace lib, daemon and pacha files
        upgrade.lib()
        upgrade.daemon()
        upgrade.pacha()
        # cleanup
        upgrade.cleanup()
    except OSError, error:
        print "Could not complete upgrade:"
        print error



