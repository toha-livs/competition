from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from judge.models import Judge


class ApparatusListView(TemplateView):
    template_name = 'judge/apparatus_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) or {}
        context['apparatuses'] = Judge.objects.filter(
            user=self.request.user,
            competition=self.kwargs.get('competition_id', None)
        )
        return context

    def get(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        response = self.render_to_response(context)
        if context['apparatuses'].count() == 1:
            response = redirect(reverse('judge:apparatus', args=[context['apparatuses'].first().pk]))
        return response

