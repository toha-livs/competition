import json

from django.core.exceptions import PermissionDenied
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.detail import BaseDetailView

from competition.models import Gymnast, TempJudgeBrigadeManager
from judge.models.judge import JudgeTypeChoice, Judge
from result.models import Result


class BaseJudgeEView(BaseDetailView):
    pk_url_kwarg = 'judge_id'
    queryset = Judge.objects.all()
    model = Judge

    def dispatch(self, request, *args, **kwargs):
        judge = self.get_object()
        if judge.judge_type == JudgeTypeChoice.E and request.user == judge.user:
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


class ApparatusEView(BaseJudgeEView):
    template_name = 'judge/apparatus_e.html'

    def _get_result(self):
        result = None
        if self.temp.temp_gymnast:
            result, created = Result.objects.get_or_create(
                apparatus=self.object.apparatus,
                gymnast=self.temp.temp_gymnast
            )
        return result

    def get(self, request, *args, **kwargs):
        context = dict()
        context['temp'] = self.temp
        context['judge'] = self.get_object()
        result = self._get_result()
        if result:
            context['mark_e'] = self._get_result().mark_e
            context['marks_d'] = self._get_result().marks_d.all()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pass


class SetTempGymnastView(BaseJudgeEView):
    http_method_names = 'post',

    def post(self, request, *args, **kwargs):
        status = 400
        if request.is_ajax():
            data = json.loads(request.body.decode('utf-8'))
            gymnast = get_object_or_404(Gymnast, pk=data.get('gymnast_id', None))
            self.temp.temp_gymnast = gymnast
            self.temp.save()
            status = 200
        return JsonResponse({'status': status})


class ApparatusEResultView(BaseJudgeEView):
    http_method_names = 'get'

    def _get_result(self):
        result = None
        if self.temp.temp_gymnast:
            result, created = Result.objects.get_or_create(
                apparatus=self.object.apparatus,
                gymnast=self.temp.temp_gymnast
            )
        return result

    def get(self, request, *args, **kwargs):
        context = {'status': 404}
        if request.is_ajax() and self.temp.temp_gymnast:
            context['status'] = 200
            context['marks'] = []
            for mark in self._get_result().marks_d.all():
                context['marks'].append(model_to_dict(mark, exclude=['id']))
        return JsonResponse(context)