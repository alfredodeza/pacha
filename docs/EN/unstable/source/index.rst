.. pacha documentation master file

pacha's documentation
=================================

.. image:: _static/pacha_light.jpg

Contents:

.. toctree::
   :maxdepth: 2

   getting_started.rst
   introduction.rst
   daemon.rst
   configuration.rst
   rebuilding.rst
   permissions.rst
   testing.rst
   changelog.rst
   dont_do_that.rst 


Next Release
============

Directory Structure
---------------------
Create a file structure. This should be in the Master. If we have a structure
like::

    /opt/pacha/hosts 

Then we would add something like:

Templates::
    /opt/pacha/templates 

Inside templates, applications should be inside a directory and inside a give
template name. For example, if we want to deal with Apache::

    /opt/pacha/templates/apache 

For a "default" tempalte::

    /opt/pacha/templates/apache/default/httpd.conf 
    /opt/pacha/templates/apache/default/ports.conf 

For other type of templates in apache we just add another dir::

    /opt/pacha/templates/apache/production/httpd.conf
    /opt/pacha/templates/apache/production/ports.conf




Scripts::
    /opt/pacha/scripts
    /opt/pacha/scripts/pre 
    /opt/pacha/scripts/post


Nodes::
    /opt/pacha/nodes

Inside Nodes is were all the *action* occurs. Nodes should contain configuration 
files that will orchestrate how a node needs to be configured. For example if
we have srv1 and srv1 that are webservers, we would have ``/opt/pacha/nodes``
like so::
    /opt/pacha/nodes/srv1.conf
    /opt/pacha/nodes/srv2.conf

It should be allowed to have *meta* nodes configured. For example, if we want
srv1 and srv2 to be configured at the same time, we do not want to run them
individually so we go ahead and have a ``srvs.conf`` file that uses both config
files::

    # meta config file for multiple servers
    include_nodes = ['srv1.conf', 'srv2.conf']

Like Python lists, order would be preserved.    




****************************************************************************************************

Configuration Manager
-----------------------
Pacha was designed from the ground up to be a simple way to backup and manage software configuration files from single or multiple server instances across the network.

Written entirely in Python (although you shouldn't care), Pacha's approach is to easily deploy an instance and capture any changes via a version control, giving the System Administrator the ability to rollback and safe guard valid, working configurations and rebuild a host from those same configurations.


Project Name
-------------
Pacha is the quechua word for Land. A nice metaphor for the configuration land that lies in front of the System Administrator!

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


