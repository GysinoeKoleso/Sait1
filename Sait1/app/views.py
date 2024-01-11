"""
Definition of views.
"""

from .forms import CommentForm # использование формы ввода комментария
from .models import Comment # использование модели комментариев
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db import models
from .models import Blog

def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST": # после отправки формы
       regform = UserCreationForm (request.POST) 
       if regform.is_valid(): #валидация полей формы
          reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
          reg_f.is_staff = False # запрещен вход в административный раздел
          reg_f.is_active = True # активный пользователь
          reg_f.is_superuser = False # не является суперпользователем
          reg_f.date_joined = datetime.now() # дата регистрации
          reg_f.last_login = datetime.now() # дата последней авторизации
          reg_f.save() # сохраняем изменения после добавления данных (добавление пользователя в БД пользователей) 
          return redirect('home') # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform, # передача формы в шаблон веб-страницы
            'year':datetime.now().year
        }
    )

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведение о нас.',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Наши партнёры',
            'message':'Ссылки на парнтнёров.',
            'year':datetime.now().year,
            }
    )

def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.order_by('-posted') # запрос на выбор всех статей из модели, отсортированных по убыванию даты опубликования
    return render(
        request,
        'app/blog.html',
        { # параметр в {} — данные для использования в шаблоне.
            'title':'Блог',
            'posts': posts, # передача списка статей в шаблон веб-страницы 
            'year':datetime.now().year,
        }
    )


def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретнойстатьи по параметру
    comments = Comment.objects.filter(post=parametr) # запрос на выбор всех комментариев к конкретной статье
    
    #работы с формой добавления комментария
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату 
            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий 
            comment_f.save() # сохраняем изменения после добавления полей 
        return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm() # создание формы для ввода комментария
        return render(
            request,
            'app/blogpost.html',
            {
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы 
            'form': form, # передача формы в шаблон веб-страницы
            'post_1': post_1, # передача конкретной статьи в шаблонвеб-страницы
            'year':datetime.now().year,
            }
        )