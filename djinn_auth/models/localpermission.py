from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except:
    # django <1.8 compatibility
    from django.contrib.contenttypes.generic import GenericForeignKey


class LocalPermission(models.Model):

    """Local permission for given model instance. Can be assigned either
    to user or to usergroup.

    """

    instance_ct = models.ForeignKey(ContentType, related_name='+')
    instance_id = models.PositiveIntegerField()
    instance = GenericForeignKey('instance_ct', 'instance_id')

    assignee_ct = models.ForeignKey(ContentType, related_name='+')
    assignee_id = models.PositiveIntegerField()
    assignee = GenericForeignKey('assignee_ct', 'assignee_id')

    permission = models.ForeignKey(Permission)

    class Meta:

        app_label = "djinn_auth"

    def __unicode__(self):

        return u"%s has %s for %s" % (self.assignee, self.permission,
                                      self.content)
