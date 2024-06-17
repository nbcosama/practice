from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.students, name='students'),
    path('login/', views.login, name='login'),
    path('register_problem/', views.register_problem, name='register_problem'),
    path('get_problems/', views.get_problems, name='get_problems')
]
