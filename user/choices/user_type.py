from django.db.models import IntegerChoices


class UserType(IntegerChoices):
    ADMIN = 0, 'Админ'
    SUPERVISOR = 1, 'Супервайзер'
    JUDGE = 2, 'Судья'
    GYMNAST = 3, 'Гимнаст'
    VIEWER = 4, 'Зритель'
