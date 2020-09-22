from django.contrib import admin
from nested_admin.nested import NestedStackedInline, NestedModelAdmin

from competition.forms.gymnast import GymnastForm
from competition.models import (
    SubCompetition, Gymnast, SubCompetitionSettings, Team,
    Competition, CompetitionScope, SubCompetitionManager
)


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


class GymnastInline(admin.TabularInline):
    model = Gymnast
    extra = 2
    form = GymnastForm


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = 'name', 'competition',
    inlines = GymnastInline,


