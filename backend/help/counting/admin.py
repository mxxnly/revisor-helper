from django.contrib import admin
from .models import WorkLog, MoneyLog


@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'hours_worked')


admin.site.register(MoneyLog)