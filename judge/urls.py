from django.urls import path

from .views import JudgeCompetitionListView, JudgeHomeView, ApparatusListView, ApparatusView

app_name = 'judge'

urlpatterns = [
    path('', JudgeHomeView.as_view(), name='home'),
    path('competition-list/', JudgeCompetitionListView.as_view(), name='competiton-list'),
    path('competition/<int:competition_id>/appatatus-list/', ApparatusListView.as_view(), name='apparatus-list'),
    path('apparatus/<int:judge_id>/', ApparatusView.as_view(), name='apparatus'),
]
