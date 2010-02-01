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
import log

def get():
    """Grab the latest version from code.google.com"""
    # The stable release has to be always in the same spot:
    stable = "https://pacha.googlecode.com/hg/branches/stable"
    command = "hg clone %s /tmp/upgrade" % stable
    log.append(module='upgrade', type='INFO', line="checking out pacha stable")
    call(command, shell=True, stdout=PIPE)

def replace_lib():
    """Replaces all lib and test files"""

def replace_daemon():
    """updates the daemon file"""

def replace_pacha():
    """updates pacha.py"""


def main():

