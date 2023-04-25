from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from messenger.forms import *
from messenger.models import *
from .permissions import IsAdminOrReadOnly
from .serializers import BooksSerializer, AuthorSerializer, GenreSerializer
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


class UserBooksPage(LoginRequiredMixin, DataMixin, ListView):
    model = Books
    template_name = 'messenger/user_books.html'
    # user = 'user'
    # slug_url_kwarg = 'user'
    context_object_name = 'books'

    def get_queryset(self):
        # print(self.kwargs['user'])
        us_id = User.objects.get(username=self.kwargs['user'])
        # return UserLib.objects.filter(user=self.request.user)
        return Books.objects.filter(user=us_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Книги")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


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


# class AddBookToWishList(LoginRequiredMixin, DataMixin, CreateView):
#     model = WishList
#     context_object_name = 'links'


@login_required(login_url='signin')
def addToWishList(request):
    if request.method == 'POST':
        user = request.POST['user']
        user_id = User.objects.get(username=user)
        my_user_id = user_id.pk
        book_slug = request.POST['book_slug']
        print('my_data: ', user, user_id, book_slug)

        if WishList.objects.filter(user=user_id, book_slug=book_slug).first():
            delete_wish = WishList.objects.get(user=user_id, book_slug=book_slug)
            delete_wish.delete()
            return redirect('/main/wishListPage/1' + user)
        else:
            new_wish = WishList.objects.create(user=user_id, book_slug=book_slug)
            new_wish.save()
            return redirect('/main/wishListPage/' + user)
    else:
        return render(request, 'messenger/user_wishList.html', )


class WishListPage(LoginRequiredMixin, DataMixin, ListView):
    model = WishList
    template_name = 'messenger/user_wishList.html'
    # user = 'user'
    # slug_url_kwarg = 'user'
    context_object_name = 'wish_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Желаемые Книги")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        # print(self.kwargs['user'])
        us_id = User.objects.get(username=self.kwargs['user'])
        return WishList.objects.filter(user=us_id)



class AddCommentPage(LoginRequiredMixin, DataMixin, FormView):
    form_class = CommentForm
    template_name = 'messenger/addCommentPage.html'
    success_url = reverse_lazy('feed')
    login_url = reverse_lazy('login')
    raise_exception = True

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Оставить комментарий")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('feed')



class ShowBook(DataMixin, DetailView):
    model = Books
    template_name = 'messenger/book.html'
    slug_url_kwarg = 'book_slug'
    context_object_name = 'book'
    # button_text = 'Добавить в виш-лист'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['book'])
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    # def get_queryset(self):
    #     if WishList.objects.get(user=self.request.user, book_slug=self.kwargs['book_slug']):
    #         button_text = 'Удалить из виш-листа'
    #     return button_text


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
        del user_menu[1:3]


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
        del user_menu[1:3]

    context = {
        'title': 'Search Page',
        'menu': user_menu,
    }
    return render(request, 'messenger/searchPage.html', context=context)


# @login_required
def about(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        del user_menu[1:3]

    context = {
        'title': 'About us',
        'menu': user_menu,
    }
    return render(request, 'messenger/about.html', context=context)

#
# def userPage(request):
#     context = {
#         'title': 'Account',
#         'menu': menu,
#     }
#     return render(request, 'messenger/userPage.html', context=context)


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



class BookViewSet(viewsets.ModelViewSet):
    # queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = (IsAdminOrReadOnly, )
    def get_queryset(self):
        pk = self.kwargs.get("pk")

        if not pk:
            return Books.objects.all()[:3]

        return Books.objects.filter(pk=pk)

    @action(methods=['get'], detail=True)
    def genre(self, request, pk=None):
        genres = Genre.objects.get(pk=pk)
        return Response({'genres': genres.name})


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )
    def get_queryset(self):
        pk = self.kwargs.get("pk")

        if not pk:
            return Genre.objects.all()[:3]

        return Genre.objects.filter(pk=pk)


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs.get("pk")

        if not pk:
            return Author.objects.all()[:3]

        return Author.objects.filter(pk=pk)


#
# class BooksAPIView(APIView):
#     def get(self, request):
#         p = Books.objects.all()
#         return Response({'books': BooksSerializer(p, many=True).data})
#
#     def post(self, request):
#         serializer = BooksSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'books': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method put not allowed"})
#
#         try:
#             instance = Books.objects.get(pk=pk)
#         except:
#             return Response({"error": "oBject doesnt not exists"})
#
#         serializer = BooksSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"books": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"})
#
#         try:
#             record = Books.objects.get(pk=pk)
#             record.delete()
#         except:
#             return Response({"error": "Object does not exists"})
#
#         return Response({"books": "delete post " + str(pk)})
#
#
# class GenreAPIView(APIView):
#     def get(self, request):
#         p = Genre.objects.all()
#         return Response({'genre': GenreSerializer(p, many=True).data})
#
#     def post(self, request):
#         serializer = GenreSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'genre': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method put not allowed"})
#
#         try:
#             instance = Genre.objects.get(pk=pk)
#         except:
#             return Response({"error": "oBject doesnt not exists"})
#
#         serializer = GenreSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"genre": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"})
#
#         try:
#             record = Genre.objects.get(pk=pk)
#             record.delete()
#         except:
#             return Response({"error": "Object does not exists"})
#
#         return Response({"genre": "delete post " + str(pk)})
#
#
# class AuthorAPIView(APIView):
#     def get(self, request):
#         p =  Author.objects.all()
#         return Response({'author': AuthorSerializer(p, many=True).data})
#
#     def post(self, request):
#         serializer = AuthorSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'author': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method put not allowed"})
#
#         try:
#             instance = Author.objects.get(pk=pk)
#         except:
#             return Response({"error": "oBject doesnt not exists"})
#
#         serializer = AuthorSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"author": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"})
#
#         try:
#             record = Author.objects.get(pk=pk)
#             record.delete()
#         except:
#             return Response({"error": "Object does not exists"})
#
#         return Response({"author": "delete post " + str(pk)})