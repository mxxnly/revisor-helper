from . import views
from django.urls import path

urlpatterns = [
    path('shops/', views.shop_list, name='shop_list'),
    path('shops/add/', views.shop_add, name='shop_add'),
    path('shops/edit/<int:shop_id>/', views.shop_edit, name='shop_edit'),
    path('shops/delete/<int:shop_id>/', views.shop_delete, name='shop_delete'),
    path('reorder_shops/', views.reorder_shops, name='reorder_shops'),
]