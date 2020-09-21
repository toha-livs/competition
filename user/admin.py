from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model
from user.models import UserExtension

User = get_user_model()


class UserExtensionInlines(admin.TabularInline):
    model = UserExtension


class UserAdmin(DjangoUserAdmin):
    def get_inlines(self, request, obj):
        inlines = list(super().get_inlines(request, obj))
        inlines.append(UserExtensionInlines)
        return tuple(inlines)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
