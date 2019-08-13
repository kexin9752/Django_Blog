import xadmin

from accounts.models import User, UserProfile, LoginRecord, UserAddress, PasswdChangeLog


class UserAdmin(object):
    list_display = ("format_username","nickname","integral","is_active")
    search_fields = ('username','nickname')
    actions = ['disable_user','enable_user']

    def format_username(self,obj):
        return obj.username[0:3]+"***"
    format_username.short_description = '用户名'

    def disable_user(self,request,queryset):
        queryset.update(is_active=False)
    disable_user.short_description = "批量禁用用户"

    def enable_user(self,request,queryset):
        queryset.update(is_active=True)
    enable_user.short_description='批量启用用户'

xadmin.site.unregister(User)
xadmin.site.register(User,UserAdmin)


class UserProfileAdmin(object):
    list_display = ["user","real_name","phone_no","gender","age","qq"]


xadmin.site.register(UserProfile,UserProfileAdmin)


class LoginRecordAdmin(object):
    list_display = ["username","ip","created_at"]


xadmin.site.register(LoginRecord,LoginRecordAdmin)


class UserAddressAdmin(object):
    list_display = ["user","address","phone","is_default","is_valid"]


xadmin.site.register(UserAddress,UserAddressAdmin)


class PasswdChangeLogAdmin(object):
    list_display = ["user","old_passwd","new_passwd","created_at"]


xadmin.site.register(PasswdChangeLog,PasswdChangeLogAdmin)

