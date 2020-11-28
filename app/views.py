from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Template
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.decorators.http import require_GET, require_POST
from django.http import Http404
from django.core.files.storage import FileSystemStorage
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, AnswerForm, LoginForm, RegistrationForm, UserSettingsForm, ProfileSettingsForm


from .models import Profile, Question, Answer, Tag, QuestionVote, AnswerVote


class UpdateQuestionVote(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        question_id = int(self.kwargs.get('question_id', None))
        opinion = str(self.kwargs.get('opinion', None))
        question = Question.objects.find_by_id(question_id)
        vote = QuestionVote.objects.find_or_create(question, request.user)
        if opinion.lower() == 'like':
            vote.like()
        elif opinion.lower() == 'dislike':
            vote.dislike()
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
        vote = AnswerVote.objects.find_or_create(answer, request.user)
        if opinion.lower() == 'like':
            vote.like()
        elif opinion.lower() == 'dislike':
            vote.dislike()
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


@login_required
def ask_question(request):
    # Page for create new Question
    if request.method == 'GET':
        form = QuestionForm()
    else:
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            question = form.save(request=request)
            return redirect(reverse('answers', kwargs={'question_id': question.pk}))
    return render(request, 'create_question.html', {'form': form})


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
    if request.method == 'GET':
        form = AnswerForm()
    else:
        if request.user.is_authenticated:
            form = AnswerForm(data=request.POST)
            if form.is_valid():
                answer = form.save(request=request, question_id=question_id)
                return redirect(reverse('answers', kwargs={'question_id': question_id}) + f'#{answer.pk}')
        else:
            return redirect(reverse('login') + f'?next={request.path}')
    context['form'] = form
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


@login_required
def settings(request):
    if request.method == 'GET':
        user_form = UserSettingsForm(instance=request.user)
        profile_form = ProfileSettingsForm(instance=request.user.profile)
    else:
        user_form = UserSettingsForm(
            data=request.POST,
            instance=request.user
        )
        profile_form = ProfileSettingsForm(
            data=request.POST,
            instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile_form.save(user=user, FILES=request.FILES)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'settings.html', context)


def login(request):
    # Page for login on site
    if request.GET.get('next'):
        next_url = request.GET.get('next')
    elif request.session.get('next'):
        next_url = request.session.get('next')
    else:
        next_url = ''

    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                if next_url != '':
                    return redirect(next_url)
                else:
                    return redirect(reverse('home'))

    if request.session.get('next') != next_url:
        request.session['next'] = next_url

    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


@login_required
def logout(request):
    auth.logout(request)
    if 'next' in request.GET:
        return redirect(request.GET['next'])
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def register(request):
    # Page for registration
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(FILES=request.FILES)
            raw_password = form.cleaned_data.get('password1')
            user = auth.authenticate(
                username=user.username,
                password=raw_password
            )
            if user is not None:
                auth.login(request, user)
            else:
                return redirect(reverse('signup'))
            return redirect(reverse('home'))
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})
