# confparser.py
#
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

""" Configuration parser. Let's be bold and try to get a better parser
than the Standard Library ConfigParser """

import re

HEADER = re.compile(
r'\['                                 # [
r'(?P<header>[^]]+)'                  # very permissive!
r'\]'                                 # ]
)
OPTION = re.compile(
r'(?P<option>[^:=\s][^:=]*)'          # very permissive!
r'\s*(?P<divider>[:=])\s*'                 # any number of space/tab,
                                      # followed by separator
                                      # (either : or =), followed
                                      # by any # space/tab
r'(?P<value>.*?)(#|$)'                # everything up to eol or a comment
)

class Parse(object):
    """Parses a configuration file"""
    
    def __init__(self,
                 config):
        self.config = open(config)
        
    def options(self):
        """Return a dictionary of values found in the config file"""
        lines = self.config.read()
        values = {}
        for line in lines.split('\n'):
            if line.startswith('#'): # ommit comments
                pass
            elif not line.strip(): # ommit empty lines
                pass
            else:
                #get_header = HEADER.match(line) #don't do anything just yet
                get_options = OPTION.match(line)
                if get_options:
                      optname, optdivider, optvalue = get_options.group('option',
                                                                        'divider',
                                                                        'value')
                      # make sure we have words without trailing space:
                      new_key = optname.split()[0]
                      new_value = optvalue.split()[0]
                      values[new_key] = new_value
        # matches the attributes from the dicionary to the values:
        for (key, value) in values.items():
            # convert string to list if within brackets
            if value.startswith('['):
                list = eval(value)
                setattr(self, key, list)
            else:
                setattr(self, key, value)
         
        

