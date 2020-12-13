from django.urls import path
from .views import ResultLiveView, ResultView, CompetitionResultTeam, CompetitionResultAllAround, CompetitionResultFinals

app_name = 'result'

urlpatterns = [
    path('', ResultView.as_view(), name='result'),
    path('competition/<int:competition_id>/team/', CompetitionResultTeam.as_view(), name='team'),
    path('competition/<int:competition_id>/all_around/', CompetitionResultAllAround.as_view(), name='all_around'),
    path('competition/<int:competition_id>/finals/', CompetitionResultFinals.as_view(), name='finals'),
    # path('/live/', ResultLiveView.as_view(), name='result-live'),
]