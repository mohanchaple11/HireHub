from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('candidates/', views.candidate_directory, name='candidate_directory'),
    path('candidates/<int:pk>/', views.candidate_detail, name='candidate_detail'),
]
