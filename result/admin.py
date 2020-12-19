from dal_admin_filters import AutocompleteFilter
from django.contrib import admin

from .forms import ResultForm
from .models import MarkD, MarkE, Result


class MarkDInline(admin.TabularInline):
    model = MarkD
    extra = 1

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        field = super().formfield_for_foreignkey(
            db_field, request, **kwargs)

        # if db_field.name == 'judge':
        #     result = request._obj_
        #     if result is not None:
        #         field.queryset = field.queryset.filter(
        #             competition=result.gymnast.team.competition,
        #             apparatus=result.apparatus,
        #             judge_type=JudgeTypeChoice.D,
        #         )
        #         # widget changed to filter by building
        #         # field.widget.rel.limit_choices_to = {'judge': result.id}
        #     else:
        #         field.queryset = field.queryset.none()

        return field


class MarkEInline(admin.TabularInline):
    model = MarkE

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super().formfield_for_foreignkey(
            db_field, request, **kwargs)

        # if db_field.name == 'judge':
        #     result = request._obj_
        #     if result is not None:
        #         field.queryset = field.queryset.filter(
        #             competition=result.gymnast.team.competition,
        #             apparatus=result.apparatus,
        #             judge_type=JudgeTypeChoice.E
        #         )
        #         # widget changed to filter by building
        #         # field.widget.rel.limit_choices_to = {'judge': result.id}
        #     else:
        #         field.queryset = field.queryset.none()

        return field


class GymnastFilter(AutocompleteFilter):
    title = 'Гимнаст'
    field_name = 'gymnast'
    autocomplete_url = 'competition:gymnast-autocomplete'


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    form = ResultForm
    list_display = 'apparatus', 'gymnast', 'result',
    inlines = MarkDInline, MarkEInline,

    list_filter = 'apparatus', GymnastFilter,

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)
