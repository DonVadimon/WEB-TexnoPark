from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    #Index page
    return render(request, 'index.html', {})

def ask_question(request):
    #Page for create new Question
    return render(request, 'create_question.html', {})


questions = [
    {
        'id': idx,
        'title': f'Question number {idx}',
        'text': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt nisi numquam aliquid dignissimos repudiandae sint, porro dolores, qui quod cumque dolorem. Id recusandae hic a quae illo excepturi quia similique',
    } for idx in range(10)
]

def answers(request, id):
    #Page with answers on current question
    
    question = questions[id]
    return render(request, 'question_page.html', {
        'question': question
    })
    
    #return render(request, 'answers.html', {})


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