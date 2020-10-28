from django.db.models import IntegerChoices


class SexChoices(IntegerChoices):
    MALE = 1, 'Мужчины'
    FEMALE = 2, 'Женщины'
