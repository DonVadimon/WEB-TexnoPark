from django.db import models


def user_directory_path(instance, filename):
    """
    Function to create user's directory path
    """
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class User(models.Model):
    login = models.CharField(max_length=256, unique=True, verbose_name='Login')
    email = models.EmailField(
        max_length=254, unique=True, verbose_name='Email')
    nickname = models.CharField(max_length=256, verbose_name='NickName')
    password = models.CharField(max_length=256)
    avatar = models.ImageField(upload_to='users_avatars/')
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Question(models.Model):
    title = models.CharField(max_length=1024, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    date_create = models.DateField(
        auto_now_add=True, verbose_name='Дата создания')
    score = models.PositiveIntegerField(default=0)
    tags = models.CharField(max_length=256, verbose_name='Tags')
    author = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст')
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
