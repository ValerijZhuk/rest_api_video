from django.contrib import admin
from django.urls import path, include
from video_hosting import urls
from video_hosting.views import VideoList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('video_hosting.urls')),
]
