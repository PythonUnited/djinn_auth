from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Role(models.Model):

    """ A role is really nothing but a bundle of permissions """

    name = models.CharField(_('name'), max_length=80, unique=True)
    permissions = models.ManyToManyField(Permission,
                                         verbose_name=_('permissions'))

    class Meta:

        app_label = "djinn_auth"
        ordering = ['name']

    def __unicode__(self):

        return self.name

    def add_permission(self, permission):

        """ Add the permission if it's not already there """

        if not self.permissions.filter(codename=permission.codename).exists():
            self.permissions.add(permission)
