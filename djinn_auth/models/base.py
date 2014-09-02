from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from djinn_auth.models.role import Role


class RoleAssignment(models.Model):

    """Abstract role assignment class"""

    assignee_ct = models.ForeignKey(ContentType, related_name='+')
    assignee_id = models.PositiveIntegerField()
    assignee = generic.GenericForeignKey('assignee_ct', 'assignee_id')

    role = models.ForeignKey(Role)

    class Meta:

        app_label = "djinn_auth"
        abstract = True

    def __unicode__(self):

        return "%s is %s" % (self.assignee, self.role)
