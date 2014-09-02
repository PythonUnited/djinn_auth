djinn_auth
==========

Role based auth module for Djinn. The package is also usable as
standalone module, since it has no relation to other djinn packages.

This module builds upon the django.contrib.auth module, and extends it
with role based authorisation, both global roles and local roles (or:
roles on a specific model instance). Roles can be assigned to a user
and a group.

For (un)assignments you can use the API specified in
djinn_auth.utils. This provides functions to assign roles to
users/groups globally and locally, and to check on global and local
roles.  Specific checks enable you to check whether a user has a role,
either directly or through one of it's groups.

Note that while this module is agnostic of the specific User model
(since this is a swappable model), it will assume at least the
existence of the user_permissions relation.


Global permissions
------------------

Global permissions provide a means of granting permissions to a user
or group globally. This means that a check on a local permission on a
given model instance, will also return the global permissions.

You can give a user a permission by:

  1. give the user a permission through the User.user_permissions attribute
  2. give the user a role that has this permission
  3. add the user to a group that has a role that has this permission
  4. add the user to a group that has the permission


Local permissions
-----------------

You can enable permissions for a given user or group on a specific
model instance by:

  1. giving the user a local role on the object with that permission
  2. giving a group the user is part of a local role with that permission
  3. giving the permission to the user on the object
  4. giving the permission to a group the user is part of on the object

To prevent acquisition of the global permissions on an instance,
implement the 'acquire_global_roles' property and return False. This
enables the scenario where users have a global 'allow', but some local
'forbiddens'. Please note that this only disallows global _roles_, not
direct permissions on the user or it's groups itself.
