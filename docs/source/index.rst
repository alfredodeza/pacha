.. pacha documentation master file, created by
   sphinx-quickstart on Fri Aug 13 17:38:26 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pacha's documentation
=================================



Contents:

.. toctree::
   :maxdepth: 2

   getting_started.rst

Configuration Manager
-----------------------
Pacha was designed from the ground up to be a simple way to backup and manage software configuration files from single or multiple server instances across the network.

Written entirely in Python, Pacha's approach is to easily deploy an instance and capture any changes via a version control, giving the System Administrator the ability to rollback and safe guard valid, working configurations and rebuild a host from those same configurations.

Coming next
------------
We have a few changes coming, make sure you check our WorkingOn page to check Pacha's next version features.

Project Name
-------------
Pacha is the quechua word for Land a nice metaphor for the configuration land that lies in front of the System Administrator!

Goals
=======

Don't learn another language
------------------------------
Other configuration frameworks tell you this, but are written in a language like Ruby and require you to extend,modify or adapt this writing Ruby. We don't! It doesn't matter that Pacha is written in Python. You do not need to know Python to make any changes to the software you want to deploy.

Easy learn curve
-----------------------
One main configuration file to manage the package to be installed and one directory where you can place any number of executable shell scripts to extend and modify your deployment according to your needs.

Versioned Configurations
----------------------------
Keep track of any changes done to a configuration file and rollback easily. We use Mercurial as our back-end but you do not need to manage it directly. Pacha can push changes immediately to any number of clients and get instant feedback.

Light
---------
Deploy Pacha as a client, server, or standalone version. Either way, you get an extremely light, low memory tool that can communicate with your configuration files almost instantly.

Extend and Conquer
------------------------
Forget about the "but this tool doesn't do this". We provide a full hook environment to plug in directly into Pacha so you can extend whatever need you have for your deployment.

Security
-----------
Transferring system configuration files, even across a trusted private network is a security risk. Pacha tackles this problem using SSH as the transport protocol. Although this may add a slight complexity to the framework, we encourage security and think this is the best shot for dealing with critical data related to your systems.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

