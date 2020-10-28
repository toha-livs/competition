from django.urls import path

from .views import JudgeCompetitionListView, JudgeHomeView, ApparatusListView, SupervisorView
from .views.apparatus_d import ApparatusDView
from .views.apparatus_e import ApparatusEView, ApparatusEResultView, SetTempGymnastView

app_name = 'judge'

urlpatterns = [
    path('', JudgeHomeView.as_view(), name='home'),
    path('competition-list/', JudgeCompetitionListView.as_view(), name='competiton-list'),
    path('competition/<int:competition_id>/appatatus-list/', ApparatusListView.as_view(), name='apparatus-list'),
    path('supervisor/<int:competition_id>/', SupervisorView.as_view(), name='supervisor'),
    path('apparatus-d/<int:judge_id>/', ApparatusDView.as_view(), name='apparatus-d'),
    path('apparatus-e/<int:judge_id>/', ApparatusEView.as_view(), name='apparatus-e'),
    path('apparatus-e-result/<int:judge_id>/', ApparatusEResultView.as_view(), name='apparatus-e-result'),
    path('apparatus-e-set-gymnast/<int:judge_id>/', SetTempGymnastView.as_view(), name='apparatus-e-set-gymnast'),
]
