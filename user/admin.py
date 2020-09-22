from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model

from user.choices.user_type import UserType
from user.models import UserExtension

User = get_user_model()


class ExtTypeFilter(admin.SimpleListFilter):
    title = 'Тип юзера'
    parameter_name = 'ext_type'

    def lookups(self, request, model_admin):
        return UserType.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(ext__type=self.value())


class UserExtensionInlines(admin.TabularInline):
    model = UserExtension


class UserAdmin(DjangoUserAdmin):

    list_display = 'username', 'last_name', 'first_name', 'is_superuser', 'is_staff', 'ext_type',

    def ext_type(self, obj):
        result = '-'
        if hasattr(obj, 'ext'):
            result = obj.ext.get_type_display()
        return result

    def get_inlines(self, request, obj):
        inlines = list(super().get_inlines(request, obj))
        inlines.append(UserExtensionInlines)
        return tuple(inlines)

    def get_list_filter(self, request):
        filters = super().get_list_filter(request)
        return *filters, ExtTypeFilter,


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
