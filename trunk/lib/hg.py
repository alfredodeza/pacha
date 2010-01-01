# Author: Alfredo Deza
# Email: alfredodeza [at] gmail dot com
# License: MIT
# Copyright 2009-2010 Alfredo Deza
#
"""SSH connections and file transfers with limited options like non
standard ports. This is a simple wrapper to suit Pacha."""

from subprocess import call, PIPE
import os
from time import strftime
import log
import confparser
import host

class Hg(object):
    """Does local commits and pushed to a central Pacha Master location"""

    def __init__(self,
            port = 22,
            host = None,
            user = None,
            dir = None
            ):
        self.port = port
        self.host = host
        self.user = user
        self.dir = dir

    def commit(self):
        """hg local commits that are needed before a push to a centralized 
        server"""
        #TODO:
        # Automatically detect if a user modified a file to commit and then
        # push the changes
        # For now, the user has to manually commit

    def push(self):
        """Pushes the repository to the centralized Pacha Master server"""
        command = "scp -P%s ~/.cuy/keys/%s_%s.keys %s@%s:~/.ssh/authorized_keys" % (
                self.port, self.user, self.host, self.user, self.host)
        try: 
            call(command, shell=True, stdout=PIPE, stderr=PIPE)
        except Exception:
            print Exception

    def hgrc(self, path):
        """An option to write the default path in hgrc for pushing
        via hg"""
        conf = '/opt/pacha/conf/pacha.conf'
        parse = confparser.Parse(conf)
        parse.options() # get all the options in the config file
        norm_path = os.path.normpath(path)
        base_path = os.path.basename(path)
        machine = host.hostname()
        #hgrc = norm_path+'/.hg/hgrc'
        try:

            hgrc = open(norm_path+'/.hg/hgrc', 'w')
            hgrc.write('[paths]\n')
            ssh_line = "default = ssh://%s@%s/%s/%s/%s" % (parse.user, parse.host,
                       parse.path, machine, base_path)
            hgrc.write(ssh_line)
            hgrc.close()

        except Exception, e:
            print e


        
