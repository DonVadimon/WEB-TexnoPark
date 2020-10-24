from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    #Index page
    return render(request, 'index.html', {})

def ask_question(request):
    #Page for create new Question
    return render(request, 'create_question.html', {})

def answers(request, id):
    #Page with answers on current question
    return render(request, 'answers.html', {})

def tag_questions(request):
    #Page with question on one tag
    return render(request, 'tag_questions.html', {})

def settings(request):
    #Page with user's settings
    return render(request, 'settings.html', {})

def login(request):
    #Page for login in site
    return render(request, 'login.html', {})

def register(request):
    #Page for registration
    return render(request, 'register.html', {})