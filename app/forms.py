from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from .models import Question, Answer, User, Profile

import re
from django.core.exceptions import ValidationError


class QuestionForm(forms.ModelForm):

    def save(self, request):
        question = super(QuestionForm, self).save(commit=False)
        question.author = request.user
        question.save()
        question.tags.set(request.POST.getlist('tags'))
        return question

    def clean(self):
        cleaned_data = super().clean()
        raw_title = cleaned_data['title']
        if re.fullmatch('^([a-z]|[A-Z])+[^\n\t\r]+$', raw_title) is None:
            self.add_error(
                'title',
                'Start your title with letter and do not use \\n, \\t, \\r'
            )

        raw_text = cleaned_data['text']
        if re.match('^([a-z]|[A-Z])+(.|\s)*$', raw_text) is None:
            self.add_error(
                'text',
                'Start your text with letter'
            )

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags')


class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, required=True)

    def save(self, request, question_id):
        answer = super(AnswerForm, self).save(commit=False)
        answer.author = request.user
        answer.question = Question.objects.find_by_id(question_id)
        answer.save()
        return answer

    def clean(self):
        cleaned_data = super().clean()
        raw_text = cleaned_data['text']
        if re.match('^([a-z]|[A-Z])+(.|\s)*$', raw_text) is None:
            self.add_error(
                'text',
                'Start your text with letter'
            )

    class Meta:
        model = Answer
        fields = ('text',)


class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ('username', 'password')


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=256)
    nickname = forms.CharField(required=True, max_length=256)
    avatar = forms.ImageField(required=False, label='Choose Avatar', widget=forms.FileInput(attrs={
        'style': 'display: none;',
    }))

    def save(self, FILES):
        user = super(RegistrationForm, self).save()
        user.refresh_from_db()
        user.profile.nickname = self.cleaned_data.get('nickname')
        if 'avatar' in FILES:
            user.profile.avatar = FILES['avatar']
        user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        raw_nickname = cleaned_data['nickname']
        if re.fullmatch('^([a-z]|[A-Z])+\S+$', raw_nickname) is None:
            self.add_error(
                'nickname',
                'Start your nickname with letter and do not use whitespace-characters'
            )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1',
                  'password2', 'nickname', 'avatar')


class UserSettingsForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=256)
    email = forms.EmailField(required=True, max_length=256)

    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileSettingsForm(forms.ModelForm):
    nickname = forms.CharField(required=True, max_length=256)
    avatar = forms.ImageField(required=False, label='Choose Avatar', widget=forms.FileInput(attrs={
        'style': 'display: none;',
    }))

    def save(self, user, FILES):
        profile = super(ProfileSettingsForm, self).save(commit=False)
        profile.user = user
        if 'avatar' in FILES:
            profile.avatar = FILES['avatar']
        profile.save()
        return profile

    def clean(self):
        cleaned_data = super().clean()
        raw_nickname = cleaned_data['nickname']
        if re.fullmatch('^([a-z]|[A-Z])+\S+$', raw_nickname) is None:
            self.add_error(
                'nickname',
                'Start your nickname with letter and do not use whitespace-characters'
            )

    class Meta:
        model = Profile
        fields = ('nickname', 'avatar')
