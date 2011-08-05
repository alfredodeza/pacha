.. _dont_do_that:

Don't do that!
===============
Some "best practices" that you should keep in mind, that would otherwise would cause you problems.

Permissions
--------------
Pacha needs as much permissions as the files it is reading. That is, if you need to watch stuff inside of ``/root`` 
then you would need to have as much permissions as the ``root`` user.

Mixed Versions
---------------
We are in constant and heavy development, for the most part, that means that Pacha can make some internal changes that 
will not be compatible for older versions.

If you have an environment that runs Pacha, have all the instances running the same version. If you are updating, make 
sure **all** your instances are updated as well.

Mixed Users
---------------
Pacha can run with different users with different permission levels. However, we do not encourage using it as a Master with 
an unpriviliged user. This will cause issues when trying to read files.

We had someone report issues when trying to have a Single instance (Master/Slave in a single server) that would have certain
files owned by ``root`` that would not be able to push to the unpriviliged user.


About Complaints and Feature Requests
---------------------------------------
It is OK to send me (Alfredo Deza) an email, but do not use it as a fast way to make me help you with your issue. The same 
goes to a feature request.

I usually find it annoying to receive those kind of emails when there is an `Issue Tracker <http://code.google.com/p/pacha/issues/entry>`_ 
that works as a feature request tracker.

Use it!
