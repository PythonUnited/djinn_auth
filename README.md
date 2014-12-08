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
implement the `acquire_global_roles` property and return False. This
enables the scenario where users have a global 'allow', but some local
'forbiddens'. Please note that this only disallows global _roles_, not
direct permissions on the user or it's groups itself.

If you need to add some sort of hierarchy, you may do so using the
`acquire_from` attribute on your instance, that must return a list of
instances it wishes to obtain roles/permissions from.


Installation
------------

Install the usual way using _pip_ or _easy\_install_. Add djinn\_auth
to your INSTALLED\_APPS. Add the djinn\_auth backend to the
AUTHENTICATION\_BACKENDS setting:

    AUTHENTICATION_BACKENDS = (
      'django.contrib.auth.backends.ModelBackend',
      'djinn_auth.authbackend.AuthBackend'
      )


Usage
-----

Basic use of the djinn\_auth module is not different from using the
builtin Django authorisation. You can use the same decorators or
calls, since djinn\_auth adds it's own backend to the autorisation
chain. Following, are some simpe cases. Check the utils.py file for
the full API. Yes, you will need to read Python code..!

Create a role and add permissions:

    from djinn_auth.models import Role
    from django.contrib.auth.models import Permission

    owner_role = Role.objects.create(name="owner")

    do_something = Permission.objects.get(codename="myapp.do_something")

    owner_role.add_permission(do_something)


To assign a global role for a user or group (assuming you have a user
_bobdobalina_):

    >> from djinn_auth.utils import assign_global_role, has_global_role
    >> assign_global_role(bobdobalina, owner_role)
    >> has_global_role(bobdobalina, owner_role)
    True
    >>

This should give us the permission granted to the role (please note that
the backend is normally called by the Django auth machinery using the
_User.has_perm_ call:

    >> from djinn_auth.authbackend import AuthBackend
    >> backend = AuthBackend()
    >> backend.has_perm(bobdobalina, "myapp.do_something")
    True

Revoke it:

    >> from djinn_auth.utils import unassign_global_role
    >> unassign_global_role(bobdobalina, owner_role)
    >> has_global_role(bobdobalina, owner_role)
    False
    >> backend.has_perm(bobdobalina, "myapp.do_something")
    False

Assign a local role:

    >> from djinn_auth.utils import assign_local_role, has_local_role
    >> instance = MyContentType.objects.get(pk=666)
    >> assign_local_role(bobdobalina, instance, owner_role)
    >> has_local_role(bobdobaline, instance, owner_role)
    True
    >> backend.has_perm(bobdobalina, "myapp.do_something")
    False
    >> backend.has_perm(bobdobalina, "myapp.do_something", obj=instance)
    True


Views
-----

To protect class based views, djinn\_auth provides a mixin class that
adds a permission check: djinn_auth.views.base.PermissionProtectedMixin.

Use like so:

    from django.views.generic.base import View
    from djinn_auth.views.base import PermissionProtectedMixin

    class MyView(PermissionProtectedMixin, View):

        permission = "myapp.view"

or even:

    class MyView(PermissionProtectedMixin, View):

        permission = {'GET': 'myapp.view', 'POST': 'myapp.edit'}
