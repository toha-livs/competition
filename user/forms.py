from django import forms

from user.models import UserExtension


class UserExtensionForm(forms.ModelForm):

    class Meta:
        model = UserExtension
        fields = '__all__'
        exclude = 'user', 'render_type', 'type',
