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

"""Copies all files and directories to the current user home folder."""
import os
import sys
import shutil
from subprocess import call
import log

def main():
    """Create the directory and copy all the files"""
    pacha_dir = '/opt/pacha'
    absolute_pacha = pacha_dir+'/pacha.py'
    executable = '/usr/bin/pacha'
    daemon = pacha_dir+'/lib/daemon/pacha'
    init = '/etc/init.d/'
    pacha_source =  sys.path[0]
    try:
        log.append(module='install', line="Creating pacha dir")
        shutil.copytree(pacha_source, pacha_dir)
        log.append(module='install', line="Copied files to /opt/pacha")
        os.symlink(absolute_pacha, executable)
        log.append(module='install',
                line="Created pacha executable symlink at /usr/bin/pacha")
        command = "chmod a+x %s" % absolute_pacha
        call(command, shell=True)
        log.append(module='install', 
                line="Corrected permissions for pacha executable")
        log.append(module='install', line="Installation completed")
        shutil.copy(daemon, init)
        log.append(module='install', 
            line="copied pacha daemon file to init.d")
        call('/etc/init.d/pacha start', shell=True)
        log.append(module='install', line="started daemon")
        call('update-rc.d pacha defaults', shell=True)
        log.append(module='install', line="run system update-rc.d for pacha in init script")

    except OSError, e:
        if e.errno == 13:
            sys.stderr.write("You need to run with sudo privileges")
            sys.exit(1)
        else:
            sys.stderr.write("%s" % e)

if __name__ == '__main__':
    main()

