from django.urls import path
from .import views
from Grader import *

urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.register, name='register'),
]