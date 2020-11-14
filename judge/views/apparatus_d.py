import json

from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseForbidden
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

    def __init__(self, *args, **kwargs):
        self.object = None
        self.temp = None
        self.competition = None
        self.result = None
        self.mark_d = None
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        judge = self.get_object()
        if judge.judge_type == JudgeTypeChoice.D and request.user == judge.user:
            self.object = self.get_object()
            self.competition = self.object.competition
            if self.competition.active:
                self.temp = TempJudgeBrigadeManager.objects.get_or_create(
                    apparatus=self.object.apparatus,
                    sub_competition=self.competition
                )[0]
                if self.temp.temp_gymnast:
                    self.result = Result.objects.get_or_create(
                        gymnast=self.temp.temp_gymnast,
                        apparatus=self.object.apparatus
                    )[0]
                    self.mark_d = MarkD.objects.get_or_create(judge=self.object, result=self.result)[0]
                return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def _get_temp_json(self):
        if team := getattr(self.temp, 'temp_team', None):
            team = getattr(team, 'name', None)
        if gymnast := getattr(self.temp, 'temp_gymnast', None):
            gymnast = f'{gymnast.user.last_name} {gymnast.user.first_name}'
        return {
            'team': team,
            'gymnast': gymnast,
            'writable': self.temp.writable
        }

    def get(self, request, *args, **kwargs):
        context = dict()
        _object = self.object
        competition = _object.competition
        if self.request.is_ajax():
            context['temp'] = self._get_temp_json()
            response = JsonResponse(context, status=200)
        else:
            context['object'] = _object
            context['competition'] = competition
            context['temp'] = self.temp
            if self.temp.temp_gymnast:
                context['mark_d'] = self.mark_d
            response = render(request, self.template_name, context)
        return response

    def post(self, request, *args, **kwargs):
        status = 403
        if request.is_ajax():
            data = json.loads(request.body.decode('utf-8'))
            if self.temp.temp_gymnast:
                if mark_d := MarkD.objects.filter(
                    judge=self.object,
                    result__gymnast=self.temp.temp_gymnast,
                    result__apparatus=self.object.apparatus
                ).first():
                    mark_d.value = data['value']
                    mark_d.comment = data['comment']
                    mark_d.save()
                    status = 200
        return JsonResponse({'status': status})

    # def _get_temp(self, judge):
    #     return TempJudgeBrigadeManager.objects.get(apparatus=judge.apparatus, sub_competition=self.competition)
    #
    # def _get_mark(self, judge):
    #     temp = self._get_temp(judge)
    #     result = Result.objects.filter(apparatus=judge.apparatus, gymnast=temp.temp_gymnast).first()
    #     if result:
    #         return
    #     return temp


