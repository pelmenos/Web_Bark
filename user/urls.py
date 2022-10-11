from django.urls import path, include

from . import views

urlpatterns = [
    path('login_user/', views.LoginUser, name='login_user'),
    path('logout/', views.Logout, name='logout'),
    path('register/', views.Register, name='register'),
]
