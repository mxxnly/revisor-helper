from django.urls import path
from . import views
urlpatterns = [
    path('rate_shop/<int:shop_id>/', views.rate_shop, name='rate_shop'),
]