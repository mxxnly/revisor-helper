from django.urls import path
from . import views

urlpatterns = [
    path('work-log/', views.work_log_view, name='work_log'),
    path('delete_log/<int:log_id>/', views.delete_work_log, name='delete_work_log'),
    path('change_bonus/<int:log_id>/', views.change_bonus_minutes, name='change'),
    path('salaries/', views.salary_list_view, name='salary_list'),
    path('user/<int:user_id>/work-log/', views.user_work_log_view, name='user_work_log_view'),
    path('work-log/<int:user_id>/change-bonus/<int:log_id>/', views.change_bonus_minutes_for_user, name='change_bonus_for_user'),
    path('work-log/<int:user_id>/delete/<int:log_id>/', views.delete_user_work_log, name='delete_work_log_user'),

]
