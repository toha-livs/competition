from dal import autocomplete
from django import forms
from result.models import Result


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = "__all__"
        widgets = {
            'gymnast': autocomplete.ModelSelect2(url='competition:gymnast-autocomplete')
        }