from django.contrib.auth import get_user_model
from django.db import models

from competition.choices.apparatus import ApparatusChoices
from competition.models.subcompetition import SubCompetition

User = get_user_model()


class JudgeTypeChoice(models.IntegerChoices):
    E = 0, 'База'
    D = 1, 'Сбавки'


class Judge(models.Model):
    competition = models.ForeignKey(
        SubCompetition,
        on_delete=models.CASCADE,
        related_name='judges',
        related_query_name='judges'
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='judges')
    apparatus = models.IntegerField('Снараяд', choices=ApparatusChoices.choices)
    judge_type = models.IntegerField('Тип судейства', choices=JudgeTypeChoice.choices)

    def __str__(self):
        return f'{self.user.username} ({self.get_apparatus_display()}:{self.get_judge_type_display()})'

    class Meta:
        verbose_name = 'Судья'
        verbose_name_plural = 'Судьи'
