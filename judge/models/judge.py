from django import apps
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.functional import cached_property

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

    @property
    def url(self):
        judge_type = 'd' if self.judge_type == JudgeTypeChoice.D else 'e'
        return reverse(f'judge:apparatus-{judge_type}', args=[self.pk])


    @cached_property
    def comments_count(self):
        result_model = apps.apps.get_model(app_label='result', model_name='Result')
        comments = 0
        for result in result_model.objects.filter(
                Q(comments__isnull=False, marks_d__judge__user=self.user) |
                Q(comments__isnull=False, mark_e__judge__user=self.user)
        ):
            comments += result.comments.count()
        return comments

    class Meta:
        verbose_name = 'Судья'
        verbose_name_plural = 'Судьи'
