from django.db import models
from django.conf import settings
from django.contrib.auth.models import Permission
from polymorphic import PolymorphicModel


class Group(PolymorphicModel):

    """Abstract group base. The polymorphism enables you to extend this
    class in several ways, but find all kinds with the Group.objects
    manager

    """

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True)
    permissions = models.ManyToManyField(
        Permission,
        related_name='groups',
        blank=True)

    def __unicode__(self):

        return self.name

    class Meta:
        ordering = ["name"]
        app_label = "djinn_auth"
