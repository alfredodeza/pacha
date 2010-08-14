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
    DAEMON=/opt/pacha/lib/daemon/pachad
    NAME=pacha
    DESC="Pacha daemon"
    LOGDIR=/var/log/pacha.log

    test -f $DAEMON || exit 0

    case "$1" in
      start)
        $DAEMON --start
        ;;
      stop)
        $DAEMON --stop
        ;;
      restart|force-reload)
        $DAEMON --stop && $DAEMON --start 
        
        ;;
      *)
        N=/etc/init.d/$NAME
        echo "Usage: $N {start|stop}" >&2
        exit 1
        ;;
    esac

    exit 0

