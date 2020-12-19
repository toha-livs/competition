from django.urls import path

from .views import (
    CompetitionScopeListView, CompetitionListView,
    ExpectedCompetitionScopeListView, CompetitionDetailView,
)
from .views.autocomplete import GymnastAutocomplete

app_name = 'competition'


urlpatterns = [
    path('', CompetitionScopeListView.as_view(), name='scope-list'),
    path('expected/', ExpectedCompetitionScopeListView.as_view(), name='expected-scope-list'),
    path('<int:scope_id>/competition-list/', CompetitionListView.as_view(), name='competition-list'),
    path('competition/<int:competition_id>/', CompetitionDetailView.as_view(), name='competition-detail'),

    path('gymnast-autocomplete/', GymnastAutocomplete.as_view(), name='gymnast-autocomplete')
]