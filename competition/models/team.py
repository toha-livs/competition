from django.db import models
from django.utils.functional import cached_property

from common.models import BaseNameModel
from competition.choices.apparatus import ApparatusChoices
from competition.models.subcompetition import SubCompetition


class Team(BaseNameModel, models.Model):
    competition = models.ForeignKey(SubCompetition, on_delete=models.CASCADE, related_name='teams')
    score = models.FloatField('Результат', null=True, blank=True)
    start_apparatus = models.IntegerField('Начальный снаряд', choices=ApparatusChoices.choices, default=ApparatusChoices.FXM)

    def calculate(self, set_attr=True):
        register_by = self.competition.competition.times_register_by
        result = 0.0
        count = 0
        for gymnast in self.gymnasts.all().order_by('-score'):
            if count < register_by and gymnast.score:
                count += 1
                result += gymnast.score
        if set_attr:
            self.score = result
            self.save()
        return result

    def team_base(self):
        return 35.6

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
