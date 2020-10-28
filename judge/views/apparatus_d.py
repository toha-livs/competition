from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.detail import BaseDetailView

from competition.models import TempJudgeBrigadeManager
from judge.models import Judge
from judge.models.judge import JudgeTypeChoice
from result.models import MarkD, Result


class ApparatusDView(BaseDetailView):
    pk_url_kwarg = 'judge_id'
    queryset = Judge.objects.all()
    model = Judge
    template_name = 'judge/apparatus_d.html'

    def dispatch(self, request, *args, **kwargs):
        judge = self.get_object()
        if judge.judge_type == JudgeTypeChoice.D and request.user == judge.user:
            self.object = self.get_object()
            self.competition = self.object.competition
            if self.competition.active:
                self.temp, created = TempJudgeBrigadeManager.objects.get_or_create(
                    apparatus=self.object.apparatus,
                    sub_competition=self.competition
                )
                return super().dispatch(request, *args, **kwargs)
        else:
            return PermissionDenied

    @staticmethod
    def _get_temp_json(temp):
        if team := getattr(temp, 'temp_team', None):
            team = getattr(team, 'name', None)
        if gymnast := getattr(temp, 'temp_gymnast', None):
            gymnast = f'{gymnast.user.last_name} {gymnast.user.first_name}'
        return {
            'team': team,
            'gymnast': gymnast,
            'writable': temp.writable
        }

    def _get_temp(self, judge):
        return TempJudgeBrigadeManager.objects.get(apparatus=judge.apparatus, sub_competition=self.competition)

    def _get_mark(self, judge):
        temp = self._get_temp(judge)
        result = Result.objects.filter(apparatus=judge.apparatus, gymnast=temp.temp_gymnast).first()
        if result:
            return
        return temp

    def get(self, request, *args, **kwargs):
        context = dict()
        _object = self.object
        competition = _object.competition
        if self.request.is_ajax():
            context['temp'] = self._get_temp_json(TempJudgeBrigadeManager.objects.get(
                apparatus=_object.apparatus,
                sub_competition=competition
            ))
            response = JsonResponse(context, status=200)
        else:
            context['object'] = _object
            temp_manager, created = TempJudgeBrigadeManager.objects.get_or_create(
                apparatus=_object.apparatus,
                sub_competition=competition)
            context['competition'] = competition
            context['temp'] = temp_manager
            if temp_manager.temp_gymnast:
                result, created = Result.objects.get_or_create(
                    gymnast=temp_manager.temp_gymnast,
                    apparatus=_object.apparatus
                )
                context['mark_d'], created = MarkD.objects.get_or_create(
                    judge=_object,
                    result=result
                )
            response = render(request, self.template_name, context)
        return response

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.body.decode('utf-8')
            _object = self.get_object()
            temp = TempJudgeBrigadeManager.objects.get(
                apparatus=_object.apparatus,
                sub_competition=_object.competition
            )
            if temp.writable and temp.temp_gymnast:
                if mark_d := MarkD.objects.filter(
                    judge=_object,
                    result__gymnast=temp.temp_gymnast,
                    result__apparatus=_object.apparatus
                ).first():
                    mark_d.value = data['value']
                    mark_d.comment = data['comment']
                return JsonResponse({'status': 200})
            else:
                return JsonResponse({'status': 403})





