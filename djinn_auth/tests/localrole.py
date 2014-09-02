from django.test.testcases import TestCase
from django.contrib.auth.models import Group, User
from djinn_auth.models import Role
from djinn_auth.utils import set_local_role, get_local_roles, has_local_role, \
    add_local_role


class LocalRoleTest(TestCase):

    def setUp(self):

        self.content = Group.objects.create(name="Foo")
        self.owner = Role.objects.create(name="owner")

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

    def test_add_local_role(self):

        tjibbe = User.objects.create(username="Tjibbe")
        gurbe = User.objects.create(username="Gurbe")

        self.assertFalse(has_local_role(tjibbe, self.content, self.owner))
        self.assertFalse(has_local_role(gurbe, self.content, self.owner))

        add_local_role(tjibbe, self.content, self.owner)

        self.assertTrue(has_local_role(tjibbe, self.content, self.owner))
        self.assertFalse(has_local_role(gurbe, self.content, self.owner))

        add_local_role(gurbe, self.content, self.owner)

        self.assertTrue(has_local_role(tjibbe, self.content, self.owner))
        self.assertTrue(has_local_role(gurbe, self.content, self.owner))

    def test_get_local_roles(self):

        tjibbe = User.objects.create(username="Tjibbe")
        gurbe = User.objects.create(username="Gurbe")

        self.assertEquals(0, len(get_local_roles(self.content)))
        self.assertEquals(0, len(get_local_roles(self.content, self.owner)))

        set_local_role(tjibbe, self.content, self.owner)
        add_local_role(gurbe, self.content, self.owner)

        self.assertEquals(2, len(get_local_roles(self.content)))
        self.assertEquals(2, len(get_local_roles(self.content, self.owner)))
