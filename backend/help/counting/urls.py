from django.urls import path
from . import views

urlpatterns = [
    path('work-log/', views.work_log_view, name='work_log'),
    path('delete_log/<int:log_id>/', views.delete_work_log, name='delete_work_log'),
]
