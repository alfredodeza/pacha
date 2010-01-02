# Author: Alfredo Deza
# Email: alfredodeza [at] gmail dot com
# License: MIT
# Copyright 2009-2010 Alfredo Deza
#
"""SSH connections and file transfers with limited options like non
standard ports. This is a simple wrapper to suit Pacha."""

from subprocess import call, PIPE
import os
import sys
from time import strftime
import log
import confparser
import host
import log

class Hg(object):
    """Does local commits and pushed to a central Pacha Master location"""

    def __init__(self,
            port = 22,
            host = None,
            user = None,
            path = None
            ):
        self.port = port
        self.host = host
        self.user = user
        self.path = os.path.normpath(path)
        self.dir = os.path.basename(path)
        self.hg_dir = self.path+'/.hg'
        # read the config file once:
        self.conf = '/opt/pacha/conf/pacha.conf'
        self.parse = confparser.Parse(self.conf)
        self.parse.options()

    def commit(self):
        """hg local commits that are needed before a push to a centralized 
        server"""
        #TODO:
        # Automatically detect if a user modified a file to commit and then
        # push the changes
        # For now, the user has to manually commit

    def push(self):
        """Pushes the repository to the centralized Pacha Master server"""

    def hgrc(self):
        """An option to write the default path in hgrc for pushing
        via hg"""
        if self.validate(self.path):
            conf = '/opt/pacha/conf/pacha.conf'
            parse = confparser.Parse(conf)
            parse.options() # get all the options in the config file
            log.append(module='hg', line="parsed options from config file")
            #norm_path = os.path.normpath(path)
            #base_path = os.path.basename(path)
            machine = host.hostname()
            try:
                hgrc = open(self.path+'/.hg/hgrc', 'w')
                hgrc.write('[paths]\n')
                ssh_line = "default = ssh://%s@%s/%s/%s/%s" % (self.parse.user, 
                        self.parse.host, self.parse.path, machine, self.dir)
                hgrc.write(ssh_line)
                hgrc.close()
                log.append(module='hg', line="wrote hgrc in %s" % self.path)

            except Exception, e:
                log.append(module='hg', type='ERROR', line=e)

        else:
            sys.stderr.write("No repository found here: %s" % self.path)

    def clone(self):
        """Clones a given repository to the remote Pacha server"""
        # needs to be called when --watch is passed, runs just one time
        command = "hg clone %s ssh://%s@%s/%s "
        # TODO: need to add trusted USERS in the global .hgrc 
        # maybe even adding root as the trusted user...

    def validate(self):
        """Validates a working HG path"""
        log.append(module='hg', line="validating repository at %s" % self.path)
        if os.path.exists(self.hg_dir):
            log.append(module='hg', 
                    line="hg repository found at %s" % self.path)
            return True
        else:
            log.append(module='hg', type='ERROR',  
                    line="hg repository not found at %s" % self.path)
            return False
