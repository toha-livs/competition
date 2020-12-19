from django.views.generic import ListView
from competition.models import Competition, Gymnast
from django.shortcuts import get_object_or_404
from django_user_agents.utils import get_user_agent
from competition.models.gymnast import LevelChoice


class CompetitionResultAllAround(ListView):
    template_name = 'result/all_around.html'
    queryset = Gymnast.objects.none()

    paginate_by = 10

    filtering = {
        'team': 'team_id',
        'year': 'user__ext__birthday_date__year',
        'level': 'level',
    }

    def get_teams(self):
        result = []
        for sub in self.competition.subs.all():
            result.extend([team for team in sub.teams.all()])
        return result

    def get_years(self):
        result = []
        for i in self.object_list:
            date = getattr(i.user.ext, 'birthday_date')
            if date:
                result.append(date.strftime('%Y'))
        return set(result)

    def get_filtering(self, queryset):
        filter_kwargs = dict()
        for _filter in self.filtering:
            if _filter in self.request.GET:
                filter_kwargs[self.filtering[_filter]] = self.request.GET.get(_filter)
        return queryset.filter(**filter_kwargs)

    def get_queryset(self):
        competition = get_object_or_404(Competition, pk=self.kwargs.get('competition_id', None))
        self.competition = competition
        queryset = Gymnast.objects.filter(
            team__competition__competition=competition
        ).order_by('level', '-score')
        queryset = self.get_filtering(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) or dict()
        context['competition'] = self.competition
        context['competition_sex'] = self.competition.subs.last().manager.sex
        context['mobile'] = True
        context['user_agent'] = get_user_agent(self.request)
        # if self.kwargs
        context['filters'] = [
            {
                'title': 'Команда',
                'field_name': 'team',
                'choices': tuple([(team.pk, team.name) for team in self.get_teams()])
            },
            {
                'title': 'Год рождения',
                'field_name': 'year',
                'choices': tuple([(int(year), year) for year in self.get_years()])
            },
            {
                'title': 'Розряд',
                'field_name': 'level',
                'choices': LevelChoice.choices
            },
        ]
        return context

