# Author: Alfredo Deza
# Email: alfredodeza [at] gmail dot com
# License: MIT
# Copyright 2009-2010 Alfredo Deza
#
"""Removes all installation files"""
import os
import shutil
import log

def main():
    pacha_dir = '/opt/pacha'
    log.append(module='uninstall', line="removing pacha dir at /opt/pacha")
    
    try:
        shutil.rmtree(pacha_dir)
        os.remove('/usr/bin/pacha')
        log.append(module='uninstall', line="destroyed symlink")
    except OSError,e:
        log.append(module='uninstall', type='ERROR',
                line=e)
       

