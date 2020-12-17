from django.urls import reverse
from django.views.generic import RedirectView


class HomeView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('competition:scope-list')

    # template_name = 'home.html'
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs) or {}
    #     context['test'] = 'Hi!'
    #     return context
