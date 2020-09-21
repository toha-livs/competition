from django.db.models import IntegerChoices


class RenderType(IntegerChoices):
    TABLE = 0, 'Таблица'
    BEAUTIFUL = 1, 'Красиво'
