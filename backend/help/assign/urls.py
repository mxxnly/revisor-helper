from django.urls import path
from .views import assign_shop_view

urlpatterns = [
    path('assign_shop/', assign_shop_view, name='assign_shop'),
]
