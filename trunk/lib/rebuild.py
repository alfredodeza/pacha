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

import os
import sys
from subprocess import call, Popen, PIPE
import shutil
import confparser, log


class Rebuild(object):
    """Does all the rebuilding work when a host needs to be reconstructed 
    with Pacha. Minimal configurations come from pacha.conf and more complex
    executions come from the sh folder.
    All executions should be done with Super User powers.

    ### WORKFLOW ###
    1. Install Pacha on new machine
    2. run `pacha --rebuild` and answer the prompts:
        pacha server:
        pacha server user:
        machine to rebuild (hostname):
    3. This will scp all the files from the pacha server to /tmp/pacha
    4. Pacha will read the config and install packages
    replaced
    6. The config will say what files need to be replaced and copied from /tmp/
    to final location.
    7. A reboot it is strongly suggested, and printed."""

    def __init__(self):
        self.server = raw_input("pacha server (IP or FQDN): ")
        self.server_user = raw_input("pacha server username: ")
        self.hostname = raw_input("machine to rebuild (hostname): ")

    def retrieve_files(self):
        """scp all the files we need to /tmp/pacha"""
        command = "scp -r %s@%s:/opt/pacha/hosts/%s /tmp/" % (self.server_user,
                self.server, self.hostname)
        run = Popen(command, shell=True, stdout=PIPE)
        for line_out in run.stdout.readlines():
            log.append(module='rebuild', line=line_out.strip('\n')[0])

    def install(self):
        """Reads the config and install via apt-get any packages that have to 
        be in form of a list"""
        conf = '/tmp/%s/conf/pacha.conf' % self.hostname
        parse = confparser.Parse(conf)
        parse.options()
        try:
            packages = parse.packages
            for package in packages:
                log.append(module='rebuild', line="installing %s" % package)
                command = "sudo apt-get -y install %s" % package
                call(command, shell=True)
        except AttributeError, e:
            log.append(module='rebuild', type='ERROR', line="%s" % e)
            sys.stderr.write("No packages specified for installation in config")
            sys.exit(1)

    def specific_tracking(self):
        """You can specify specific files to be rebuilt to avoid replacing
        whole directories. Mercurial can't keep track of single files."""
        conf = '/tmp/%s/conf/pacha.conf' % self.hostname
        parse = confparser.Parse(conf)
        parse.options()
        log.append(module='rebuild', line="read config file and parsed options")
        #check if the config has dirs we have in tmp:
        for dirname in self.tracked():
            # we check the dirs in tmp and then get attributes if any
            if hasattr(parse, dirname):
                log.append(module='rebuild', 
                        line="found dirs that have specific config")
                # now be build the paths and move stuff
                for item in getattr(parse, dirname):
                    default_path = "/%s/%s" % (dirname, item)
                    shutil.move(default_path, default_path+'.old')
                    log.append(module='rebuild', 
                            line="moving %s to %s" % (default_path, 
                            default_path+'.old'))
                    replacer = '/tmp/%s/%s/%s' % (self.hostname, 
                            dirname, item)
                    shutil.move(replacer, default_path)
                    log.append(module='rebuild', 
                            line="moving %s to %s" % (replacer, default_path))


    def tracked(self):
        """There needs to be a comparison between the copied files and the
        files that are in the config file. If they are being tracked but
        nothing is specified in the config the whole directory is moved."""
        list_files = os.listdir('/tmp/%s' % self.hostname)
        return list_files

