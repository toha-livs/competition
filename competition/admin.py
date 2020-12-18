import csv

from django.contrib import admin
from django.http import HttpResponse
from nested_admin.nested import NestedStackedInline, NestedModelAdmin

from competition.choices.sex import SexChoices
from competition.forms.gymnast import GymnastForm
from competition.models import (
    SubCompetition, Gymnast, SubCompetitionSettings, Team,
    Competition, CompetitionScope, SubCompetitionManager
)
from judge.models import Judge


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


@admin.register(Competition)
class CompetitionAdmin(NestedModelAdmin):
    list_display = 'name',
    inlines = SubCompetitionInline,

    actions = ['get_result', 'calculate_result']

    def get_result(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="results.csv"'
        writer = csv.writer(response)
        headers = ['Имя', 'Розряд', 'Город', 'Год']
        competition = queryset.first()
        if competition.subs.first().manager.sex == SexChoices.MALE:
            headers.extend(['ВУ', 'Конь', 'Кольца', 'ОП', 'ПП', 'ВП', 'Всего'])
        else:
            headers.extend(['ВУ', 'Бревно', 'РБ', 'ОП', 'Всего'])
        for gymnast in Gymnast.objects.filter(team__competition__competition=competition).order_by('level', '-score'):
            writer.writerow([
                gymnast.get_competition_name(),
                gymnast.get_level_display(),
                gymnast.city,
                gymnast.user.ext.birthday_date.strftime('%Y'),
                getattr(gymnast.results.fxm(), 'result', '-'),
                getattr(gymnast.results.ph(), 'result', '-'),
                getattr(gymnast.results.rings(), 'result', '-'),
                getattr(gymnast.results.vtm(), 'result', '-'),
                getattr(gymnast.results.pb(), 'result', '-'),
                getattr(gymnast.results.hb(), 'result', '-'),
                gymnast.score,
            ])
        return response

    def calculate_result(self, request, queryset):
        for competition in queryset:
            competition.calculate()

    get_result.short_description = "Получить результаты *.csv"
    calculate_result.short_description = "Пересчитать результаты"


class SubCompetitionSettingsInline(admin.TabularInline):
    model = SubCompetitionSettings


class SubCompetitionManagerInline(admin.TabularInline):
    model = SubCompetitionManager


class JudgeInline(admin.TabularInline):
    model = Judge


@admin.register(SubCompetition)
class SubCompetitionAdmin(admin.ModelAdmin):
    list_display = 'scope_competition_name', 'competition_name', 'name',
    inlines = SubCompetitionManagerInline, SubCompetitionSettingsInline, JudgeInline,

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
    list_display = 'name', 'competition', 'start_apparatus',
    inlines = GymnastInline,


