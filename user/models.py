from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from user.choices.render_type import RenderType
from user.choices.user_type import UserType

User = get_user_model()


class UserExtension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ext')
    type = models.IntegerField('Тип пользователя', choices=UserType.choices)

    render_type = models.IntegerField('Тип отображения результатов', choices=RenderType.choices, default=RenderType.BEAUTIFUL)

