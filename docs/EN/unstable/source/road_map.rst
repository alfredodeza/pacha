.. _road_map:

Road Map
========
A short document to describe the ideas for the upcoming release for Pacha.


File transfer
--------------
We divide these actions into 2 sections: deploying and pushing. They have one
thing in common which is a configuration file that helps the deployment.


Configuration
-------------
Needs to be quite simple really. We want to get away from complicated
deployment work-flows similar to other CM engines (e.g. no code).

Something like this would be cool ::

    # IP's or FQDN to scp/rsync to:
    send_to = ['10.0.0.1', '10.0.0.2', '10.0.0.3']

    # The absolute paths paired to their destinations
    paths = {
                '/path/to/source'           : '/path/to/destination',
                '/path/to/source/configs    : '/path/to/source/destination'
                }



deploy command
--------------
Meant for deploy applications that need Capistrano-like functionality with
symbolic links in place and rollback features.


push command
------------
Meant for configuration changes that can be application specific, like making
changes to httpd.conf 


status
------
When any of the commands above explained are run, the tools should be able to
provide the status of the deploy/push. It is bad if we are pushing a change and
adding checksums if we can't verify from the initiator what is going on.

This should prevent the "let me log-in and check" syndrome.
