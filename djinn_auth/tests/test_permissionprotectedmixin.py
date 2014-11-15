from django.test.testcases import TestCase
from django.contrib.auth.models import User
from django.views.generic.base import View
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from djinn_auth.views.base import PermissionProtectedMixin
from djinn_auth.models.role import Role
from djinn_auth.utils import assign_local_role


class BaseView(PermissionProtectedMixin, View):

    def get(self, request, *args, **kwargs):

        return "GET OK"

    def post(self, request, *args, **kwargs):

        return "POST OK"


class OpenView(BaseView):

    pass


class ClosedView(BaseView):

    permission = "djinn_auth.view"


class SemiClosedView(BaseView):

    permission = {'GET': "djinn_auth.view"}


class ClosedDetailView(BaseView):

    permission = "djinn_auth.view"
    obj = None

    def get_object(self):

        return self.obj


class Request(object):

    def __init__(self, method, user):

        self.method = method
        self.user = user


class PermissionProtectedMixinTest(TestCase):

    def setUp(self):

        self.user = User.objects.create(username="bobdobalina")

        contenttype = ContentType.objects.get(app_label='contenttypes',
                                              model='contenttype')

        self.perm, created = Permission.objects.get_or_create(
            codename="view",
            content_type=contenttype, defaults={'name': 'View content'})

    def test_get(self):

        view = OpenView.as_view()

        self.assertEquals("GET OK", view(Request("GET", self.user)))

        view = ClosedView.as_view()

        try:
            view(Request("GET", self.user))
            self.fail("GET should be forbidden")
        except PermissionDenied:
            pass

        self.user.user_permissions.add(self.perm)

        self.assertEquals("GET OK", view(Request("GET", self.user)))

    def test_methods(self):

        view = SemiClosedView.as_view()

        self.assertEquals("POST OK", view(Request("POST", self.user)))

        try:
            view(Request("GET", self.user))
            self.fail("GET should be forbidden")
        except PermissionDenied:
            pass

    def test_object_view(self):

        thing = self.user

        view = ClosedDetailView.as_view(obj=thing)

        try:
            view(Request("GET", self.user))
            self.fail("GET should be forbidden")
        except PermissionDenied:
            pass

        # Let's have some fun and assign a local permission to self...
        #
        owner, created = Role.objects.get_or_create(name="owner")
        owner.add_permission(self.perm)

        assign_local_role(self.user, thing, owner)

        self.assertEquals("GET OK", view(Request("GET", self.user)))
