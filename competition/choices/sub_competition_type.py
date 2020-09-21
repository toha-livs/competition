from django.db.models import IntegerChoices


class SubCompetitionTypeChoices(IntegerChoices):
    DEFAULT = 0, 'Стандартные'
    FINALS = 1, 'Финалы'
