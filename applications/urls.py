from django.urls import path

from . import views

urlpatterns = [
    path('', views.my_applications, name='my_applications'),
    path('apply/<int:job_id>/', views.apply, name='apply'),
    path('received/', views.employer_applications, name='employer_applications'),
    path('<int:application_id>/status/', views.update_status, name='update_application_status'),
]
