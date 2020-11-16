"""askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('hot', views.hot_questions, name='hot'),
    path('ask/', views.ask_question, name='ask'),
    path('question/<int:id>/', views.answers, name='answers'),
    path('tag/<slug:tag>/', views.tag_questions, name='tag'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('requirement/<int:question_id>/<str:opinion>', views.UpdateQuestionVote.as_view(), name='requirement_question_vote'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
