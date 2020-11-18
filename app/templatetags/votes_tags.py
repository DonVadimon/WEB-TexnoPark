from django import template
from ..models import QuestionVote, AnswerVote

register = template.Library()


@register.simple_tag
def q_liked_by(user, question):
    vote = QuestionVote.objects.find_or_create(question, user)
    return vote.vote == 1


@register.simple_tag
def q_disliked_by(user, question):
    vote = QuestionVote.objects.find_or_create(question, user)
    return vote.vote == -1


@register.simple_tag
def a_liked_by(user, answer):
    vote = AnswerVote.objects.find_or_create(answer, user)
    return vote.vote == 1


@register.simple_tag
def a_disliked_by(user, answer):
    vote = AnswerVote.objects.find_or_create(answer, user)
    return vote.vote == -1
