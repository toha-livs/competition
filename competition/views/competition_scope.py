from django.db.models import Q
from django.utils import timezone
from django.views.generic import ListView

from competition.models import CompetitionScope, Gymnast


class CompetitionScopeListView(ListView):
    model = CompetitionScope
    queryset = CompetitionScope.objects.filter(
        date_start__lte=timezone.localdate() + timezone.timedelta(days=30)
    )
    template_name = 'competition/competition_scope_list.html'
    context_object_name = 'competitions'
    ordering = '-date_start'

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'search' in self.request.GET:
            search_value = self.request.GET.get('search')
            competition_ids = set([
                gymnast.team.competition.competition.competition_scope_id for gymnast in
                Gymnast.objects.filter(user__last_name__contains=search_value)
            ])
            queryset = queryset.filter(Q(name__contains=search_value) | Q(id__in=competition_ids))
        return queryset


class ExpectedCompetitionScopeListView(ListView):
    model = CompetitionScope
    queryset = CompetitionScope.objects.filter(date_start__gt=timezone.localdate())
    template_name = 'competition/expected_competition_scope_list.html'
    context_object_name = 'competitions'
    ordering = 'date_start'
