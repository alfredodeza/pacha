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

import os
from time import strftime

"""All file operations are done here. Usually host related stuff like proper
hosts and setting IP's""" 

class Edit(object):
    """Main class to edit text files."""

    def __init__(self,
            file):
        self.file = file

    def rename(self):
        """Renames a file with a timestamp to give space for the
        new file that is generated from Pacha"""

        # Get the timestamp:
        timestamp = strftime('%m-%d_%H-%M-%S')+'_pacha.renamed'
        renamed_file = self.file+append
        os.rename(self.file, renamed_file)
   
    def replace(self):
        """From the templates, it replaces the data according to what
        we need."""
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
 

