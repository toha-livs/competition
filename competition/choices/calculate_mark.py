from django.db.models import IntegerChoices


class CalculateMarkTypeChoices(IntegerChoices):
    BY_1 = 1, 'По одному'
    BY_2 = 2, 'По двум'
    BY_3 = 3, 'По трем'
    BY_4 = 4, 'По четырем'
    BY_5 = 5, 'По пятерым'
    BY_6 = 6, 'По шестерым'
    BY_7 = 7, 'По семерым'
