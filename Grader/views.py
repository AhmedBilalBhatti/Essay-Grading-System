from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages

# Create your views here.



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = Registration(username=username, email=email, password=password)
        user.save()

        messages.success(request, 'Account created successfully')
        return redirect('login')
    else:
        return render(request, 'register.html')


def login(request):
    return render(request,'login.html')

def home(request):
    return render(request,'index.html')