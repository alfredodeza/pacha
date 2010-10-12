.. _getting_started:

GettingStarted  
====================

Introduction
--------------
The main goal is to get Pacha running and having you backing up your configuration files in as 
little steps as possible. More advanced Pacha functions are not covered here.


.. note::
    The only "dependency" Pacha has is SSH. Make sure you have it installed and running
    (e.g. that you can *ssh* to other machines 



Installation and setup 
------------------------
We recommend installing from the Python Package Index (PYPI)::

    pip install pacha 

Have your SSH keys ready for the machines you want Pacha to talk to.

Even if you plan to keep files in a single server, get your ssh keys for ``localhost``. 
Pacha pushes information **only** via SSH.

If this is a single machine, below is a quick example of getting SSH keys running::

    cd ~/.ssh
    ssh-keygen
    [...]
    cat id_rsa.pub >> authorized_keys

Verify it is working by logging in passwordless::

    ssh localhost

If the above does not work, then Pacha will not work since any and all network communications
are done via SSH. 


Edit the configuration file
-------------------------------
After installing you need to add a configuration file. The config file can be located 
anywhere and can be called whatever you want. For a sample config file see :ref:`configuration`

If no configuration file is added, Pacha complains::
        
     +----------------------------------------------------+
     |                 ** WARNING **                      |
     |                                                    |
     |  You have not set a configuration file for Pacha.  |
     |  To add a configuration file, run:                 |
     |                                                    |
     |    pacha --add-config /path/to/config              |
     |                                                    |
     +----------------------------------------------------+

Once you have a config file, run::

    pacha --add-config /path/to/config

If you want to remove it, you can::

    pacha --remove-config /path/to/config

And if you want to check the values that are being parsed, you can run::

    pacha --config-values

    Configuration file: /Users/alfredo/vpacha/foo/pacha.conf

    log_level      = DEBUG
    ssh_port       = 22  
    hosts_path     = /tmp/pacha/hosts
    host           = localhost
    frequency      = 60  
    master         = True
    log_datefmt    = %H:%M:%S
    ssh_user       = alfredo
    log_format     = %(asctime)s %(levelname)s %(name)s %(message)s
        

Verify username in HGRC
---------------------------
Mercurial needs to know what is the user that is going to make the changes. If you do not supply one the daemon will dye and you will get this error message next time you try to start::

    Pacha searched for a Mercurial username in the $HOME directory
    and /etc/mercurial/hgrc but could not find one.
    Mercurial needs a username provided:
    But no username was supplied (see "hg help config")
    [ui]
         username = Firstname Lastname <firstname.lastname@example.net>
         verbose = True

So follow the above warning to add a username and avoid the daemon problem.

Master Slave approach
----------------------
Pacha can run as a single instance but we want to accomplish a good configuration backup setup. Master/Slave is what we are going to cover here.

+-----------------+------------------------------------------------------------------------------------------+
| ``host``        | Where is the Pacha master server running?. An IP or a FQDN works                         |
+-----------------+------------------------------------------------------------------------------------------+
| ``port``        | If you are running a different port other than 22 for SSH, edit this. No need to specify |
|                 | if you have not changed the standard port.                                               |
+-----------------+------------------------------------------------------------------------------------------+
| ``ssh_user``    | The user Pacha will use to connect via SSH                                               |
+-----------------+------------------------------------------------------------------------------------------+
| ``hosts_path``  | What is the path where the config files will be pushing to. e.g.:                        |
|                 |   ``/opt/hosts``                                                                         |
+-----------------+------------------------------------------------------------------------------------------+

.. note:: 
    We will not cover the rebuilding process here. Again, the goal is to have Pacha backing up configuration files in this guide.

Tracking Configuration Files
------------------------------
First we need to create a directory where all the configuration files will be pushed. 
This is the way of "granting permissions" in the Pacha server. So in the master server run::

    pacha --add-host my_hostname

Replace *my_hostname* with the name of the machine you want to get configuration files from. 

.. note::
    Pacha will not be able to push files if this is not done!

Pacha uses the --watch option to start tracking a directory. You can either be in the directory and run --watch or specify the path directly::

    pacha --watch ~/bar 
    adding foo.txt
    foo.txt
    running ssh alfredo@localhost "/usr/local/bin/hg init /tmp/pacha/hosts/mbp.local/bar"
    running ssh alfredo@localhost "/usr/local/bin/hg -R /tmp/pacha/hosts/mbp.local/bar serve --stdio"
    searching for changes
    1 changesets found
    remote: adding changesets
    remote: adding manifests
    remote: adding file changes
    remote: added 1 changesets with 1 changes to 1 files

Daemon
--------
Although you have configured Pacha and added some files, the daemon process is not running. The daemon will 
help with the *automated* part of using Pacha.

You can start the daemon either in the background or foreground:

Background method (detaches from the terminal)::

    pacha --daemon-start

And in the foreground::

    pacha --daemon-foreground


