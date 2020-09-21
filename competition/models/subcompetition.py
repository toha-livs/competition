from django.db import models
from django.utils.functional import cached_property

from common.models import BaseNameModel
from competition.choices.calculate_mark import CalculateMarkTypeChoices
from competition.choices.sub_competition_type import SubCompetitionTypeChoices
from competition.choices.competition_type import CompetitionTypeChoices
from competition.choices.level import Level


class CompetitionScope(BaseNameModel, models.Model):
    date_start = models.DateField("Дата начала", null=True, blank=True)
    level = models.IntegerField("Уровень", choices=Level.choices, default=Level.REGION)
    date_end = models.DateField('Дата окончания', null=True, blank=True)

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнование'

    @property
    def date_render(self):
        result = f'{self.date_start.day}-{self.date_end.strftime("%d.%m.%Y")}'
        if self.date_start.month != self.date_end.month:
            result = f'{self.date_start.strftime("%d.%m")}-{self.date_end.strftime("%d.%m.%Y")}'
        return result


class Competition(BaseNameModel, models.Model):
    competition_scope = models.ForeignKey(CompetitionScope, on_delete=models.CASCADE, related_name='competitions')
    date = models.DateField("Дата", null=True, blank=True)
    competition_type = models.IntegerField(
        'Тип совернований',
        choices=CompetitionTypeChoices.choices,
        default=CompetitionTypeChoices.ALL_AROUND
    )
    times_register_by = models.IntegerField('В зачет по', default=3)

    @cached_property
    def gymnast_count(self):
        return sum([sum([team.gymnasts.count() for team in sub.teams.all()]) for sub in self.subs.all()])

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'


class SubCompetition(BaseNameModel, models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='subs')
    date = models.DateField('Дата проведения')

    def __str__(self):
        return f'{self.competition.competition_scope.name} | {self.competition.name} | {self.name}'

    class Meta:
        verbose_name = 'Под Соревнование'
        verbose_name_plural = 'Под Соревнования'


class SubCompetitionManager(models.Model):
    sub_competition = models.OneToOneField(SubCompetition, on_delete=models.CASCADE, related_name='manager')
    rotation = models.IntegerField('Ротейшен', default=0)

    class Meta:
        verbose_name = 'Соревнование (Менеджер)'
        verbose_name_plural = 'Соревнования (Менеджер)'


class SubCompetitionSettings(models.Model):
    sub_competition = models.OneToOneField(SubCompetition, on_delete=models.CASCADE, related_name='settings')
    day_off = models.IntegerField('Выхоной', default=0)
    calculate_mark_type = models.IntegerField(
        'Тип расчета оценки',
        choices=CalculateMarkTypeChoices.choices,
        default=CalculateMarkTypeChoices.BY_3
    )
    sub_competition_type = models.IntegerField(
        'Тип соревнований',
        choices=SubCompetitionTypeChoices.choices,
        default=SubCompetitionTypeChoices.DEFAULT
    )

    class Meta:
        verbose_name = 'Настройки соревнований'
        verbose_name_plural = 'Настройки соревнований'
