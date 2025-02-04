from django.apps import apps
from django.db import models
from django.utils.functional import cached_property

from common.models import BaseNameModel
from competition.choices.apparatus import ApparatusChoices
from competition.models.subcompetition import SubCompetition


class Team(BaseNameModel, models.Model):
    competition = models.ForeignKey(SubCompetition, on_delete=models.CASCADE, related_name='teams')
    base_score = models.FloatField('Общая база', null=True, blank=True)
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

    def calculate_base(self, set_attr=True):
        register_by = self.competition.competition.times_register_by
        result = 0.0
        count = 0
        for gymnast in self.gymnasts.all().order_by('-base_score'):
            if count < register_by and gymnast.base_score:
                count += 1
                result += gymnast.base_score
        if set_attr:
            self.base_score = result
            self.save()
        return result

    def set_temp_judges_brigade(self, manager):
        temp_judge_brigade_manager_model = apps.get_model(app_label='competition', model_name='TempJudgeBrigadeManager')
        apparatus = self.start_apparatus + manager.rotation
        if apparatus > manager.max_rotations:
            apparatus %= manager.max_rotations
        if temp := temp_judge_brigade_manager_model.objects.filter(
            sub_competition=manager.sub_competition,
            apparatus=apparatus
        ).first():
            temp.temp_team = self
            temp.save()

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
