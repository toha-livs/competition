from django.views.generic import ListView

from competition.models import SubCompetition


class JudgeCompetitionListView(ListView):
    model = SubCompetition
    queryset = SubCompetition.objects.all()
    template_name = 'judge/competition_list.html'
    context_object_name = 'competitions'

    def get_queryset(self):
        competition_ids = set([judge.competition_id for judge in self.request.user.judges.all()])
        return super().get_queryset().filter(id__in=competition_ids)
