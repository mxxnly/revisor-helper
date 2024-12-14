from django.urls import path
from .views import update_hours_difference

urlpatterns = [
    path('update_hours/', update_hours_difference, name='update_hours'),
]