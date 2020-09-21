from django.contrib import admin
from nested_admin.nested import NestedStackedInline, NestedModelAdmin

from competition.forms.gymnast import GymnastForm
from competition.models import SubCompetition, Result, MarkD, MarkE, Gymnast, SubCompetitionSettings, Team, Judge, \
    Competition, CompetitionScope, SubCompetitionManager
from competition.models.judge import JudgeTypeChoice


class SubCompetitionInline(NestedStackedInline):
    model = SubCompetition
    extra = 0


class CompetitionInline(NestedStackedInline):
    model = Competition
    inlines = SubCompetitionInline,
    extra = 0


@admin.register(CompetitionScope)
class CompetitionScopeAdmin(NestedModelAdmin):
    list_display = 'name',
    inlines = CompetitionInline,


class SubCompetitionSettingsInline(admin.TabularInline):
    model = SubCompetitionSettings


class SubCompetitionManagerInline(admin.TabularInline):
    model = SubCompetitionManager


@admin.register(SubCompetition)
class SubCompetitionAdmin(admin.ModelAdmin):
    list_display = 'scope_competition_name', 'competition_name', 'name',
    inlines = SubCompetitionManagerInline, SubCompetitionSettingsInline,

    def competition_name(self, obj):
        return obj.competition.name

    def scope_competition_name(self, obj):
        return obj.competition.competition_scope.name

    competition_name.short_description = 'Название под соревнований'
    scope_competition_name.short_description = 'Название соревнований'


class MarkDInline(admin.TabularInline):
    model = MarkD
    extra = 3

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        field = super().formfield_for_foreignkey(
            db_field, request, **kwargs)

        if db_field.name == 'judge':
            result = request._obj_
            if result is not None:
                field.queryset = field.queryset.filter(
                    competition=result.gymnast.team.competition,
                    apparatus=result.apparatus,
                    judge_type=JudgeTypeChoice.D,
                )
                # widget changed to filter by building
                # field.widget.rel.limit_choices_to = {'judge': result.id}
            else:
                field.queryset = field.queryset.none()

        return field


class MarkEInline(admin.TabularInline):
    model = MarkE

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super().formfield_for_foreignkey(
            db_field, request, **kwargs)

        if db_field.name == 'judge':
            result = request._obj_
            if result is not None:
                field.queryset = field.queryset.filter(
                    competition=result.gymnast.team.competition,
                    apparatus=result.apparatus,
                    judge_type=JudgeTypeChoice.E
                )
                # widget changed to filter by building
                # field.widget.rel.limit_choices_to = {'judge': result.id}
            else:
                field.queryset = field.queryset.none()

        return field


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = 'apparatus', 'gymnast', 'result',
    inlines = MarkDInline, MarkEInline,

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)


class GymnastInline(admin.TabularInline):
    model = Gymnast
    extra = 2
    form = GymnastForm


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = 'name', 'competition',
    inlines = GymnastInline,


@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):
    list_display = 'user', 'competition', 'apparatus', 'judge_type',
