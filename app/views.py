from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.decorators.http import require_GET, require_POST
from django.http import Http404
from django.core.files.storage import FileSystemStorage

from .models import Profile, Question, Answer, Tag

# Paginate starts


def paginate(request, per_page, model_list):
    paginator = Paginator(model_list, per_page)
    page_number = int(request.GET.get('page', 1))
    if page_number > paginator.num_pages:
        raise Http404

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
    questions = Question.objects.all()
    context = paginate(request, 5, questions)
    return render(request, 'index.html', context)


def ask_question(request):
    # Page for create new Question
    return render(request, 'create_question.html', {})


def is_ajax(request):
    """
    This utility function is used, as `request.is_ajax()` is deprecated.

    This implements the previous functionality. Note that you need to
    attach this header manually if using fetch.
    """
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


def answers(request, id):
    # Page with answers on current question

    question = Question.objects.get(pk=id)
    q_answers = Answer.objects.filter(question=question)

    per_page = 5
    context = paginate(request, per_page, q_answers)
    context['question'] = question

    if is_ajax(request):
        return render(request, 'inc/_answers.html', context)
    return render(request, 'answers.html', context)


def tag_questions(request, tag):
    # Page with question on one tag
    cur_tag = Tag.objects.filter(tag=tag).first()
    tag_qs = Question.objects.filter(tags__in=[cur_tag.pk])

    context = paginate(request, 5, tag_qs)
    context['tag'] = f'{tag}'

    return render(request, 'tag_questions.html', context)


def settings(request):
    # Page with user's settings
    return render(request, 'settings.html', {})


errors = ['Incorrect login', 'Wrong password']


def login(request):
    # Page for login in site
    context = {
        'errors': errors,
    }
    return render(request, 'login.html', context)


def register(request):
    # Page for registration
    return render(request, 'register.html', {})
