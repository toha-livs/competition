from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse
from django.views.generic import CreateView

from user.choices.user_type import UserType


class LoginView(DjangoLoginView):

    def form_valid(self, form):
        self.user = form.user_cache
        return super().form_valid(form)

    def get_success_url(self):
        success_url = super().get_success_url()
        if hasattr(self.user, 'ext') and self.user.ext.type in [UserType.JUDGE, UserType.SUPERVISOR]:
            success_url = reverse('judge:home')
        return success_url


class RegistrationView(CreateView):
    pass



