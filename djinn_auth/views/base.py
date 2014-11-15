from django.core.exceptions import PermissionDenied


class PermissionProtectedMixin(object):

    """ Mixin to protect the view with a permission. If provided,
    the class may actually check against the type of call """

    permission = None

    def get_permission(self, request):

        if type(self.permission) == dict:
            return self.permission.get(request.method)
        else:
            return self.permission

    def check_permission(self, request):

        permission = self.get_permission(request)

        if not permission:
            return True

        try:
            obj = self.get_object()
        except:
            obj = None

        return request.user.has_perm(permission, obj=obj)

    def handle_unauthorized(self):

        raise PermissionDenied

    def dispatch(self, request, *args, **kwargs):

        if not self.check_permission(request):
            self.handle_unauthorized()

        return super(PermissionProtectedMixin, self).dispatch(
            request, *args, **kwargs)
