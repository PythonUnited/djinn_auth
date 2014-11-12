from django.test.testcases import TestCase
from django.contrib.auth.models import User
from djinn_auth.models import Role
from djinn_auth.utils import get_global_roles, has_global_role, \
    assign_global_role, unassign_global_role


class GlobalRoleTest(TestCase):

    def setUp(self):

        self.role = Role.objects.create(name="somerole")

    def test_assign_global_role(self):

        tjibbe = User.objects.create(username="Tjibbe")
        gurbe = User.objects.create(username="Gurbe")

        self.assertFalse(has_global_role(tjibbe, self.role))
        self.assertFalse(has_global_role(gurbe, self.role))

        assign_global_role(tjibbe, self.role)

        self.assertTrue(has_global_role(tjibbe, self.role))
        self.assertFalse(has_global_role(gurbe, self.role))

    def test_has_global_role(self):

        tjibbe = User.objects.create(username="Tjibbe")

        self.assertFalse(has_global_role(tjibbe, self.role))

        assign_global_role(tjibbe, self.role)

        self.assertTrue(has_global_role(tjibbe, self.role))
        self.assertTrue(has_global_role(tjibbe, "somerole"))

    def test_unassign_global_role(self):

        tjibbe = User.objects.create(username="Tjibbe")

        self.assertFalse(has_global_role(tjibbe, self.role))

        assign_global_role(tjibbe, self.role)

        self.assertTrue(has_global_role(tjibbe, self.role))

        unassign_global_role(tjibbe, self.role)

        self.assertFalse(has_global_role(tjibbe, self.role))

    def test_get_global_roles(self):

        tjibbe = User.objects.create(username="Tjibbe")

        self.assertEquals(0, len(get_global_roles(tjibbe)))

        assign_global_role(tjibbe, self.role)

        self.assertEquals(1, len(get_global_roles(tjibbe)))
