from django.urls import path
from .import views
from Grader import *

urlpatterns = [
    path('', views.home, name='home'),
]