from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from djinn_auth.models.base import RoleAssignment


class LocalRole(RoleAssignment):

    """ Local role for given model instance. Can be assigned either to
    user or to usergroup.
    """

    instance_ct = models.ForeignKey(ContentType, related_name='+')
    instance_id = models.PositiveIntegerField()
    instance = generic.GenericForeignKey('instance_ct', 'instance_id')

    class Meta:

        app_label = "djinn_auth"

    def __unicode__(self):

        return u"%s is %s for %s" % (self.assignee, self.role, self.instance)
