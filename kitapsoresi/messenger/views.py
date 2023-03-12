from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from messenger.forms import *
from messenger.models import *


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить книгу", 'url_name': 'addBookPage'},
        {'title': "Регистрация", 'url_name': 'login'}]
        # "Messenger", "My Page", "Search"]

class MainPage(ListView):
    model = Books
    template_name = 'messenger/index.html'
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Books.objects.filter(is_published=True)


def registrationPage(request):
    context = {
        'title': 'Registration Page',
        # 'menu':menu
    }
    # return HttpResponseNotFound('<h1>Reg page</h1>')
    return render(request, 'messenger/registrationPage.html', context=context)

class AddBookPage(CreateView):
    form_class = AddBookForm
    template_name = 'messenger/addBookPage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление Книги'
        context['menu'] = menu
        return context

class ShowBook(DetailView):
    model = Books
    template_name = 'messenger/book.html'
    slug_url_kwarg = 'book_slug'
    context_object_name = 'book'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['book']
        context['menu'] = menu
        return context

class BooksCategory(ListView):
    model = Books
    template_name = 'messenger/index.html'
    context_object_name = 'books'
    allow_empty = False

    def get_queryset(self):
        return Books.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(context['books'][0].cat)
        context['menu'] = menu
        context['cat_selected'] = context['books'][0].cat_id
        return context


def categories(request, catid):
    return HttpResponse(f"<h1>Categories<br></h1>  <p>{catid}</p>")


def error400(request, exception):
    return HttpResponseNotFound('<h1>Page not found 400</h1>')
    # return render(request, 'messenger/errors/400.html', status=400)


def error403(request, exception):
    return HttpResponseNotFound('<h1>Page not found 403 </h1>')
    # return render(request, 'messenger/errors/403.html', status=403)


def error404(request, exception):
    return HttpResponseNotFound('<h1>Page not found 404</h1>')


def error500(request):
    return HttpResponseNotFound('<h1>Page not found 500</h1>')
    # return render(request, 'messenger/errors/500.html', status=500)
