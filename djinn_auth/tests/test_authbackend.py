from django.test.testcases import TestCase
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from djinn_auth.models import Role
from djinn_auth.utils import assign_global_role, unassign_global_role, \
    assign_local_role, unassign_local_role
from djinn_auth.authbackend import AuthBackend


class AuthBackendTest(TestCase):

    """ Test the auth backend for role base permissions. """

    def setUp(self):

        self.backend = AuthBackend()
        self.owner, created = Role.objects.get_or_create(name="owner")

        ctype = ContentType.objects.get_for_model(Group)

        do_something, created = Permission.objects.get_or_create(
            codename="do_something",
            content_type=ctype, defaults={'name': 'Can do things'})

        self.perm = do_something
        self.owner.add_permission(do_something)

    def test_has_perm_by_global_role(self):

        """Test global permissions when a global role has been granted to the
        user
        """

        tjibbe = User.objects.create(username="Tjibbe")

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something"))

        assign_global_role(tjibbe, self.owner)

        self.assertTrue(self.backend.has_perm(tjibbe, "app.do_something"))

        unassign_global_role(tjibbe, self.owner)

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something"))

    def test_has_perm_by_permission_on_user(self):

        """Test global permissions when a specific permission has been granted
        to the user
        """

        tjibbe = User.objects.create(username="Tjibbe")

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something"))

        tjibbe.user_permissions.add(self.perm)

        self.assertTrue(self.backend.has_perm(tjibbe, "app.do_something"))

        tjibbe.user_permissions.remove(self.perm)

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something"))

    def test_has_perm_by_global_role_on_group(self):

        """Test global permissions when the permission is part of a global
        group role

        """

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

    def test_has_perm_on_object(self):

        """ Check whether the user has the permission on the object, when
        a global role has been assigned to this user."""

        tjibbe = User.objects.create(username="Tjibbe")

        content = Group.objects.create(name="Tjibbes")

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something",
                                               obj=content))

        assign_global_role(tjibbe, self.owner)

        self.assertTrue(self.backend.has_perm(tjibbe, "app.do_something",
                                              obj=content))

        unassign_global_role(tjibbe, self.owner)

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something",
                                               obj=content))

    def test_has_perm_on_object_with_userpermission(self):

        """ Test whether the permission is there when the user has been given
        a specific permission."""

        tjibbe = User.objects.create(username="Tjibbe")

        content = Group.objects.create(name="Tjibbes")

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something",
                                               obj=content))

        tjibbe.user_permissions.add(self.perm)

        self.assertTrue(self.backend.has_perm(tjibbe, "app.do_something",
                                              obj=content))

        tjibbe.user_permissions.remove(self.perm)

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something",
                                               obj=content))

    def test_has_perm_on_object_by_local_role(self):

        tjibbe = User.objects.create(username="Tjibbe")

        content = Group.objects.create(name="Tjibbes")

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something",
                                               obj=content))

        assign_local_role(tjibbe, content, self.owner)

        self.assertTrue(self.backend.has_perm(tjibbe, "app.do_something",
                                              obj=content))

        unassign_local_role(tjibbe, content, self.owner)

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something",
                                               obj=content))

    def test_has_perm_on_object_by_local_role_on_group(self):

        tjibbe = User.objects.create(username="Tjibbe")
        tjibbes = Group.objects.create(name="Tjibbes")

        content = Group.objects.create(name="Content")

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something",
                                               obj=content))

        assign_local_role(tjibbes, content, self.owner)

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something",
                                               obj=content))

        tjibbe.groups.add(tjibbes)

        self.assertTrue(self.backend.has_perm(tjibbe, "app.do_something",
                                              obj=content))

        tjibbe.groups.remove(tjibbes)

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something",
                                               obj=content))

    def test_local_roles_without_acquire_global(self):

        """Test whether the backend actually honors the 'acquire_global_roles'
        setting.  """

        tjibbe = User.objects.create(username="Tjibbe")
        content = Group.objects.create(name="Content")

        assign_global_role(tjibbe, self.owner)

        self.assertTrue(self.backend.has_perm(tjibbe, "app.do_something",
                                              obj=content))

        setattr(content, "acquire_global_roles", False)

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something",
                                               obj=content))

    def test_has_perm_with_acquisition(self):

        content = Group.objects.create(name="Tjibbes")
        parent = Group.objects.create(name="Parent")

        tjibbe = User.objects.create(username="Tjibbe")

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something",
                                               obj=content))

        assign_local_role(tjibbe, parent, self.owner)

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something",
                                               obj=content))

        assign_local_role(tjibbe, parent, self.owner)

        self.assertFalse(self.backend.has_perm(tjibbe, "app.do_something",
                                               obj=content))

        content.acquire_from = [parent]

        self.assertTrue(self.backend.has_perm(tjibbe, "app.do_something",
                                              obj=content))
