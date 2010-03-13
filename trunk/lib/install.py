#Copyright (c) 2009-2010 Alfredo Deza <alfredodeza [at] gmail [dot] com>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.




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

