from django.urls import path
from .views import ResultLiveView, ResultView

app_name = 'result'

urlpatterns = [
    path('result/', ResultView.as_view(), name='result'),
    path('result/live/', ResultLiveView.as_view(), name='result-live'),
]