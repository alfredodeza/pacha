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

from subprocess import call, PIPE
import shutil
import log


class Replace(object):
    """methods to perform different changes for the upgrade"""

    def __init__(self):
        self.stable = "https://pacha.googlecode.com/hg/branches/stable"
        self.tmp = "/tmp/upgrade"

    def get(self):
        """Grab the latest version from code.google.com"""
        command = "hg clone %s %s" % (self.stable, self.tmp)
        log.append(module='upgrade', type='INFO', line="checking out pacha stable")
        call(command, shell=True, stdout=PIPE)
        log.append(module='upgrade', type='INFO', line="finished cloning for upgrade")

    def lib(self):
        """Replaces all lib and test files"""
        # first move lib
        lib_location = "/opt/pacha/lib"
        lib_destination = "/tmp/lib"
        lib_clone = "/tmp/upgrade/lib"
        shutil.move(lib_location, lib_destination)
        log.append(module='upgrade', type='INFO', line="moved lib to tmp")
        # now we move the new lib into place
        shutil.move(lib_clone, lib_destination)
        log.append(module='upgrade', type='INFO', line="moved new lib into /opt/pacha")


    def daemon(self):
        """updates the daemon file"""
        # move daemon
        daemon_location = "/etc/init.d/pacha"
        daemon_destination = "/tmp/pacha_daemon"
        daemon_clone = "/tmp/upgrade/lib/daemon/pacha"
        shutil.move(daemon_location, daemon_destination)
        log.append(module='upgrade', type='INFO', line="moved daemon to tmp")
        # new daemon goes into place
        shutil.move(daemon_clone, daemon_destination)
        log.append(module='upgrade', type='INFO', line="moved new daemon to init.d")


    def pacha(self):
        """updates pacha.py"""


def main():
    """does the upgrade step by step"""
    # grab the latest
    get()


