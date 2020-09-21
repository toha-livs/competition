from django import forms
from django.contrib.auth import get_user_model

from competition.models import Judge
from user.choices.user_type import UserType

User = get_user_model()


class JudgeForm(forms.ModelForm):

    class Meta:
        model = Judge
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(ext__type=UserType.JUDGE)
