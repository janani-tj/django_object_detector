from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name="logout"),

    path('objectdetection/', views.objectdetection, name='objectdetection'),
    path('videostream/', views.videostream, name='videostream'),

    path('runvideo/', views.run_video, name='run_video'),
    path('classes/', views.classes, name='classes'),
    path('add/', views.add_db, name='add_db'),
    path('delete/', views.delete_db, name='delete_db'),
    path("objtest/", views.objtest, name="objtest")
    
]
