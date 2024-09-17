from django.urls import path
from .views import add_user_view, login_view, logout_view, error_view, profile_view

urlpatterns = [
    path('add-user/', add_user_view, name='add_user'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('perm-error/', error_view, name='perm_error'),
    path('profile/', profile_view, name='profile'),
]