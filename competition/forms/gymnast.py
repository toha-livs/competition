from django import forms
from django.contrib.auth import get_user_model

from competition.models import Gymnast
from user.choices.user_type import UserType

User = get_user_model()


class GymnastForm(forms.ModelForm):

    class Meta:
        model = Gymnast
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(ext__type=UserType.GYMNAST)