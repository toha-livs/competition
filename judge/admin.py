from django.contrib import admin

from .models import Judge


@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):
    list_display = 'user', 'competition', 'apparatus', 'judge_type',
