from django.views.generic.base import View, TemplateView

from competition.models import Gymnast
from result.models import Result


class ResultView(TemplateView):
    template_name = 'result/result_base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) or {}
        gymnasts = Gymnast.objects.filter(team__competition__competition__name='Сдюшоры')
        context['results'] = [{'info': gymnast.user.username, 'results': gymnast.all_around_render} for gymnast in gymnasts]
        print(context['results'])
        context['columns'] = ['ФИО', "В/У", "Конь", "Кольца", "О/П", "П/Б", "Перекладина"]
        return context
