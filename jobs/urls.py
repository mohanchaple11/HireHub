from django.urls import path

from . import views

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list'),
    path('new/', views.JobCreateView.as_view(), name='create_job'),
    path('manage/', views.ManageJobsView.as_view(), name='manage_jobs'),
    path('<int:pk>/edit/', views.JobUpdateView.as_view(), name='edit_job'),
    path('<int:pk>/delete/', views.JobDeleteView.as_view(), name='delete_job'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
]
