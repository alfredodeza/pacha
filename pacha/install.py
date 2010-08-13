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
        shutil.copytree(pacha_source, pacha_dir)
        log.append(module='install', line="Creating pacha dir")
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

