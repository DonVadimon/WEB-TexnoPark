from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.generic import ListView

questions = [
    {
        'id': idx,
        'title': f'Question about dJango {idx}',
        'text': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt nisi numquam aliquid dignissimos repudiandae sint, porro dolores, qui quod cumque dolorem. Id recusandae hic a quae illo excepturi quia similique',
        'score': f'{idx}',
        'tags': ['dJango', 'Python'],
    } for idx in range(1, 101)
]

tags = [
    'dJango',
    'Python',
    'MySQL',
    'Mailru',
    'Texnopark',
    'PHP',
]

# GLOBAL CONTEXT STARTS
context = {}
context['all_tags'] = tags
# GLOBAL CONTEXT ENDS

# Paginate starts


def paginate(request, per_page, model_list):
    paginator = Paginator(model_list, per_page)
    page_number = request.GET.get('page', 1)
    obj_list = paginator.get_page(page_number)

    max_range = int(page_number) + 4
    context = {
        "page_obj": obj_list,
        "max_range": max_range,
    }
    return context
# Paginate ends


def index(request):
    # Index page
    context.update(paginate(request, 5, questions))
    return render(request, 'index.html', context)


def ask_question(request):
    # Page for create new Question
    return render(request, 'create_question.html', context)


q_answers = [
    {
        'q_id': idx,
        'score' : f'{idx}',
        'author': 'VadikPadik',
        'text': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt nisi numquam aliquid dignissimos repudiandae sint, porro dolores, qui quod cumque dolorem.',
    } for idx in range(1, 4)
]


def answers(request, id):
    # Page with answers on current question
    question = questions[id]
    context['question'] = question
    context['answers'] = q_answers
    return render(request, 'answers.html', context)


def tag_questions(request, tag):
    # Page with question on one tag
    tag_qs = []
    for q in questions:
        if tag in q['tags']:
            tag_qs.append(q)

    context.update(paginate(request, 5, tag_qs))
    context['tag'] = f'{tag}'

    return render(request, 'tag_questions.html', context)


user = {
    'login': 'Vadim',
    'email': 'vadim@gmail.com',
    'nickname': 'DonVadimon',
}


def settings(request):
    # Page with user's settings
    context['user'] = user
    return render(request, 'settings.html', context)


errors = ['Incorrect login', 'Wrong password']


def login(request):
    # Page for login in site
    context['errors'] = errors
    return render(request, 'login.html', context)


def register(request):
    # Page for registration
    return render(request, 'register.html', context)
