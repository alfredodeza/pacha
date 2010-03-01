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
import tarfile
import log

class Upgrade(object):
    """Checks the download links available in the project page and decides
    which one is the best option. A few checks are in place to verify
    the latest version is downloaded"""

    def __init__(self,
            url = 'http://code.google.com/p/pacha'):
        self.url = url
        self.daemon_dest = "/tmp/daemon"+strftime("%H%M%S")
        self.lib_dest = "/tmp/lib"+strftime("%H%M%S")
        self.pacha_dest = "/tmp/pacha"+strftime("%H%M%S")

    def get(self):
        """Downloads the latest version of Pacha to the tmp directory"""
        link = self.download_link()[0]
        tar_file = self.url_filename(link)
        dest = '/tmp/%s' % tar_file
        urllib.urlretrieve(link, dest)
        log.append(module='upgrade.get', type='INFO', 
                line="downloaded %s" % link)
        self.uncompress(dest)

    def uncompress(self, file):
        """Given a tar.gz file we uncompress it and return a path"""
        tar_file = tarfile.open(file)
        tar_file.extractall('/tmp/upgrade')
        log.append(module='upgrade.uncompress', type='INFO', 
                line="uncompressed %s" % file)

    def lib(self):
        """Replaces all lib and test files"""
        # first move lib
        lib_location = "/opt/pacha/lib"
        lib_clone = "/tmp/upgrade/pacha/lib"
        shutil.move(lib_location, self.lib_dest)
        log.append(module='upgrade', type='INFO', line="moved lib to tmp")
        # now we move the new lib into place
        shutil.copytree(lib_clone, lib_location)
        log.append(module='upgrade.lib', type='INFO', line="moved new lib into /opt/pacha")

    def daemon(self):
        """updates the init.d file"""
        # move daemon
        daemon_location = "/etc/init.d/pacha"
        daemon_clone = "/tmp/upgrade/pacha/lib/daemon/pacha"
        shutil.move(daemon_location, self.daemon_dest)
        log.append(module='upgrade.daemon', type='INFO', 
                line="moved daemon to tmp")
        # new daemon goes into place
        shutil.move(daemon_clone, daemon_location)
        log.append(module='upgrade.daemon', type='INFO', 
                line="moved new daemon to init.d")

    def pacha(self):
        """updates pacha.py"""
        # move pacha.py out
        pacha_location = "/opt/pacha/pacha.py"
        pacha_clone = "/tmp/upgrade/pacha/pacha.py"
        shutil.move(pacha_location, self.pacha_dest)
        log.append(module='upgrade.pacha', type='INFO', 
                line="moved pacha.py to tmp")
        # new pacha.py into place
        shutil.move(pacha_clone, pacha_location)
        log.append(module='upgrade.pacha', type='INFO', 
                line="moved new pacha.py to /opt/pacha")

    def cleanup(self):
        """After all these downloads and uncmpressions, lets clean up!"""
        try:
            shutil.rmtree('/tmp/pacha')
            log.append(module='upgrade.cleanup', type='INFO', 
                    line="removing /tmp/pacha")
        except OSError, error:
            pass
            log.append(module='upgrade.cleanup', type='ERROR', line="%s" % error)

    def download_link(self):
        """Return a list with the available download links"""
        source = urllib.urlopen(self.url)
        links = []
        for line in source:
            if 'files/pacha-' in line:
                links.append(line.split('"')[1])
        log.append(module='upgrade.download_link', type='INFO', 
            line="links found: %s" % links)
        return links

    def current_version(self):
        """Return the current Pacha version"""
        command = "pacha --version"
        get_version = Popen(command, shell=True, stdout=PIPE)
        # this return is a mouthful...
        return get_version.stdout.readlines()[0].split('\n')[0]

    def url_check(self):
        """Validate a url, returning False is it is not available"""
        try:
            address = urllib.urlopen(self.url)
            return True
        except IOError:
            return False

    def is_number(self, number):
        """Determines if any part of a string is a valid number or not"""
        try:
            float(number)
            return True
        except ValueError:
            return False

    def url_filename(self, url):
        """Return the filename from a url"""
        file = self.url.split('/')[-1]
        return file
        log.append(module='upgrade.url_filename', type='INFO', 
                line="file name to download: %s" % file)

def main():
    """does the upgrade step by step"""
    try:
        up = Upgrade()
        up.get()
        # replace lib, daemon and pacha files
        up.lib()
        up.daemon()
        up.pacha()
        up.cleanup()
    except OSError, error:
        print "Could not complete upgrade:"
        print error

