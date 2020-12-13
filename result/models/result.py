from math import ceil

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg

from common.models import BaseDateTimeModel
from competition.choices.apparatus import ApparatusChoices
from competition.models.gymnast import Gymnast
from judge.models.judge import Judge

User = get_user_model()


class ResultManager(models.Manager):

    def fxm(self, one=True, **kwargs):
        result = self.get_queryset(**kwargs).filter(apparatus=ApparatusChoices.FXM)
        if one:
            result = result.first()
        return result

    def ph(self, one=True, **kwargs):
        result = self.get_queryset(**kwargs).filter(apparatus=ApparatusChoices.PH)
        if one:
            result = result.first()
        return result

    def rings(self, one=True, **kwargs):
        result = self.get_queryset(**kwargs).filter(apparatus=ApparatusChoices.RINGS)
        if one:
            result = result.first()
        return result

    def vtm(self, one=True, **kwargs):
        result = self.get_queryset(**kwargs).filter(apparatus=ApparatusChoices.VTM)
        if one:
            result = result.first()
        return result

    def pb(self, one=True, **kwargs):
        result = self.get_queryset(**kwargs).filter(apparatus=ApparatusChoices.PB)
        if one:
            result = result.first()
        return result

    def hb(self, one=True, **kwargs):
        result = self.get_queryset(**kwargs).filter(apparatus=ApparatusChoices.HB)
        if one:
            result = result.first()
        return result

    def fxw(self, one=True, **kwargs):
        result = self.get_queryset(**kwargs).filter(apparatus=ApparatusChoices.FXW)
        if one:
            result = result.first()
        return result

    def ub(self, one=True, **kwargs):
        result = self.get_queryset(**kwargs).filter(apparatus=ApparatusChoices.UB)
        if one:
            result = result.first()
        return result

    def bb(self, one=True, **kwargs):
        result = self.get_queryset(**kwargs).filter(apparatus=ApparatusChoices.BB)
        if one:
            result = result.first()
        return result

    def vtw(self, one=True, **kwargs):
        result = self.get_queryset(**kwargs).filter(apparatus=ApparatusChoices.VTW)
        if one:
            result = result.first()
        return result


class Result(models.Model):
    apparatus = models.IntegerField('Снаряд', choices=ApparatusChoices.choices)
    gymnast = models.ForeignKey(Gymnast, on_delete=models.CASCADE, related_name='results')
    result = models.FloatField('Результат', null=True, blank=True)

    objects = ResultManager()

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
        unique_together = [['apparatus', 'gymnast']]

    def calculate(self, set_result=True):
        max_marks = self.gymnast.team.competition.settings.calculate_mark_type
        result = 0
        base_mark = 0
        if hasattr(self, 'mark_e'):
            base_mark = (self.mark_e.e_value or 0) + (self.mark_e.base_value or 0)
        decreases_marks = self.marks_d.get_avgs(max_marks=max_marks).aggregate(Avg('value')).get('value__avg') or 0
        if base_mark > (10 - decreases_marks):
            result = base_mark - (10 - decreases_marks)
        if set_result:
            self.result = result
            self.save()
        return result


class Comment(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='comments', related_query_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Комментарий')
    create_dt = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий к результату'
        verbose_name_plural = 'Комментарии к результатам'


class MarkE(BaseDateTimeModel, models.Model):
    result = models.OneToOneField(Result, on_delete=models.CASCADE, related_name='mark_e')
    judge = models.ForeignKey(Judge, on_delete=models.SET_NULL, null=True, blank=True, related_name='marks_e')
    e_value = models.FloatField('Оценка', null=True)
    base_value = models.FloatField('Судейство с', default=10.0)
    comment = models.TextField('Комментарий', null=True, blank=True)

    @property
    def value(self):
        return self.base_value or 0 + self.e_value or 0

    class Meta:
        verbose_name = 'Оценка E'
        verbose_name_plural = 'Оценки E'


class MarkDManager(models.Manager):

    def get_avgs(self, max_marks=None, **kwargs):
        result = self.get_queryset(**kwargs)
        if max_marks:
            else_marks = result.count() - max_marks
            if else_marks > 0:
                front_del = ceil(else_marks / 2)
                end_del = result.count() - (else_marks - front_del)
                end_del = end_del if else_marks % 2 == 0 else end_del - 1
                result = result[front_del:end_del if end_del > front_del else result.count()]
        return result


class MarkD(BaseDateTimeModel, models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='marks_d')
    judge = models.ForeignKey(Judge, on_delete=models.SET_NULL, null=True, blank=True, related_name='marks_d')
    value = models.FloatField('Оценка', null=True)
    comment = models.TextField('Комментарий', null=True, blank=True)

    objects = MarkDManager()

    class Meta:
        verbose_name = 'Оценка D'
        verbose_name_plural = 'Оценки D'
