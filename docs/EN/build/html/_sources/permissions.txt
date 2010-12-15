.. _permissions:

Permissions
=============
Pacha tracks all permissions related to files and directories that it tracks. This is 
where the tool starts to separate from the versioning engine. 

Usually, DVCS (Distributed Versioning Control Systems) do not track permissions, but 
since Pacha is able to rebuild hosts, it needed to be able to track granular permissions 
on files **and** directories.

What is tracked
-----------------
When you issue a ``--watch`` or ``--watch-single`` command option Pacha not only versions, 
commits, and pushes the files, but it also adds every bit of permissions related to every 
single file.

rwx
------
We track the sticky bit, what are the ``rwx`` permissions related 
to the owner, group and everyone else. This would allow us to match **exactly**
the original permissions regardless of what changed when the files moved or where 
handled by the DVCS.

Ownership
----------
Files and directories can have an owner and a group owner. In this case we track both.

So if a file is owned by ``root`` and the group owner is ``admins``, at the time of rebuilding 
both should be "applied" to the file. 

When it might not work
--------------------------
There are certain ocassions where tracking or setting permissions might not work correctly. There 
are basically 2 scenarios where this would happen:

 * Insuficcient rights to read the permissions 
 * ``user`` or ``group`` does not exist in the host when rebuilding. 

 The first scenario is simple, you try to watch a directory that is owned by a user that has a higher 
 level of permissions and doesn't allow you to properly read the files. Usually, Pacha would tell 
 you it couldn't read and version the files correctly, but in certain cases you might be allowed to 
 push the files but not the metadata associated with them.

 The second case, would happen when rebuilding a host. If host-1 has a bunch of tracked files owned by 
 ``admin-one`` and group owned by ``group-one`` and you try to rebuild a host where both the user and group 
 do not exist, then Pacha would simply skip setting the permissions.

 If in that host, by some reason you had ``admin-two`` and ``group-two`` the ownership would still not be 
 able to be applied. 

 A way around this problem would be to use the **pre** and **post** hooks provided with Pacha.
