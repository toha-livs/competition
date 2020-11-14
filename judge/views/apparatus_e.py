import json
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.views.generic.detail import BaseDetailView

from competition.models import Gymnast, TempJudgeBrigadeManager
from judge.models.judge import JudgeTypeChoice, Judge
from result.models import Result, MarkE


class BaseJudgeEView(BaseDetailView):
    pk_url_kwarg = 'judge_id'
    queryset = Judge.objects.all()
    model = Judge

    def __init__(self, *args, **kwargs):
        self.object = None
        self.temp = None
        self.competition = None
        self.result = None
        self.mark_e = None
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):

        self.object = self.get_object()
        if self.object.judge_type == JudgeTypeChoice.E and request.user == self.object.user:
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
                    self.mark_e = MarkE.objects.get_or_create(judge=self.object, result=self.result)[0]
                return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()


class ApparatusEView(BaseJudgeEView):
    template_name = 'judge/apparatus_e.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['temp'] = self.temp
        context['judge'] = self.object
        context['judge_d'] = self.competition.judges.filter(
            judge_type=JudgeTypeChoice.D,
            apparatus=self.object.apparatus,
            user=request.user
        ).first()
        context['result'] = self.result
        if self.result:
            context['mark_e'] = getattr(self.result, 'mark_e', {})
            context['marks_d'] = self.result.marks_d.all()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        status = 400
        result = None
        if request.is_ajax():
            data = json.loads(request.body.decode('utf-8'))
            if self.result:
                mark, created = MarkE.objects.get_or_create(result_id=self.result.id, judge=self.object)
                mark.e_value = data['e_value']
                mark.comment = data['comment']
                mark.base_value = data['base_value']
                mark.save()
                result = self.result.calculate(set_result=True)
        return JsonResponse({'status': status, 'result': result})


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

    @staticmethod
    def get_mark_e_info(mark):
        result = dict()
        result['judge'] = mark.judge.user.username
        result['value'] = mark.value
        result['comment'] = mark.comment
        return result

    def get(self, request, *args, **kwargs):
        context = {'status': 404}
        if request.is_ajax() and self.temp.temp_gymnast:
            context['status'] = 200
            context['marks'] = []
            context['score'] = self.result.calculate() if self.result.result is None else self.result.result
            for mark in self.result.marks_d.all():
                context['marks'].append(self.get_mark_e_info(mark))
        return JsonResponse(context)
