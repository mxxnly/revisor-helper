

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('q.urls')),
    path('', include('assign.urls')),
    path('', include('counting.urls')),
    path('', include('users.urls')),
    path('', include('rate.urls')),
    path('', include('hours_bonus.urls')),
    path('', include('utopky.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
