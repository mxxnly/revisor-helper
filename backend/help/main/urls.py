from . import views
from django.urls import path

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('revisors/',views.revisor,name='revisors'),
    path('revisors/delete/<int:revisor_id>/',views.delete_revisor,name='delete_revisor'),
    path('add_revisor',views.add_revisor, name='add_revisor'),
    path('add_shops/<int:revisor_id>/',views.add_shops, name='add_shops'),
    path('add_way_shops/<int:revisor_id>/',views.add_way_shops, name='add_way_shops'),
    path('add_move_shops/<int:revisor_id>/',views.add_move_shops, name='add_move_shops'),
]