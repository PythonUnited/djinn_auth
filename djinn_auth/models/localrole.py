from django.db import models
from django.contrib.contenttypes.models import ContentType
from djinn_auth.models.base import RoleAssignment
try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except:
    # django <1.8 compatibility
    from django.contrib.contenttypes.generic import GenericForeignKey


class LocalRole(RoleAssignment):

    """ Local role for given model instance. Can be assigned either to
    user or to usergroup.
    """

    instance_ct = models.ForeignKey(ContentType, related_name='+')
    instance_id = models.PositiveIntegerField()
    instance = GenericForeignKey('instance_ct', 'instance_id')

    class Meta:

        app_label = "djinn_auth"

    def __unicode__(self):

        return u"%s is %s for %s" % (self.assignee, self.role, self.instance)
