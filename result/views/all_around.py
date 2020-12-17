from django.views.generic.base import TemplateView

from competition.choices.apparatus import ApparatusChoices
from competition.models import Competition, Gymnast
from django.shortcuts import get_object_or_404

from result.utils.get_all_around_result import get_all_around_result


class CompetitionResultAllAround(TemplateView):
    template_name = 'result/all_around.html'

    def get_context_data(self, **kwargs):
        competition = get_object_or_404(Competition, pk=kwargs.get('competition_id', None))
        context = super().get_context_data(**kwargs) or dict()
        competition.calculate()
        context['competition'] = competition
        context['competition_sex'] = competition.subs.last().manager.sex
        context['result'] = Gymnast.objects.filter(
            team__competition__competition=competition
        # ).order_by('team', 'number')
        ).order_by('level', '-score')
        return context

