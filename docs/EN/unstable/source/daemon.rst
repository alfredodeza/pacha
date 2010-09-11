.. _daemon:

Daemonization
===============
Pacha is able to run on the background with the ``--daemon-start`` flag. However, you may want to
do this automatically in your environment.

Here is an example ``INIT`` script that you could use (modify to fit your needs)::

    #! /bin/sh
    ### BEGIN INIT INFO
    # Provides:           pacha
    # Required-Start:     
    # Required-Stop:      
    # Default-Start:      2 3 4 5
    # Default-Stop:       0 1 
    # Short-Description:  Start the pacha daemon.
    ### END INIT INFO
    #
    # Copyright (c) 2010 Alfredo Deza, alfredodeza [at] gmail [dot] com
    # Licence: MIT

    PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
    DAEMON=/usr/bin/pacha
    NAME=pacha
    DESC="Pacha daemon"
    LOGDIR=/var/log/pacha.log

    test -f $DAEMON || exit 0

    case "$1" in
      start)
        $DAEMON --daemon-start
        ;;
      stop)
        $DAEMON --daemon-stop
        ;;
      restart|force-reload)
        $DAEMON --daemon-stop && $DAEMON --daemon-start 
        
        ;;
      *)
        N=/etc/init.d/$NAME
        echo "Usage: $N {start|stop}" >&2
        exit 1
        ;;
    esac

    exit 0


Foreground
------------
The daemon process can also run on the foreground. This will effectively output all information to the 
terminal and the daemon itself will never detach from the console.

Having a ``foreground`` option enables a user to be able to run Pacha with tools such as 
`Supervisor <http://supervisord.org/>`_ where the daemonization process is taken care of.

To exit from the foreground process you can issue a ``KeyboardInterrupt`` by doing ``Ctrl-C``

It is safe to exit from the foreground process that way.

Daemon Status
----------------
A nice way to tell if the Pacha daemon is running, is to issue the ``--daemon-status`` command.
What this does, is to check the *PID* file where the process ID is normally stored. If the file
is not found (this usually is the case when the process is not running) or if the PID that is in a file 
is no longer there a message displays the information about it.

Permissions
--------------
No ``root`` permissions are needed in order to run Pacha processes. However, when you are trying to 
control files that have higher permissions than the user you are trying to run the Pacha daemon with, you
might get into a situation where the daemon can't interact with that file because of lack of permissions.

Try starting the daemon with enough permissions to work with the files you want.
