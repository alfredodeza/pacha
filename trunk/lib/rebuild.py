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
import os
from time import strftime

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
        try:
            hostname =  self.parse.hostname

            
        except AttributeError:
            log.append(module='rebuild', type='WARN',
            line='no hostname defined in pacha.conf')

class Sh(object):
    """Executes all the *.sh scripts in the sh folder"""

def file_operations(filename, content):
    """Simple function to move a config file and write a new one, Pacha
    powered"""
    # First we rename the file with a timestamp:
    append = strftime('%m-%d_%H-%M-%S')+'_pacha.renamed'
    old_file = filename+append
    os.rename(filename, old_file)
    # Now we write the new content:
    new_file = open(filename, 'w')
    new_file.write(content)
    new_file.close()


   
    def remove(self, user):
        """Matches a user and deletes it"""
        key_file = open(self.key)
        data = []
        for line in key_file.readlines():
            if user in line:
                pass
            else:
                data.append(line)
        key_file.close()
        rewrite = open(self.key, 'w')
        for key in data:
            rewrite.write(key)
 

