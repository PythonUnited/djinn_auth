from django.contrib import admin
from djinn_auth.models.role import Role
from djinn_auth.models.localrole import LocalRole
from djinn_auth.models.globalrole import GlobalRole
from djinn_auth.models.localpermission import LocalPermission


class RoleAdmin(admin.ModelAdmin):

    list_display = ['name']
    search_fields = ['name']
    ordering = ['-name']


class LocalRoleAdmin(admin.ModelAdmin):

    pass


class GlobalRoleAdmin(admin.ModelAdmin):

    pass


class LocalPermissionAdmin(admin.ModelAdmin):

    pass


admin.site.register(Role, RoleAdmin)
admin.site.register(LocalRole, LocalRoleAdmin)
admin.site.register(GlobalRole, GlobalRoleAdmin)
admin.site.register(LocalPermission, LocalPermissionAdmin)
