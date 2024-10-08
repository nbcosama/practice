from django.contrib import admin
from django.urls import path, include
from . import views
from .import otp


urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.students, name='students'),
    path('login/', views.login, name='login'),
    path('register_problem/', views.register_problem, name='register_problem'),
    path('get_problems/', views.get_problems, name='get_problems'),
    path('send-otp/', otp.send_otp_view, name='send_otp'),
    path('sendemail/', views.sendemail, name='sendemail'),
    path('community/', views.community, name='community'),
    path('community_detail', views.community_detail, name='community_detail'),
    path('degree/', views.degree, name='degree'),
    
]
