from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from messenger.forms import *
from messenger.models import *
from .serializers import BooksSerializer
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
        return Books.objects.filter(is_published=True).prefetch_related('genre')



class AddBookPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddBookForm
    template_name = 'messenger/addBookPage.html'
    success_url = reverse_lazy('booksPage')
    # login_url = '/admin/'
    # login_url = reverse_lazy('login')
    raise_exception = True

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление книги")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class AddCommentPage(LoginRequiredMixin, DataMixin, FormView):
    form_class = CommentForm
    template_name = 'messenger/addCommentPage.html'
    # success_url = reverse_lazy('book')
    success_url = reverse_lazy('booksPage')
    login_url = reverse_lazy('login')
    raise_exception = True

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Оставить комментарий")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        # return redirect('book')
        return redirect('booksPage')

# class AccountPage(LoginRequiredMixin):

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
        return Books.objects.filter(genre__slug=self.kwargs['genre_slug'], is_published=True).prefetch_related('genre')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # c_def = self.get_user_context(title=str(context['books'][0].genre),
        #                               genre_selected=context['books'][0].genre,
        #                               author_selected=context['books'][0].author)
        c = Genre.objects.get(slug=self.kwargs['genre_slug'])
        # a = Author.objects.get(slug=self.kwargs['author_slug'])
        c_def = self.get_user_context(title=str(c.name),
                                      genre_selected=c.pk,)
                                      # author_selected=context['books'][0].author)

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


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'messenger/registrationPage.html'
    success_url = reverse_lazy('loginPage')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'messenger/loginPage.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logoutUser(request):
    logout(request)
    return redirect('loginPage')


# class Index(DataMixin, ListView):
#     template_name = 'messenger/index.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Главная страница")
#         return dict(list(context.items()) + list(c_def.items()))
#
#     def get_queryset(self):
#         return Books.objects.filter(is_published=True).prefetch_related('genre')



def index(request):

    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(2)

    context = {
        'title': 'Main Page',
        'menu': user_menu,
    }

    return render(request, 'messenger/index.html', context=context)



# def registrationPage(request):
#     context = {
#         'title': 'Registration Page',
#         'menu': menu,
#     }
#     return render(request, 'messenger/registrationPage.html', context=context)
#
# def loginPage(request):
#     context = {
#         'title': 'Login Page',
#         'menu': menu,
#     }
#     return render(request, 'messenger/loginPage.html', context=context)

def searchPage(request):

    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(2)

    context = {
        'title': 'Search Page',
        'menu': user_menu,
    }
    return render(request, 'messenger/searchPage.html', context=context)


# @login_required
def about(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(2)

    context = {
        'title': 'About us',
        'menu': user_menu,
    }
    return render(request, 'messenger/about.html', context=context)

def userPage(request):
    context = {
        'title': 'Account',
        'menu': menu,
    }
    return render(request, 'messenger/userPage.html', context=context)


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


class BooksAPIView(APIView):
    def get(self, request):
        b = Books.objects.all()
        return Response({'books': BooksSerializer(b, many=True).data})
    def post(self, request):
        serializer = BooksSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'book': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            instance = Books.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = BooksSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})
        try:
            instance = Books.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        instance.delete()

        return Response({"post": "delete post " + str(pk)})

# class BooksAPIVeiw(generics.ListAPIView):
#     queryset = Books.objects.all()
#     serializer_class = BooksSerializer
