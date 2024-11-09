from django.urls import path
from . import views

urlpatterns = [
    path('work-log/', views.work_log_view, name='work_log'),
    path('delete_log/<int:log_id>/', views.delete_work_log, name='delete_work_log'),
    path('salaries/', views.salary_list_view, name='salary_list'),
    path('update_hours/', views.update_hours_difference, name='update_hours'),
    path('secret/elina/', views.elina, name="hash"),
    path('delete-log/<int:log_id>/', views.delete_bonus_log, name='delete_bonus_log'),
    path('user/<int:user_id>/work-log/', views.user_work_log_view, name='user_work_log_view'),
]
