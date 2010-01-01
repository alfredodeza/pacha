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

    def push(self):
        """Pushes the repository to the centralized Pacha Master server"""
        command = "scp -P%s ~/.cuy/keys/%s_%s.keys %s@%s:~/.ssh/authorized_keys" % (
                self.port, self.user, self.host, self.user, self.host)
        try: 
            call(command, shell=True, stdout=PIPE, stderr=PIPE)
        except Exception:
            print Exception
