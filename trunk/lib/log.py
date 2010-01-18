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
"""Handles all logging for Pacha. Not using Python's logging module
knowlingly."""

import os
import sys
from time import strftime

def append(module='pacha', type='INFO', line=''):
    """Simple function to write to a log file"""

    log_file = '/var/log/pacha.log'
    try:
        if os.path.isfile(log_file):
            open_log = open(log_file, 'a')
        else:
            open_log = open(log_file, 'w')

        timestamp = strftime('%b %d %H:%M:%S')
        log_line = "%s %s %s %s" % (timestamp, type, module, line)
        open_log.write(log_line+'\n')
        open_log.close()

    except IOError:
        sys.stderr.write("Permission denied to write log file ")
        sys.exit(1)




