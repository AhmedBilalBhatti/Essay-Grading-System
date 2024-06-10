from django.shortcuts import render,redirect
from django.http import HttpResponse , JsonResponse
from .models import *
from django.contrib import messages
from .nlp import * 
from .topic import *


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


def logout(request):
    del request.session['identity']
    return redirect('login')


def home(request):
    email =  request.session.get('identity')
    if email:
        user = Registration.objects.get(email=email)
    else:
        return redirect('login')
    
    return render(request,'index.html', {'user':user})

def slice_string(input_string, length=300):
    return (input_string[:length] + '...') if len(input_string) > length else input_string

def main(request):
    email = request.session.get('identity')
    if email:
        user = Registration.objects.get(email=email)
    else:
        return redirect('login')
    if request.method == 'POST':
        message = request.POST['message']
        new_essay = message

        grade, num_errors, num_uncommon_words, num_punctuation, detailed_uncommon_words, avg_sentiment, sentiment_label = grade_and_assess_mistakes(new_essay)
        # suggestions = improvement_suggestions(new_essay)
        topic = topic_modelling(new_essay)
        
        if sentiment_label == '1 star':
            sentiment_label = 'Very Negative'
        elif sentiment_label == '2 stars':
            sentiment_label = 'Negative'
        elif sentiment_label == '3 stars':
            sentiment_label = 'Neutral'
        elif sentiment_label == '4 stars':
            sentiment_label = 'Positive'
        else:
            sentiment_label = 'Very Positive'
        
        detailed_uncommon_words = slice_string(detailed_uncommon_words)
        print('Ptt================',detailed_uncommon_words)
        
        response = {
            'grade': grade,
            'num_errors': num_errors,
            'num_uncommon_words': num_uncommon_words,
            'num_punctuation': num_punctuation,
            'detailed_uncommon_words': detailed_uncommon_words,
            'avg_sentiment': avg_sentiment,
            'sentiment_label': sentiment_label,
            # 'suggestions': suggestions,
            'topic': topic,
        }

        return JsonResponse({'message': response})

    return render(request, 'chatbot.html', {'user': user})



def user_profile(request):
    email =  request.session.get('identity')
    if email:
        user = Registration.objects.get(email=email)
    else:
        return redirect('login')
    return render(request, 'profile.html', {'user':user})