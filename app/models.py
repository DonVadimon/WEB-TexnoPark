from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class QuestionManager(models.Manager):
    def most_popular(self):
        return self.all().order_by('-score')

    def new(self):
        return self.all().order_by('date_created')

    def tag(self, tag):
        return self.filter(tags__tag__iexact=tag)


class AnswerManager(models.Manager):
    def most_popular(self):
        return self.all().order_by('-score')


class ProfileManager(models.Manager):
    def top_ten(self):
        return self.all().order_by('-score')[:10]


class Question(models.Model):
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
    score = models.PositiveIntegerField(
        default=0
    )
    tags = models.ManyToManyField('Tag')
    author = models.ForeignKey(
        'Profile',
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    # Manager
    objects = QuestionManager()


class Answer(models.Model):
    author = models.ForeignKey(
        'Profile',
        null=True,
        on_delete=models.SET_NULL
    )
    text = models.TextField(
        verbose_name='Text'
    )
    score = models.PositiveIntegerField(
        default=0
    )
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.author.nickname

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
        on_delete=models.CASCADE
    )
    avatar = models.ImageField(
        upload_to='profiles_avatars/',
        blank=True
    )
    nickname = models.CharField(
        max_length=128,
        verbose_name='NickName'
    )
    score = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    # Manager
    objects = ProfileManager()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
