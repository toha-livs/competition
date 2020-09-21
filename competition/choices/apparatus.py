from django.db.models import IntegerChoices


class ApparatusChoices(IntegerChoices):
    FXW = 0, 'Вольные упражнения (Ж)'
    FXM = 1, 'Вольные упражнения (М)'
    VTW = 2, 'Опорный прыжок (Ж)'
    VTM = 3, 'Опорный прыжок (М)'
    PH = 4, 'Конь'
    RINGS = 5, 'Кольца'
    PB = 6, 'Паралельные брусья'
    HB = 7, 'Перекладина'
    UB = 8, 'Разновысокие брусья'
    BB = 9, 'Бревно'
    DAY_OFF = 10, 'Выходной'
    DAY_OFF2 = 11, 'Выходной 2'
