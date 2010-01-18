# Copyright 2009 Alfredo Deza
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

import confparser
import os
from time import strftime
from subprocess import call, Popen, PIPE
import shutil
import confparser, log

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
5. A dir will be created: /opt/pacha/old_host to move all files that will be 
replaced
6. The config will say what files need to be replaced and copied from /tmp/
to final location.
7. A reboot it is strongly suggested, and printed.

"""

class Rebuild(object):
    """ """
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
            log.append(module='rebuild', line=line_out)

    def install(self):
        conf = '/tmp/%s/conf/pacha.conf' % self.hostname
        parse = confparser.Parse(conf)
        parse.options()
        try:
            packages = parse.packages
        except AttributeError:
            sys.stderr.write(AttributeError)
            sys.exit(1)
        for package in packages:
            command = "sudo apt-get -y install %s" % package
            call(command, shell=True)

    def specific_tracking(self):
        """You can specify specific files to be rebuilt to avoid replacing
        whole directories. Mercurial can't keep track of single files."""
        conf = '/tmp/%s/conf/pacha.conf' % self.hostname
        parse = confparser.Parse(conf)
        parse.options()
        #check if the config has dirs we have in tmp:
        for dirname in self.tracked():
            # we check the dirs in tmp and then get attributes if any
            if hasattr(parse, dirname):
                # now be build the paths and move stuff
                for file in getattr(parse, dirname):
                    default_path = "/%s/%s" % (dirname, file)
                    shutil.move(default_path, default_path+'.old')
                    replacer = '/tmp/%s/%s/%s' % (self.hostname, 
                            dirname, file)
                    shutil.move(replacer, default_path)


    def tracked(self):
        """There needs to be a comparison between the copied files and the
        files that are in the config file. If they are being tracked but
        nothing is specified in the config the whole directory is moved."""
        ls = os.listdir('/tmp/%s' % self.hostname)
        return ls


class ExecConfig(object):
    """Reads pacha.conf and executes the values. Usually host related
    settings like hostname, network and users."""
    
    def __init__(self):
        # reads the config file and sets all the options
        self.conf = '/opt/pacha/conf/pacha.conf'
        self.parse = confparser.Parse(self.conf)
        self.parse.options()


    def pacha_server(self):
        """Determines where Pacha is located"""
        try:
            host =  self.parse.host
            
        except AttributeError:
            log.append(module='rebuild', type='WARN',
            line='no host defined in pacha.conf')


