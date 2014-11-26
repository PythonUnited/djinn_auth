from django.test.testcases import TestCase
from django.contrib.auth.models import Group, User
from djinn_auth.models import Role
from djinn_auth.utils import set_local_role, get_local_roles, has_local_role, \
    assign_local_role, has_user_local_role


class LocalRoleTest(TestCase):

    def setUp(self):

        self.content = Group.objects.create(name="Foo")
        self.owner, created = Role.objects.get_or_create(name="owner")

    def test_set_local_role(self):

        tjibbe = User.objects.create(username="Tjibbe")
        gurbe = User.objects.create(username="Gurbe")

        self.assertFalse(has_local_role(tjibbe, self.content, self.owner))
        self.assertFalse(has_local_role(gurbe, self.content, self.owner))

        set_local_role(tjibbe, self.content, self.owner)

        self.assertTrue(has_local_role(tjibbe, self.content, self.owner))
        self.assertFalse(has_local_role(gurbe, self.content, self.owner))

        set_local_role(gurbe, self.content, self.owner)

        self.assertFalse(has_local_role(tjibbe, self.content, self.owner))
        self.assertTrue(has_local_role(gurbe, self.content, self.owner))

        set_local_role(tjibbe, self.content, "owner")

        self.assertTrue(has_local_role(tjibbe, self.content, self.owner))
        self.assertFalse(has_local_role(gurbe, self.content, self.owner))

    def test_set_local_role_to_group(self):

        tjibbe = User.objects.create(username="Tjibbe")
        tjibbes = Group.objects.create(name="Tjibbes")

        self.assertFalse(has_user_local_role(tjibbe, self.content, self.owner))

        set_local_role(tjibbes, self.content, self.owner)

        self.assertFalse(has_user_local_role(tjibbe, self.content, self.owner))

        tjibbe.groups.add(tjibbes)

        self.assertTrue(has_user_local_role(tjibbe, self.content, self.owner))

    def test_assign_local_role(self):

        tjibbe = User.objects.create(username="Tjibbe")
        gurbe = User.objects.create(username="Gurbe")

        self.assertFalse(has_local_role(tjibbe, self.content, self.owner))
        self.assertFalse(has_local_role(gurbe, self.content, self.owner))

        assign_local_role(tjibbe, self.content, self.owner)

        self.assertTrue(has_local_role(tjibbe, self.content, self.owner))
        self.assertFalse(has_local_role(gurbe, self.content, self.owner))

        assign_local_role(gurbe, self.content, self.owner)

        self.assertTrue(has_local_role(tjibbe, self.content, self.owner))
        self.assertTrue(has_local_role(gurbe, self.content, self.owner))

    def test_get_local_roles(self):

        tjibbe = User.objects.create(username="Tjibbe")
        gurbe = User.objects.create(username="Gurbe")

        self.assertEquals(0, len(get_local_roles(self.content)))
        self.assertEquals(0, len(get_local_roles(self.content, self.owner)))

        set_local_role(tjibbe, self.content, self.owner)
        assign_local_role(gurbe, self.content, self.owner)

        self.assertEquals(2, len(get_local_roles(self.content)))
        self.assertEquals(2, len(get_local_roles(self.content, self.owner)))
