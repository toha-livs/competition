from django.db.models import IntegerChoices


class Level(IntegerChoices):
    INTERNATIONAL = 0, 'Международные'
    UKRAINE = 1, 'Всеукраинские'
    REGION = 2, 'Региональные'
