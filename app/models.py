from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.db.models import Sum


class VoteInterface():
    def get_total_likes(self):
        return self.likes.users.count()

    def get_total_dislikes(self):
        return self.dislikes.users.count()

    def like(self, user):
        if user in self.likes.users.all():
            self.likes.users.remove(user)
        else:
            self.likes.users.add(user)
            self.dislikes.users.remove(user)
        return True

    def dislike(self, user):
        if user in self.dislikes.users.all():
            self.dislikes.users.remove(user)
        else:
            self.dislikes.users.add(user)
            self.likes.users.remove(user)
        return True

    def update_score(self):
        self.score = int(self.get_total_likes()) - \
            int(self.get_total_dislikes())
        self.save(update_fields=['score'])
        return True


class QuestionManager(models.Manager):
    def most_popular(self):
        return self.all().order_by('-score').prefetch_related('author', 'tags')

    def new(self):
        return self.all().order_by('-date_create').prefetch_related('author', 'tags')

    def find_by_tag(self, tag):
        questions = self.filter(
            tags__tag__iexact=tag).prefetch_related('author')
        if not questions:
            raise Http404
        return questions

    def find_by_id(self, id):
        try:
            question = self.get(pk=id)
        except ObjectDoesNotExist:
            raise Http404
        return question


class AnswerManager(models.Manager):
    def most_popular(self, question):
        return self.filter(question=question).order_by('-score')

    def find_by_id(self, id):
        try:
            answer = self.get(pk=id)
        except ObjectDoesNotExist:
            raise Http404
        return answer


class ProfileManager(models.Manager):
    def top_ten(self):
        return self.all().order_by('-score')[:10]


class QuestionLikeManager(models.Manager):
    def find_or_create(self, question):
        try:
            question.likes
        except Question.likes.RelatedObjectDoesNotExist as identifier:
            self.create(question=question)
        return True


class QuestionDislikeManager(models.Manager):
    def find_or_create(self, question):
        try:
            question.dislikes
        except Question.dislikes.RelatedObjectDoesNotExist as identifier:
            self.create(question=question)
        return True


class AnswerLikeManager(models.Manager):
    def find_or_create(self, answer):
        try:
            answer.likes
        except Answer.likes.RelatedObjectDoesNotExist as identifier:
            self.create(answer=answer)
        return True


class AnswerDislikeManager(models.Manager):
    def find_or_create(self, answer):
        try:
            answer.dislikes
        except Answer.dislikes.RelatedObjectDoesNotExist as identifier:
            self.create(answer=answer)
        return True


class QuestionLike(models.Model):
    question = models.OneToOneField(
        'Question',
        related_name='likes',
        on_delete=models.CASCADE
    )
    users = models.ManyToManyField(
        User,
        related_name='requirement_question_likes'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.question.title)

    objects = QuestionLikeManager()


class QuestionDislike(models.Model):
    question = models.OneToOneField(
        'Question',
        related_name='dislikes',
        on_delete=models.CASCADE
    )
    users = models.ManyToManyField(
        User,
        related_name='requirement_question_dislikes'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.question.title)

    objects = QuestionDislikeManager()


class Question(models.Model, VoteInterface):
    title = models.CharField(
        max_length=1024,
        verbose_name='Title'
    )
    text = models.TextField(
        verbose_name='Text'
    )
    date_create = models.DateField(
        auto_now_add=True,
        verbose_name='Date of creation'
    )
    last_modified = models.DateField(
        auto_now=True,
        verbose_name='Last modified'
    )
    tags = models.ManyToManyField('Tag')
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='questions'
    )
    score = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    # Manager
    objects = QuestionManager()


class AnswerLike(models.Model):
    answer = models.OneToOneField(
        'Answer',
        related_name='likes',
        on_delete=models.CASCADE
    )
    users = models.ManyToManyField(
        User,
        related_name='requirement_answer_likes'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.answer.text[:30])

    objects = AnswerLikeManager()


class AnswerDislike(models.Model):
    answer = models.OneToOneField(
        'Answer',
        related_name='dislikes',
        on_delete=models.CASCADE
    )
    users = models.ManyToManyField(
        User,
        related_name='requirement_answer_dislikes'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.answer.text[:30])

    objects = AnswerDislikeManager()


class Answer(models.Model, VoteInterface):
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='answers'
    )
    text = models.TextField(
        verbose_name='Text'
    )
    score = models.IntegerField(
        default=0
    )
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE
    )
    date_create = models.DateField(
        auto_now_add=True,
        verbose_name='Date of creation'
    )
    last_modified = models.DateField(
        auto_now=True,
        verbose_name='Last modified'
    )

    def __str__(self):
        return self.author.profile.nickname

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    # Manager
    objects = AnswerManager()


class Tag(models.Model):
    tag = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    avatar = models.ImageField(
        upload_to='profiles_avatars/',
        blank=True
    )
    nickname = models.CharField(
        max_length=128,
        verbose_name='NickName'
    )
    score = models.IntegerField(
        default=0
    )
    
    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    # Manager
    objects = ProfileManager()

    def get_score_from_questions(self):
        questions_scores = self.user.questions.all().aggregate(Sum('score'))
        return questions_scores['score__sum']

    def get_score_from_answers(self):
        answers_scores = self.user.answers.aggregate(Sum('score'))
        return answers_scores['score__sum']

    def update_score(self):
        self.score = self.get_score_from_questions() + self.get_score_from_answers()
        self.save(update_fields=['score'])
        return True


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
