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
            print "Stopped daemon"
            os.remove('/etc/init.d/pacha')
        print "Destroyed pacha daemon symlink"
        if os.path.isdir(pacha_dir):
            shutil.rmtree(pacha_dir)
            print "Removed /opt/pacha"
        os.remove('/usr/bin/pacha')
        print "Destroyed symlink"
        
    except OSError,e:
        print e
       
if __name__ == '__main__':
    main()
                
