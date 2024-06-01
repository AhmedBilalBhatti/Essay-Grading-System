from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        profile_picture = request.FILES['profile_picture']

        user = Registration(username=username, email=email, password=password, profile_picture=profile_picture)
        user.save()

        if user:
            messages.success(request, 'Account created successfully')
            request.session['identity'] = email
            return redirect('home')
        else:
            messages.error(request, 'Account creation failed')
            return redirect('register')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = Registration.objects.get(email=email,password=password)
        except Registration.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

        if user:
            messages.success(request, 'Logged in successfully')
            request.session['identity'] = email
            return redirect('home')  
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
    else:
        return render(request, 'login.html')




def home(request):
    return render(request,'index.html')