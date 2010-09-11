.. _configuration:

Configuration
=================
Pacha has some defaults and some needed configuration. Since an automatic
push of data needs to happen every time a configuration change is done, it needs
to know about where it can push that data.

Config File
----------------
Below is how a configuration file for Pacha would look like with default values::

    [DEFAULT]
    # Pacha onfiguration file

    ###################################
    # Pacha Server Configuration
    ###################################

    # Frequency check in seconds. Add a number to the frequency Pacha
    # should check for different revision numbers. Do not add anything
    # lower than 10 seconds. By default Pacha runs every 60 seconds
    pacha.frequency = 60

    # Tell Pacha if this machine is a Master Pacha Server
    # It will default to False
    pacha.master = False

    # Pacha master server (if using the standalone version, you still need
    # to edit this). Values can be IP's or FQDN:
    pacha.host = localhost

    # Change the SSH port if the master is not running a
    # standard (22) port:
    pacha.ssh.port = 22

    # Username for the SSH connection:
    pacha.ssh.user = root

    # Path for the hosts config file directory
    # usually in /opt/pacha/hosts
    # Pacha will use this path to either store the configurations locally
    # (if this is set as a Master server) or the remote path where
    # Pacha will push its files
    pacha.hosts.path = /opt/pacha/hosts

    # HG Autocorrect will try to match changes in the config with 
    # hgrc mismatches
    pacha.hg.autocorrect = True

    # Logging Stuff
    # Set this to True and add a log_path to enable logging 
    pacha.log.enable = False

    # this can be a file path or a directory path 
    pacha.log.path = None
    
    # Below options set Logging formatting
    pacha.log.format = %(asctime)s %(levelname)s %(name)s %(message)s
    pacha.log.datefmt = %H:%M:S


Defaults
-------------
All the values that you see in the above example configuration file are just the default ones. If nothing is set, Pacha will enable default values and will try to run with those.


Config File Gone
-----------------
When a configuration file that was previously added is no longer present (or Pacha is unable to access it) a
warning message will display alerting of this.
This is useful because since Pacha tries to get values and feeds defaults to the ones it can't find, it can
be tricky to spot if you are reading default values or not.

This is how the warning message should look in the command line prompt::

    +-----------------------------------------------------+
    |                   ** WARNING **                     |
    |                                                     |
    |  The config file supplied does not exist. Try       |
    |  adding a new valid path by running:                |
    |                                                     |      
    |    pacha --add-config /path/to/config               |
    |                                                     | 
    +-----------------------------------------------------+

Logging Configuration
-----------------------
Starting on version 0.2.4, you need to add some specifics to logging to be able to have it play
nicely with Pacha.

You have 4 options to control logging but 2 that are absolutely needed in order to have logging 
working::

    # Both needed to enable logging 
    pacha.log.enable = False
    pacha.log.path = None
    
    # Optional logging configuration 
    pacha.log.format = %(asctime)s %(levelname)s %(name)s %(message)s
    pacha.log.datefmt = %H:%M:S


The reason behind ``pacha.log.enable`` is that we wanted to give more control to turn on or off 
logging even if you have the ``pacha.log.path`` option set.

Pacha *needs* to log to a file, so adding a log path is also required. 

The logging path should be absolute and it can be in the form of a directory or a file.

If a directory is given (e.g: ``pacha.log.path = '/var/log'``) Then the log file would be created
with this full path::

    /var/log/pacha.log 

However, you might not want that name for your log file. If you want something else you can pass 
that information as a full path to that file (e.g: ``pacha.log.path = '/home/alfredo/my_daemon.log'``)
And in that case the logging module would accept that as a valid path and there would not be any 
path modification.


HG Autocorrect
----------------
There are sometimes where Pacha might be running and watching some files and directories with a 
``.hgrc`` configuration that points to a ssh connection, user and host like::

    default = ssh://alfredo@localhost//opt/pacha/hosts/mbp.local/foo 

What happens if one day you change your ``pacha.ssh.user`` in your config to something else?

Pacha will no longer be able to push correctly when a change is found. Here is where the autocorrect 
option comes in to play.

By default is set to ``True`` and will check what you have in the ``.hgrc`` file and rewrite it 
if a mismatch is found to mirror your changes in the Pacha config file.


