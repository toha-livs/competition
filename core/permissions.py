from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

from user.choices.user_type import UserType


def judge_check():
    def check(user):
        if user.is_authenticated:
            if user.is_superuser or user.ext.type in [UserType.JUDGE, UserType.SUPERVISOR]:
                return True
        raise PermissionDenied
    return user_passes_test(check)


def gymnast_check():
    def check(user):
        if user.is_authenticated:
            if user.is_superuser or user.ext.type == UserType.GYMNAST:
                return True
        raise PermissionDenied
    return user_passes_test(check)