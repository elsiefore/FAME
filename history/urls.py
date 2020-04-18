from django.urls import path

from . import views

urlpatterns = [
    path('', views.list, name='list'),
    path('/?P<int:job_id>/', views.job_detail, name="job_detail")
]
