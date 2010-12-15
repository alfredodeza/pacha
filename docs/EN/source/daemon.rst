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


Foreground
-----------
Sometimes you do not need to run the daemon in the background, but rather, see what is going on as you go.

Pacha has a ``--daemon-foreground`` option that lets you do just that. It will run in the foreground  and will 
not exit unless you send a ``KeyboardInterrupt`` (Ctrl-C in most cases).


Run Once
----------
Another option to deal with daemonization is if you do not really care for a daemon to be always in the background.
To avoid this issue, we provide an option that will run all the tasks once and will exit safely at the end.
The option ``daemon-run-once`` will accomplish this and it is really convenient if you want to call pacha via ``cron``
and set up a cron job that can take care of running.

Sometimes, setting up cron and calling pacha is easier than dealing with annoying daemonizing processes from the OS.
