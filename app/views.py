from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

questions = [
    {
        'id' : idx,
        'title' : f'Question about dJango {idx}',
        'text' : 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt nisi numquam aliquid dignissimos repudiandae sint, porro dolores, qui quod cumque dolorem. Id recusandae hic a quae illo excepturi quia similique',
        'score' : f'{idx}',
        'tags' : ['dJango', 'Python'],
    } for idx in range(5)
]

tags = [
    'dJango',
    'Python',
    'Mail.ru',
    'Texnopark',
    'PHP',
]

def index(request):
    #Index page
    context = {
        "questions" : questions,
    }
    return render(request, 'index.html', context)

def ask_question(request):
    #Page for create new Question
    context = {
        'tags' : tags,
    }
    return render(request, 'create_question.html', context)

def answers(request, id):
    #Page with answers on current question
    question = questions[id]
    return render(request, 'answers.html', {'question' : question,})

def tag_questions(request, tag):
    #Page with question on one tag
    tag_qs = []
    for q in questions:
        if tag in q['tags']:
            tag_qs.append(q)
    
    context = {
        'tag_questions' : tag_qs,
        'tag' : f'{tag}',
    }

    return render(request, 'tag_questions.html', context)

user = {
    'login' : 'Vadim',
    'email' : 'vadim@gmail.com',
    'nickname' : 'DonVadimon',
}

def settings(request):
    #Page with user's settings
    context = {
        'user' : user,
    }
    return render(request, 'settings.html', context)

errors = ['Incorrect login', 'Wrong password']

def login(request):
    #Page for login in site
    context = {
        'errors' : errors,
    }
    return render(request, 'login.html', context)

def register(request):
    #Page for registration
    return render(request, 'register.html', {})