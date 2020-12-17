from django.contrib.auth import get_user_model
from django.db import models

from user.choices.render_type import RenderType
from user.choices.user_type import UserType

User = get_user_model()


class UserExtension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ext')
    birthday_date = models.DateField("Дата рождения", null=True, blank=True)
    type = models.IntegerField('Тип пользователя', choices=UserType.choices)
    last_name = models.CharField('Фамилия', max_length=255, null=True, blank=True)
    middle_name = models.CharField('Отчество', max_length=255, null=True, blank=True)
    first_name = models.CharField('Имя', max_length=255, null=True, blank=True)
    position = models.CharField("Звание", max_length=255, null=True, blank=True)
    photo = models.ImageField('Фото', upload_to='photos/users/', null=True, blank=True)

    render_type = models.IntegerField(
        'Тип отображения результатов',
        choices=RenderType.choices,
        default=RenderType.BEAUTIFUL
    )

