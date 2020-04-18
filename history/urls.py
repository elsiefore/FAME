from django.urls import path

from . import views

urlpatterns = [
    path('', views.list, name='list'),
<<<<<<< HEAD
    path('/?P<int:job_id>/', views.job_detail, name="job_detail")
=======
    path('job_detail/<int:job_id>/', views.job_detail, name="job_detail")
>>>>>>> c6ae02967224d39f6ba14655ab5918a92a09f516
]
