from . import views
from django.urls import path

urlpatterns = [
    path('shops/', views.shop_list, name='shop_list'),
    path('reorder_shops/', views.reorder_shops, name='reorder_shops'),
]