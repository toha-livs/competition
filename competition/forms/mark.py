from django import forms

from competition.models import MarkD, MarkE, Judge
from competition.models.judge import JudgeTypeChoice


class MarkDForm(forms.ModelForm):
    class Meta:
        model = MarkD
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['judge'].queryset = Judge.objects.filter(judge_type=JudgeTypeChoice.D)


class MarkEForm(forms.ModelForm):
    class Meta:
        model = MarkE
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['judge'].queryset = Judge.objects.filter(judge_type=JudgeTypeChoice.E)
