from django.test.testcases import TestCase
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from djinn_auth.models import Role
from djinn_auth.utils import assign_global_role, unassign_global_role
from djinn_auth.authbackend import AuthBackend


class AuthBackendTest(TestCase):

    """ Test the auth backend for role base permissions """

    def setUp(self):

        self.backend = AuthBackend()
        self.owner = Role.objects.create(name="owner")

        ctype = ContentType.objects.get_for_model(Group)

        do_something, created = Permission.objects.get_or_create(
            codename="do_something",
            content_type=ctype, defaults={'name': 'Can do things'})

        self.perm = do_something
        self.owner.add_permission(do_something)

    def test_has_perm_by_global_role(self):

        """ Test global permissions """

        tjibbe = User.objects.create(username="Tjibbe")

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something"))

        assign_global_role(tjibbe, self.owner)

        self.assertTrue(self.backend.has_perm(tjibbe, "app.do_something"))

        unassign_global_role(tjibbe, self.owner)

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something"))

    def test_has_perm_by_global_role_on_group(self):

        """ Test global permissions """

        tjibbe = User.objects.create(username="Tjibbe")
        tjibbes = Group.objects.create(name="Tjibbes")

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something"))

        assign_global_role(tjibbes, self.owner)

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something"))

        tjibbe.groups.add(tjibbes)

        self.assertTrue(self.backend.has_perm(tjibbe, "app.do_something"))

        tjibbe.groups.remove(tjibbes)

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something"))

    def test_has_perm_by_global_permission_on_group(self):

        """ Test global permissions when the permission has been set
        onto a group that the user is a member of """

        tjibbe = User.objects.create(username="Tjibbe")
        tjibbes = Group.objects.create(name="Tjibbes")

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something"))

        tjibbes.permissions.add(self.perm)

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something"))

        tjibbe.groups.add(tjibbes)

        self.assertTrue(self.backend.has_perm(tjibbe, "app.do_something"))

        tjibbe.groups.remove(tjibbes)

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something"))
