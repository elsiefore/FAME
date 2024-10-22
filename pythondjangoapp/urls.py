from django.contrib import admin

from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('', include('uploader.urls')),
    path('video', include('video_processor.urls')),
    path('history/', include('history.urls')),
]
