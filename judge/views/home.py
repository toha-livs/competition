from django.views.generic import TemplateView


class JudgeHomeView(TemplateView):
    template_name = 'judge/home.html'

    def get_context_data(self, **kwargs):
        return {}
