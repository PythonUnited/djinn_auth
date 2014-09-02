from django.contrib.contenttypes.models import ContentType
from djinn_auth.models import LocalRole


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
