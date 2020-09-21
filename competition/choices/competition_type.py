from django.db.models import IntegerChoices


class CompetitionTypeChoices(IntegerChoices):
    QUALIFICATION = 0, 'Квалификация'
    ALL_AROUND = 1, 'Многоборье'
    TEAMS = 3, 'Командные'
    FINALS = 2, 'Финалы'
