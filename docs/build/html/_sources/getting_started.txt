.. _getting_started:

GettingStarted  
====================

Introduction
--------------
You will be able to quickly get started with this guide. The main goal is to get Pacha installed and running and having you backing up your configuration files. More advanced Pacha functions are not covered here.

Dependencies
-----------------
We have 3 dependencies, make sure you have them installed and ready when installing Pacha:

 *  SSH (versions 4.7p1 to 5.1p1)
 *  Mercurial (versions 0.9.5 to 1.3.1)
 *  Python (version 2.5 to 2.6)

About version differences
----------------------------
You should NOT use Pacha with different versions of Mercurial in different servers otherwise you will get undesired behavior when trying to rebuild a host. This would happen when functionality found in later versions of Mercurial will conflict with the older ones, hence the ability lack of being able to get the latest version of the files you need to rebuild.

Operating Systems
-------------------
Pacha should work with any system that has the above installed. If you experience any issues let us know!

Installation
--------------
We recommend installing from the Python Package Index (PYPI)::

    pip install pacha 

But you can also install from the latest version of Pacha from the http://code.google.com/p/pacha Uncompress the contents::

    hg clone https://pacha.googlecode.com/hg/ pacha 

And run the following within the extracted directory::

    python setup.py install 


After Installation
======================
Remember to edit pacha.conf and run:
pacha --watch /opt/pacha/conf
This will keep track of all host specific configurations that will be needed
when rebuilding.

Edit the configuration file
-------------------------------
After installing you need to edit the config file. Pacha needs to have this edited to be running properly. The config file should be located in: /opt/pacha/conf/pacha.conf

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

So follow that above warning to add a username and avoid the daemon problem.

Master Slave approach
----------------------
Pacha can run as a single instance but we want to accomplish a good configuration backup setup. Master/Slave is what we are going to cover here.

+-----------+------------------------------------------------------------------------------------------+
| ``host``  | Where is the Pacha master server running?. An IP or a FQDN works                         |
+-----------+------------------------------------------------------------------------------------------+
| ``port``  | If you are running a different port other than 22 for SSH, edit this. No need to specify |
|           | if you have not changed the standard port.                                               |
+-----------+------------------------------------------------------------------------------------------+
| ``user``  | The user Pacha will use to connect via SSH                                               |
+-----------+------------------------------------------------------------------------------------------+
| ``path``  | If you are running a different port other than 22 for SSH, edit this. No need to         |
|           | specify if you have not changed the standard port.                                       |
+-----------+------------------------------------------------------------------------------------------+

.. note:: We will not cover the rebuilding process here. Again, the goal is to have Pacha backing up configuration files in this guide.

SSH and Keys
--------------
Pacha is intended to be fully automated so you need to have your ssh keys associated with the user you set in the configuration file so it has read/write access to the location where Pacha is installed.

Tracking Configuration Files
------------------------------
First we need to create a directory where all the configuration files will be pushed. This is the way of "granting permissions" in the Pacha server. So in the master server run:

sudo pacha --add-host hostname
---------------------------------
Replace "hostname" with the name of the machine you want to get configuration files from. NOTE: Pacha will not be able to push files if this is not done!

Pacha uses the --watch option to start tracking a directory. Let's follow the recommendation when we finished installing Pacha. You can either be in the directory and run --watch or specify the path directly::

    pacha --watch /opt/pacha/conf

You are now all set!
