from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from competition.models import SubCompetition


class SupervisorView(TemplateView):
    template_name = 'judge/supervisor.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.super_competitions.filter(id=kwargs.get('competition_id', None)).exists():
            return super().dispatch(request, *args, **kwargs)
        return PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) or {}
        context['competition'] = SubCompetition.objects.filter(id=kwargs.get('competition_id', None)).first()
        return context

    def post(self, request, *args, **kwargs):
        competition = SubCompetition.objects.filter(id=kwargs.get('competition_id', None)).first()
        if competition:
            if 'action' in request.POST:
                if request.POST.get('action') == 'start':
                    competition.manager.rotate()
                competition.active = True if request.POST.get('action') == 'start' else False
                competition.save()
            elif 'rotation' in request.POST:
                competition.manager.rotate(int(request.POST.get('rotation')))
        return redirect(reverse('judge:supervisor', args=[competition.pk]))
