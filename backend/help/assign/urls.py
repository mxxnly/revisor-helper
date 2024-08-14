from django.urls import path
from .views import assign_shop_view, assign_that_view
from .views import complete_task

urlpatterns = [
    path('assign_that/', assign_that_view, name='assign_that'),
    path('assign_shop/', assign_shop_view, name='assign_shop'),
    path('task/complete/<int:task_id>/', complete_task, name='complete_task'),
]
