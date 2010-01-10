# Copyright 2009 Alfredo Deza
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

import confparser

"""Does all the rebuilding work when a host needs to be reconstructed 
with Pacha. Minimal configurations come from pacha.conf and more complex
executions come from the sh folder.
All executions should be done with Super User powers"""

class ExecConfig(object):
    """Reads pacha.conf and executes the values. Usually host related
    settings like hostname, network and users."""
    
    def __init__(self):
        # reads the config file and sets all the options
        self.conf = '/opt/pacha/conf/pacha.conf'
        self.parse = confparser.Parse(self.conf)
        self.parse.options()

    def hostname(self):
        """Gets the hostname from the config file and applies it"""
        if self.parse.hostname:
            print self.parse.hostname

class Sh(object):
    """Executes all the *.sh scripts in the sh folder"""



