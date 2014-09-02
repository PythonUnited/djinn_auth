from djinn_auth.models.base import RoleAssignment


class GlobalRole(RoleAssignment):

    """Provide a means of giving a user or group a specific role that
    is global, so it will add it's permissions on ALL calls on for
    instance 'has_perm'.

    """

    class Meta:

        app_label = "djinn_auth"
