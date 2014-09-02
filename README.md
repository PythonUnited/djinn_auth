djinn_auth
===================

Role based auth module for Djinn. The package is also useable as
standalone module, since it has no relation to other djinn packages.

This module build upon the django.contrib.auth module, and extends it
with role based authorisation. Roles can be assigned to a user and a
group.


Global permissions
------------------

You can give a user a permission by:

  1. give the user a role that has this permission
  2. add the user to a group that has a role that has this permission
  3. add the user to a group that has the permission


Object permissions
------------------

You can enable permissions for a given user or group on a specific object by:

  1. giving the user a local role on the object with that permission
  2. giving a group the user is part of a local role with that permission
  3. giving the permission to the user on the object
  4. giving the permission to a group the user is part of on the object

To prevent acquisition of the global permissions on an instance, implement the
'acquire_global_roles' property and return False.
