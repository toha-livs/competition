from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, TemplateView

from competition.choices.competition_type import CompetitionTypeChoices
from competition.models import Competition, Team


class CompetitionListView(ListView):
    template_name = 'competition/competition_list.html'
    context_object_name = 'competitions'
    model = Competition
    queryset = Competition.objects.all()
    ordering = '-date'

    def get_queryset(self):
        return Competition.objects.filter(competition_scope_id=self.kwargs.get('scope_id'))

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        if self.get_queryset().count() == 1:
            response = redirect(reverse('competition:competition-detail', args=[self.get_queryset().first().id]))
        return response


class CompetitionDetailView(TemplateView):
    template_name = 'competition/competition_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) or {}
        competition = get_object_or_404(Competition, pk=kwargs.get('competition_id'))
        context['results'] = []
        context['competition'] = competition
        if context['competition'].competition_type == CompetitionTypeChoices.TEAMS:
            competition_ids = (sub.id for sub in competition.subs.all())
            context['results'] = Team.objects.filter(competition__in=competition_ids).order_by('-score')
        return context
