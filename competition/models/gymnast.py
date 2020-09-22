from django.contrib.auth import get_user_model
from django.db import models

from competition.models.team import Team

User = get_user_model()


class LevelChoice(models.IntegerChoices):
    JUNIOR3 = 0, 'Третий юнешеский'
    JUNIOR2 = 1, 'Второй юнешеский'
    JUNIOR1 = 2, 'Первый юнешеский'
    ADULT3 = 3, 'Третий взрослый'
    ADULT2 = 4, 'Второй юнешеский'
    ADULT1 = 5, 'Превый юнешеский'
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

    def __str__(self):
        return f'{self.user.username}'

    def calculate(self, set_attr=True):
        result = sum([result.result for result in self.results.all() if result.result])
        if set_attr:
            self.score = result
            self.save()
        return result

    def calculate_base(self, set_attr=True):
        result = sum([result.mark_e.e_value for result in self.results.all() if hasattr(result, 'mark_e')])
        if set_attr:
            self.score = result
            self.save()
        return result

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
