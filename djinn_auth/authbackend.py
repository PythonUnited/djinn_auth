import logging
from django.contrib.auth.models import Permission
from djinn_auth.utils import get_user_global_roles, get_user_local_roles


LOGGER = logging.getLogger("djinn_auth")


class AuthBackend(object):

    # We support object based permissions
    #
    supports_object_permissions = True
    supports_anonymous_user = False

    def authenticate(self, username=None, password=None):

        return None

    def get_user(self, user_id):

        return None

    def has_perm(self, user, permission, obj=None):

        """ Find out whether the user has a given permission. This is
        a potentially 'heavy' operation, given the role based auth
        that we have.

        A user can have a permission in general (obj=None) if:
          1. the user has a global role that holds the permission
          2. the user is part of a group that has a global role that holds the
             permission

        When an object is provided, the user can FURTHERMORE have a permission
        if:
          3. the user has a local role on the object
          4. the user is part of a group that has a local role on the object

        Some heuristics are in place to try and determine this in a
        smart way. We first check on the 'user' role. If this holds
        the permission, return. If not, check ownership...

        """

        if user.is_anonymous():
            return False

        return self._check_all_permissions(user, permission, obj=obj)

    def _check_all_permissions(self, user, perm, obj=None):

        """ Go find the actual permission, then loop over it's roles, users
        and groups. Check if the user has the global role, the role
        locally if obj is provided, or is in a group with that
        permission.
        """

        perm_app, perm_name = perm.split(".")

        _perm = Permission.objects.get(codename=perm_name)

        # Check whether the user is in the permission's user set
        #
        _filter = {user.USERNAME_FIELD: user.get_username()}

        if _perm.user_set.filter(**_filter).exists():
            return True

        user_group_ids = user.groups.all().values_list('id', flat=True)

        # Check whether the user and the permission share any groups
        #
        if _perm.group_set.filter(pk__in=user_group_ids):
            return True

        # Now check on the roles. Start with global roles
        #
        perm_role_ids = _perm.role_set.all().values_list('id', flat=True)

        if not obj or getattr(obj, "acquire_global_roles", True):

            if get_user_global_roles(user).filter(
                    role__id__in=perm_role_ids).exists():
                return True

        # Now go for local roles if need be
        #
        if obj:

            if get_user_local_roles(user, obj).filter(
                    role__id__in=perm_role_ids
            ).exists():
                return True

        # Finally, we may have an acquire list, so as to be able to
        # 'inherit' roles from another object, or objects.
        #
        for acq_obj in getattr(obj, "acquire_from", []):
            if get_user_local_roles(user, acq_obj).filter(
                    role__id__in=perm_role_ids
            ).exists():
                return True

        return False
