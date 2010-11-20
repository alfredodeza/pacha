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
    pacha.master = True

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

