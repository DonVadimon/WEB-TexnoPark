from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Template
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.decorators.http import require_GET, require_POST
from django.http import Http404
from django.core.files.storage import FileSystemStorage

from .models import Profile, Question, Answer, Tag, QuestionLike, QuestionDislike, AnswerLike, AnswerDislike


from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


class UpdateQuestionVote(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        question_id = int(self.kwargs.get('question_id', None))
        opinion = str(self.kwargs.get('opinion', None))
        question = Question.objects.find_by_id(question_id)
        QuestionDislike.objects.find_or_create(question)
        QuestionLike.objects.find_or_create(question)
        if opinion.lower() == 'like':
            question.like(request.user)
        elif opinion.lower() == 'dislike':
            question.dislike(request.user)
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        question.update_score()
        question.author.profile.update_score()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UpdateAnswerVote(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        answer_id = int(self.kwargs.get('answer_id', None))
        opinion = str(self.kwargs.get('opinion', None))
        answer = Answer.objects.find_by_id(answer_id)
        AnswerDislike.objects.find_or_create(answer)
        AnswerLike.objects.find_or_create(answer)
        if opinion.lower() == 'like':
            answer.like(request.user)
        elif opinion.lower() == 'dislike':
            answer.dislike(request.user)
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        answer.update_score()
        answer.author.profile.update_score()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
    questions = Question.objects.new()
    context = paginate(request, 5, questions)
    return render(request, 'index.html', context)


def hot_questions(request):
    questions = Question.objects.most_popular()
    context = paginate(request, 5, questions)
    return render(request, 'hot_questions.html', context)


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


def answers(request, question_id):
    # Page with answers on current question
    question = Question.objects.find_by_id(question_id)
    q_answers = Answer.objects.most_popular(question)

    context = paginate(request, 5, q_answers)
    context['question'] = question

    if is_ajax(request):
        return render(request, 'inc/_answers.html', context)
    return render(request, 'answers.html', context)


def tag_questions(request, tag):
    # Page with question on one tag
    cur_tag = Tag.objects.filter(tag=tag).first()
    if not cur_tag:
        raise Http404
    tag_qs = Question.objects.find_by_tag(tag)

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
