from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import cached_property

from common.models import BaseNameModel
from competition.choices.apparatus import ApparatusChoices
from competition.choices.calculate_mark import CalculateMarkTypeChoices
from competition.choices.sex import SexChoices
from competition.choices.sub_competition_type import SubCompetitionTypeChoices
from competition.choices.competition_type import CompetitionTypeChoices
from competition.choices.level import Level

User = get_user_model()


class CompetitionScope(BaseNameModel, models.Model):
    date_start = models.DateField("Дата начала", null=True, blank=True)
    level = models.IntegerField("Уровень", choices=Level.choices, default=Level.REGION)
    date_end = models.DateField('Дата окончания', null=True, blank=True)

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

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

    def calculate(self):
        for sub in self.subs.all():
            for team in sub.teams.all():
                for gymnast in team.gymnasts.all():
                    for result in gymnast.results.all():
                        result.calculate(set_result=True)
                    gymnast.calculate(set_attr=True)
                    gymnast.calculate_base(set_attr=True)

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'


class SubCompetition(BaseNameModel, models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='subs')
    date = models.DateTimeField('Дата проведения', null=True)
    active = models.BooleanField('Активны', default=False)
    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='super_competitions'
    )

    def calculate(self):
        for team in self.teams.all():
            for gym in team.gymnasts.all():
                gym.calculate(set_attr=True)
                gym.calculate_base(set_attr=True)

    def __str__(self):
        return f'{self.competition.competition_scope.name} | {self.competition.name} | {self.name}'

    class Meta:
        verbose_name = 'Поток'
        verbose_name_plural = 'Потоки'


class SubCompetitionManager(models.Model):
    sub_competition = models.OneToOneField(SubCompetition, on_delete=models.CASCADE, related_name='manager')
    sex = models.IntegerField('Пол', choices=SexChoices.choices, default=SexChoices.MALE)
    rotation = models.IntegerField('Ротейшен', default=0)

    @property
    def base_apparatus_count(self):
        count = 4 if self.sex == SexChoices.FEMALE else 6
        count += self.sub_competition.settings.day_off
        return count

    def get_team(self, judge):
        current_apparatus = (judge.apparatus + self.rotation - 1) % self.base_apparatus_count
        return self.sub_competition.teams.filter(start_apparatus=current_apparatus).first()

    def set_temp_teams(self):
        self.set_temp_managers()
        for team in self.sub_competition.teams.all():
            team.set_temp_judges_brigade(manager=self)

    def set_temp_managers(self):
        temp_judge_brigade_manager_model = apps.get_model(app_label='competition', model_name='TempJudgeBrigadeManager')
        for apparatus in range(1, self.base_apparatus_count + 1):
            temp, created = temp_judge_brigade_manager_model.objects.get_or_create(
                sub_competition=self.sub_competition,
                apparatus=apparatus
            )
            if created is False:
                temp.temp_team = None
                temp.temp_gymnast = None
                temp.save()

    @property
    def settings(self):
        return self.sub_competition.settings

    @property
    def max_rotations(self):
        return self.base_apparatus_count + self.settings.day_off

    # def

    def rotate(self, rotation=None):
        if rotation is None:
            rotation = 0
            self.set_temp_managers()
        self.rotation = rotation
        self.save()
        self.set_temp_teams()

    class Meta:
        verbose_name = 'Поток (Менеджер)'
        verbose_name_plural = 'Потоки (Менеджер)'


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
        verbose_name = 'Настройки потока'
        verbose_name_plural = 'Настройки потоков'
