from django.urls import path
from . import views

urlpatterns = [
    path('work-log/', views.work_log_view, name='work_log'),
]
