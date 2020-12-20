from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import RedirectView


def render_type_view(request):
    redirect_url = request.META.get('HTTP_REFERER', '')
    if request.method == 'POST':
        request.session['render_type'] = request.POST.get('render_type')
        redirect_url = request.POST.get('redirect_url')
    return redirect(redirect_url)


class HomeView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('competition:scope-list')

    # template_name = 'home.html'
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs) or {}
    #     context['test'] = 'Hi!'
    #     return context
