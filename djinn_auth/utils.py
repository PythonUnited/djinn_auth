from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.contrib.auth.models import User, Group
from djinn_auth.models import LocalRole, GlobalRole


def set_local_role(assignee, instance, role):

    """Set the local role. Existing local roles in the given instance with
    the same role will be discarded

    """

    ctype = ContentType.objects.get_for_model(instance)

    LocalRole.objects.filter(
        role=role,
        instance_id=instance.id,
        instance_ct=ctype).delete()

    LocalRole.objects.create(instance=instance, assignee=assignee,
                             role=role)


def add_local_role(assignee, instance, role):

    """Add the local role if it's not already there"""

    instance_ct = ContentType.objects.get_for_model(instance)
    assignee_ct = ContentType.objects.get_for_model(assignee)

    LocalRole.objects.get_or_create(instance_ct=instance_ct,
                                    assignee_ct=assignee_ct,
                                    instance_id=instance.id,
                                    assignee_id=assignee.id,
                                    role=role)


def assign_global_role(assignee, role):

    """Assign the global role if it's not already there"""

    assignee_ct = ContentType.objects.get_for_model(assignee)

    GlobalRole.objects.get_or_create(assignee_ct=assignee_ct,
                                     assignee_id=assignee.id,
                                     role=role)


def unassign_global_role(assignee, role):

    """Assign the global role if it's not already there"""

    assignee_ct = ContentType.objects.get_for_model(assignee)

    GlobalRole.objects.filter(assignee_ct=assignee_ct,
                              assignee_id=assignee.id,
                              role=role).delete()


def get_global_roles(assignee, as_role=False):

    ctype = ContentType.objects.get_for_model(assignee)

    roles = GlobalRole.objects.filter(assignee_ct=ctype,
                                      assignee_id=assignee.id)

    if as_role:
        roles = [role.role for role in roles]

    return roles


def get_user_global_roles(user, as_role=False):

    """ Get global roles for user, also taking groups into account """

    user_ct = ContentType.objects.get_for_model(User)
    group_ct = ContentType.objects.get_for_model(Group)

    user_group_ids = user.groups.all().values_list('id', flat=True)

    roles = GlobalRole.objects.filter(
        Q(assignee_ct=user_ct, assignee_id=user.id) |
        Q(assignee_ct=group_ct, assignee_id__in=user_group_ids)
    )

    if as_role:
        roles = [role.role for role in roles]

    return roles


def get_local_roles(instance, role=None):

    ctype = ContentType.objects.get_for_model(instance)

    _filter = {'instance_id': instance.id, 'instance_ct': ctype}

    if role:
        _filter['role'] = role

    return LocalRole.objects.filter(**_filter)


def has_local_role(assignee, instance, role):

    instance_ct = ContentType.objects.get_for_model(instance)
    assignee_ct = ContentType.objects.get_for_model(assignee)

    return LocalRole.objects.filter(
        role=role,
        assignee_id=assignee.id,
        assignee_ct=assignee_ct,
        instance_id=instance.id,
        instance_ct=instance_ct).exists()
