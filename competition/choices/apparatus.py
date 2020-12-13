from django.db.models import IntegerChoices

from competition.choices.sex import SexChoices


class ApparatusChoices(IntegerChoices):
    FXM = 1, 'Вольные упражнения (М)'
    PH = 2, 'Конь'
    RINGS = 3, 'Кольца'
    VTM = 4, 'Опорный прыжок (М)'
    PB = 5, 'Паралельные брусья'
    HB = 6, 'Перекладина'
    DAY_OFF_M = 7, 'Выходной'
    DAY_OFF2_M = 8, 'Выходной 2'

    FXW = 11, 'Вольные упражнения (Ж)'
    BB = 12, 'Бревно'
    UB = 13, 'Разновысокие брусья'
    VTW = 14, 'Опорный прыжок (Ж)'
    DAY_OFF_W = 15, 'Выходной'
    DAY_OFF2_W = 16, 'Выходной 2'

    @classmethod
    def get_competition_choices(cls, sub_competition, day_off=True):
        result = list(filter(lambda x: x[0] < 10, cls.choices))
        if sub_competition.manager.sex == SexChoices.FEMALE:
            result = list(filter(lambda x: x[0] > 10, cls.choices))
        if day_off is False:
            result = list(filter(lambda x: x[0] not in [15, 16, 7, 8], result))
        return result
