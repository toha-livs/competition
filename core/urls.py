"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from decorator_include import decorator_include
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.conf.urls.static import static

from core.permissions import judge_check
from .views import HomeView


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^_nested_admin/', include('nested_admin.urls')),
    path('competitions/', include('competition.urls', namespace='competition')),
    path('result/', include('result.urls', namespace='result')),
    path('judge/', decorator_include([login_required, judge_check()], 'judge.urls', namespace='judge')),
    path('auth/', include('registration.urls', namespace='registration')),

    path('select2/', include('django_select2.urls')),

    path('', HomeView.as_view(), name='home'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
