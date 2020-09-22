from django.views.generic import TemplateView
from django.views.generic.detail import BaseDetailView

from judge.models import Judge
from judge.models.judge import JudgeTypeChoice


class ApparatusView(BaseDetailView, TemplateView):
    pk_url_kwarg = 'judge_id'
    queryset = Judge.objects.all()
    model = Judge

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) or {}

        return context

    def get_template_names(self):
        judge = self.get_object()
        if judge.judge_type == JudgeTypeChoice.E:
            return 'judge/apparatus_e.html'
        elif judge.judge_type == JudgeTypeChoice.D:
            return 'judge/apparatus_d.htm'
        raise ValueError('Judge instance is not in ["E", "D"] types')
