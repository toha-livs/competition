from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import cached_property

from competition.choices.sex import SexChoices
from competition.models.team import Team

User = get_user_model()


class LevelChoice(models.IntegerChoices):
    JUNIOR3 = 0, 'Третий юнешеский'
    JUNIOR2 = 1, 'Второй юнешеский'
    JUNIOR1 = 2, 'Первый юнешеский'
    ADULT3 = 3, 'Третий взрослый'
    ADULT2 = 4, 'Второй взрослый'
    ADULT1 = 5, 'Превый взрослый'
    KMS = 6, 'КМС'
    MS = 7, 'МС'

    JUNIOR2FREE = 8, 'Второй юнешеский (Произвольный)'
    JUNIOR1FREE = 9, 'Первый юнешеский (Произвольный)'
    ADULT3FREE = 10, 'Третий взрослый (Произвольный)'
    ADULT2FREE = 11, 'Второй юнешеский (Произвольный)'
    ADULT1FREE = 12, 'Превый юнешеский (Произвольный)'


class Gymnast(models.Model):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='gymnasts')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='gymnasts')
    level = models.IntegerField('Розряд', choices=LevelChoice.choices)
    base_score = models.IntegerField('Общая база', null=True, blank=True)
    score = models.FloatField('Результат', null=True, blank=True)
    number = models.IntegerField('Номер', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}'

    def get_competition_name(self):
        return f'{self.user.username} ({self.number})'

    def calculate(self, set_attr=True):
        result = sum([result.result for result in self.results.all() if result.result])
        if set_attr:
            self.score = result
            self.save()
        return result

    def calculate_results(self):
        for result in self.results.all():
            result.calculate(set_result=True)

    def calculate_base(self, set_attr=True):
        result = sum([result.mark_e.e_value or 0 for result in self.results.all() if hasattr(result, 'mark_e')])
        if set_attr:
            self.base_score = result
            self.save()
        return result

    @cached_property
    def all_around_render(self):
        if self.team.competition.manager.sex == SexChoices.MALE:
            result = (
                self.results.fxm(True), self.results.ph(True), self.results.rings(True),
                self.results.vtm(True), self.results.pb(True), self.results.hb(True),
            )
        else:
            result = (
                self.results.fxw(True), self.results.ub(True),
                self.results.bb(True), self.results.vtw(True),
            )
        return result

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
