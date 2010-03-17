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
#
"""Removes all installation files"""
import os
import shutil
import log
from subprocess import call

def main():
    pacha_dir = '/opt/pacha'
    print "Removing pacha dir at /opt/pacha"
    
    try:
        if os.path.isfile('/etc/init.d/pacha'):
            call('/etc/init.d/pacha stop', shell=True)
            print "Stopped daemon")
            os.remove('/etc/init.d/pacha')
        print "Destroyed pacha daemon symlink")
        if os.path.isdir(pacha_dir):
            shutil.rmtree(pacha_dir)
            print "Removed /opt/pacha")
        os.remove('/usr/bin/pacha')
        print "Destroyed symlink")
        
    except OSError,e:
        print e
       
if __name__ == '__main__':
    main()
                
