from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
from djinn_auth.models import LocalRole, GlobalRole, Role


def get_group_model():

    """Even though Django doesn't let you override the group model, we
    do...

    """

    group_model = Group

    if getattr(settings, 'AUTH_GROUP_MODEL', None):
        try:
            app_label, model_name = settings.AUTH_GROUP_MODEL.split('.')
        except ValueError:
            raise ImproperlyConfigured(
                "AUTH_GROUP_MODEL must be of the form 'app_label.model_name'")

        group_model = get_model(app_label, model_name)

        if group_model is None:
            raise ImproperlyConfigured("AUTH_GROUP_MODEL refers to model '%s' "
                                       "that has not been installed" %
                                       settings.AUTH_GROUP_MODEL)
    return group_model


def set_local_role(assignee, instance, role):

    """Set the local role. Existing local roles on the given instance with
    the same role will be discarded.

    """

    if type(role) in [str, unicode]:
        role = Role.objects.get(name=role)

    ctype = ContentType.objects.get_for_model(instance)

    LocalRole.objects.filter(
        role=role,
        instance_id=instance.id,
        instance_ct=ctype).delete()

    LocalRole.objects.create(instance=instance, assignee=assignee,
                             role=role)


def assign_local_role(assignee, instance, role):

    """Assign the local role to the given assignee on the instance if it's
    not already there

    """

    instance_ct = ContentType.objects.get_for_model(instance)
    assignee_ct = ContentType.objects.get_for_model(assignee)

    if type(role) in [str, unicode]:
        role = Role.objects.get(name=role)

    LocalRole.objects.get_or_create(instance_ct=instance_ct,
                                    assignee_ct=assignee_ct,
                                    instance_id=instance.id,
                                    assignee_id=assignee.id,
                                    role=role)


def unassign_local_role(assignee, instance, role):

    """Unassign the local role on the given instance for the assignee"""

    instance_ct = ContentType.objects.get_for_model(instance)
    assignee_ct = ContentType.objects.get_for_model(assignee)

    if type(role) in [str, unicode]:
        role = Role.objects.get(name=role)

    LocalRole.objects.filter(instance_ct=instance_ct,
                             assignee_ct=assignee_ct,
                             instance_id=instance.id,
                             assignee_id=assignee.id,
                             role=role).delete()


def assign_global_role(assignee, role):

    """Assign the global role to the assignee if it's not already there"""

    assignee_ct = ContentType.objects.get_for_model(assignee)

    if type(role) in [str, unicode]:
        role = Role.objects.get(name=role)

    GlobalRole.objects.get_or_create(assignee_ct=assignee_ct,
                                     assignee_id=assignee.id,
                                     role=role)


def unassign_global_role(assignee, role):

    """Remove the global role for the asignee"""

    assignee_ct = ContentType.objects.get_for_model(assignee)

    if type(role) in [str, unicode]:
        role = Role.objects.get(name=role)

    GlobalRole.objects.filter(assignee_ct=assignee_ct,
                              assignee_id=assignee.id,
                              role=role).delete()


def get_global_roles(assignee, as_role=False):

    """Return all global roles for the given assignee. If as_role is
    True, return the actual Role objects instead of the GlobalRole
    objects.

    """

    assignee_ct = ContentType.objects.get_for_model(assignee)

    roles = GlobalRole.objects.filter(assignee_ct=assignee_ct,
                                      assignee_id=assignee.id)

    if as_role:
        roles = [role.role for role in roles]

    return roles


def has_global_role(assignee, role):

    assignee_ct = ContentType.objects.get_for_model(assignee)

    if isinstance(role, Role):
        role_name = role.name
    else:
        role_name = role

    return GlobalRole.objects.filter(
        role__name=role_name,
        assignee_id=assignee.id,
        assignee_ct=assignee_ct).exists()


def get_user_global_roles(user, as_role=False):

    """ Get global roles for user, also taking groups into account. If as_role
    is True, return Role instances instead of GlobalRole objects."""

    user_ct = ContentType.objects.get_for_model(get_user_model())
    group_ct = ContentType.objects.get_for_model(get_group_model())

    user_group_ids = user.groups.all().values_list('id', flat=True)

    roles = GlobalRole.objects.filter(
        Q(assignee_ct=user_ct, assignee_id=user.id) |
        Q(assignee_ct=group_ct, assignee_id__in=user_group_ids)
    )

    if as_role:
        roles = [role.role for role in roles]

    return roles


def get_user_local_roles(user, instance, as_role=False):

    """ Get local roles for user, also taking groups into account. If as_role
    is True, return the Role objects instead of the LocalRole objects."""

    user_ct = ContentType.objects.get_for_model(get_user_model())
    group_ct = ContentType.objects.get_for_model(get_group_model())
    instance_ct = ContentType.objects.get_for_model(instance)

    user_group_ids = user.groups.all().values_list('id', flat=True)

    roles = LocalRole.objects.filter(
        Q(instance_ct=instance_ct, instance_id=instance.id,
          assignee_ct=user_ct, assignee_id=user.id) |
        Q(instance_ct=instance_ct, instance_id=instance.id,
          assignee_ct=group_ct, assignee_id__in=user_group_ids)
    )

    if as_role:
        roles = [role.role for role in roles]

    return roles


def get_local_roles(instance, role=None):

    """ Return all local roles on the given instance. If role is set, return
    only local roles that have that role set."""

    ctype = ContentType.objects.get_for_model(instance)

    _filter = {'instance_id': instance.id, 'instance_ct': ctype}

    if role:
        if type(role) in [str, unicode]:
            _filter['role__name'] = role
        else:
            _filter['role'] = role

    return LocalRole.objects.filter(**_filter)


def has_local_role(assignee, instance, role):

    """ Check whether the assignee has the local role """

    instance_ct = ContentType.objects.get_for_model(instance)
    assignee_ct = ContentType.objects.get_for_model(assignee)

    if isinstance(role, Role):
        role_name = role.name
    else:
        role_name = role

    return LocalRole.objects.filter(
        role__name=role_name,
        assignee_id=assignee.id,
        assignee_ct=assignee_ct,
        instance_id=instance.id,
        instance_ct=instance_ct).exists()


def has_user_local_role(user, instance, role):

    """Check whether the user has the local role. This is true if either
    the user directly has the role, or if one of the user groups has
    it.

    """

    if type(role) in [str, unicode]:
        role = Role.objects.get(name=role)

    return get_user_local_roles(user, instance).filter(role=role).exists()
