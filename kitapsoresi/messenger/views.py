from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from messenger.forms import *
from messenger.models import *
from .utils import *

class MainPage(DataMixin, ListView):
    model = Books
    template_name = 'messenger/books.html'
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Книги")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Books.objects.filter(is_published=True)



class AddBookPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddBookForm
    template_name = 'messenger/addBookPage.html'
    success_url = reverse_lazy('home')
    # login_url = '/admin/'
    # login_url = reverse_lazy('login')
    raise_exception = True

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление книги")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

class ShowBook(DataMixin, DetailView):
    model = Books
    template_name = 'messenger/book.html'
    slug_url_kwarg = 'book_slug'
    context_object_name = 'book'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['book'])
        context = dict(list(context.items()) + list(c_def.items()))
        return context

class BooksGenre(DataMixin, ListView):
    model = Books
    template_name = 'messenger/books.html'
    context_object_name = 'books'
    allow_empty = False

    def get_queryset(self):
        return Books.objects.filter(genre__slug=self.kwargs['genre_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=str(context['books'][0].genre),
                                      genre_selected=context['books'][0].genre,
                                      author_selected=context['books'][0].author)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

class BooksAuthor(DataMixin, ListView):
    model = Books
    template_name = 'messenger/books.html'
    context_object_name = 'books'
    allow_empty = False

    def get_queryset(self):
        return Books.objects.filter(author__slug=self.kwargs['author_slug'], is_published=True)

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=str(context['books'][0].genre),
                                      genre_selected=context['books'][0].genre,
                                      # genre_selected = 0
                                      author_selected=context['books'][0].author)
        context = dict(list(context.items()) + list(c_def.items()))
        return context


def index(request):
    context = {
        'title': 'Main Page',
        'menu': menu,
    }

    return render(request, 'messenger/index.html', context=context)

def registrationPage(request):
    context = {
        'title': 'Registration Page',
        'menu': menu,
    }
    return render(request, 'messenger/registrationPage.html', context=context)

def loginPage(request):
    context = {
        'title': 'Login Page',
        'menu': menu,
    }
    return render(request, 'messenger/loginPage.html', context=context)

def searchPage(request):
    context = {
        'title': 'Search Page',
        'menu': menu,
    }
    return render(request, 'messenger/searchPage.html', context=context)

# @login_required
def about(request):
    context = {
        'title': 'About us',
        'menu': menu,
    }
    return render(request, 'messenger/about.html', context=context)

def error400(request, exception):
    # return HttpResponseNotFound('<h1>Page not found 400</h1>')
    return render(request, 'messenger/errors/400.html', status=400)


def error403(request, exception):
    # return HttpResponseNotFound('<h1>Page not found 403 </h1>')
    return render(request, 'messenger/errors/403.html', status=403)


def error404(request, exception):
    # return HttpResponseNotFound('<h1>Page not found 404</h1>')
    return render(request, 'messenger/errors/404.html', status=403)


def error500(request):
    # return HttpResponseNotFound('<h1>Page not found 500</h1>')
    return render(request, 'messenger/errors/500.html', status=500)
