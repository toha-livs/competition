from django.db import models

from competition.choices.apparatus import ApparatusChoices
from competition.models.team import Team
from competition.models.gymnast import Gymnast
from competition.models.subcompetition import SubCompetition


class TempJudgeBrigadeManager(models.Model):
    sub_competition = models.ForeignKey(SubCompetition, on_delete=models.SET_NULL, null=True, blank=True, related_name='temp_judge_managers')
    apparatus = models.IntegerField('Снараяд', choices=ApparatusChoices.choices)
    temp_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='temps')
    temp_gymnast = models.ForeignKey(Gymnast, on_delete=models.SET_NULL, null=True, blank=True, related_name='temps')
    writable = models.BooleanField('Изеняемо', default=False)

    class Meta:
        verbose_name = 'Временный менеджер судей'
        verbose_name_plural = 'Временные менеджеры судей'

    # def save(self, *args, **kwargs):
    #     if self.writable is True:
    #         super().save(*args, **kwargs)
    #         self.writable = False


