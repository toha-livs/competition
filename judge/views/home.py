from django.db.models import Q
from django.utils import timezone
from django.views.generic import TemplateView

from competition.models import SubCompetition
from user.forms import UserExtensionForm


class JudgeHomeView(TemplateView):
    http_method_names = ['get', 'post']
    template_name = 'judge/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) or {}
        date_now = timezone.localdate()
        date_range = [date_now - timezone.timedelta(days=10), date_now + timezone.timedelta(days=10)]
        competitions = [comp.pk for comp in SubCompetition.objects.filter(
            Q(supervisor=self.request.user) |
            Q(supervisor=self.request.user, date__gte=date_now, active=False) |
            Q(supervisor=self.request.user, date__lte=date_now, active=False) |
            Q(judges__user=self.request.user, active=True) |
            Q(judges__user=self.request.user, date__gte=date_now, active=False) |
            Q(judges__user=self.request.user, date__lte=date_now, active=False)
        )]
        context['competitions'] = SubCompetition.objects.filter(id__in=set(competitions))

        context['judge_history'] = self.request.user.judges.all().order_by('-competition__date')[:10]
        context.setdefault('user_ext_form', UserExtensionForm(instance=self.request.user.ext))
        return context

    def post(self, request, *args, **kwargs):
        _kwargs = dict()
        form = UserExtensionForm(request.POST, files=request.FILES, instance=request.user.ext)
        if form.is_valid():
            print('success')
            form.save()
        else:
            print(form.errors)
            _kwargs['user_ext_form'] = form
        return self.get(request, **_kwargs)


