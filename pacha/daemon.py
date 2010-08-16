#!/usr/bin/env python
#
# Copyright 2009-2010 Alfredo Deza
# Pacha Daemon

import os
import sys
import time
from getpass import getuser
from optparse import OptionParser
from subprocess import Popen, PIPE
import supay
from pacha import log, hg, database
from pacha.config_options import config_defaults

class Watcher(object):
    """Handles all the Reports to display"""
 
    def __init__(self,
                 path=None):
        self.path = os.path.normpath(path)
 
    def report(self):
        """Report if a file changed and the change has not been commited"""
        log.append(module='pachad', 
                line='watching for changes in %s' % self.path)
        run = Runners(location=self.path)
        if run.modified() is True:
            mercurial = hg.Hg(path=self.path)
            mercurial.commit()
            mercurial.push()

    def revision_compare(self, path, rev):
        """Conect to the database for revision comparison
        and insert a revision hash from Mercurial if it 
        does not exist"""
        run = Runners(location=self.path)
        if rev == None:  #a path without a revision so insert one
            log.append(module='pachad.Watcher.revision_compare',
                    line='No revision recorded in DB - so adding it')
            revision = run.hg_revision()[0]
            db = database.Worker()
            db.update_rev(self.path, revision)
            log.append(module='pachad.Watcher.revision_compare',
                    line='added revision %s for path %s' % (revision,
                        self.path))
        else: # we have a hash there so:
            revision = run.hg_revision()[0]
            if rev != revision:
                log.append(module='pachad.Watcher.revision_compare',
                        line='found a new revision: %s at %s' % (rev,
                        self.path))
                mercurial = hg.Hg(path=self.path)
                mercurial.push()
                db = database.Worker()
                db.update_rev(self.path, revision) 

class Runners(object):
    """Handles everything related to Mercurial calls"""
 
    def __init__(self, location=None):
        self.location = location
        os.chdir(location) # change directory (HG bug)

    def hg_revision(self):
        """Gets the revision ID from the path"""
        changeset = run_command(std="stdout", cmd="hg head")[0]
        return changeset[-13:].split('\n')

    def modified(self):
        """Checks if a file has been modified and not commited"""
        out = run_command(std="stdout", cmd="hg st")
        for line in out:
            file_name = line[2:].split('\n')[0] # get a nice file name
            if line.startswith('M'):
                log.append(module='pachad', 
                        line='found modified file: %s' % file_name)
                return True
            else:
                return False
                log.append(module='pachad', 
                        line='no changes with: %s' % file_name)

def run_command(std, cmd):
    """Runs a command via Popen"""
    if std == "stderr":
        run = Popen(cmd, shell=True, stderr=PIPE)
        out = run.stderr.readlines()
    if std == "stdout":
        run = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out = run.stdout.readlines()
    return out

def check_path(file_path):
    """We need to always return a path that ends with a directory """ 
    if os.path.isdir(file_path):
        return file_path
    else:
        return os.path.dirname(file_path)

def start(config):
    daemon = supay.Daemon(name='pacha', log=False, pid_dir=os.path.dirname(__file__))
    daemon.start()
    log.append(module='pachad', line='Daemon started')

    while True:
        try:
            db = database.Worker()
            repos = []
            for i in db.get_repos():
                repos.append(i)
            db.closedb()
            #log.append(module='pachad', line='reading repos from database')
            #pacha_conf = confparser.Parse(config='/opt/pacha/conf/pacha.conf')
            #log.append(module='pachad', line='reading pacha.conf')
            #pacha_conf.options()
            # frequency check:
            try:
                freq = int(config['frequency'])
                if freq < 10:
                    freq = 60
            except ValueError: # if we do not get a number
                freq = 60
            except AttributeError:
                freq = 60
            try:
                master = config['master']
               # log.append(module='pachad.main', type='INFO',
               #         line='machine set to master')
                if master == 'True':
                    hg.update()
            except AttributeError, error:
                # it is ok if this setting is not ON
                # but annoying if you see this INFO all over
                # your log files, so nothing to see here
                pass
#                log.append(module='pachad.main', line='looping over repos in db')
            for repo in repos:
                # need to get an abspath from 'repo' and then pass it on
                # else the daemon will error out
                repo_path = check_path(repo[1])
                if os.path.exists(repo_path): # catches a path no longer there...
                    watch = Watcher(path=repo_path)
                    watch.report()
                    watch.revision_compare(path=repo_path, rev=repo[4])
                else:
                    pass # TODO Add logging
                    #log.append(module='pachad', 
                     #type='WARN', line='path %s does not exist' % repo_path)
            time.sleep(freq)
        except Exception, error:
#                log.append(module='pachad', type='ERROR', 
#                    line='Fatal Exception - daemon killed')
#                log.append(module='pachad', type='ERROR',
#                    line='%s' % error)
            sys.exit(1)

def stop():
    daemon = supay.Daemon(name='pacha', log=False, pid_dir=os.path.dirname(__file__))
    daemon.stop()
    log.append(module='pachad', line='Daemon stopped')

