from django.db.models import Count
from django.core.cache import cache

from .models import *

menu = [
    {'title': "Книги", 'url_name': '/main/books'},
    {'title': "Добавить книгу", 'url_name': '/main/addBookPage'},
    {'title': "Новости", 'url_name': '/'},
    {'title': "Поисковик", 'url_name': '/main/searchPage'},
    {'title': "О нас", 'url_name': '/main/about'},
    # {'title': "Главная", 'url_name': '/main'},
]

class DataMixin:
    paginate_by = 3
    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        books_list = cache.get('books_list')
        genres = cache.get('genres')
        cache_menu = cache.get('menu')
        # wish_books = cache.get('wish_books')
        # us_id = User.objects.get(username=self.kwargs['user'])
        # wish_list = WishList.objects.filter(user=us_id)



        # wish_books = Books.objects.filter(slug=us_id)

        if not self.request.user.is_authenticated:
            del user_menu[1:3]
            cache.set('menu', user_menu, 60)

        if self.request.user.is_authenticated:
            user_menu = menu.copy()
            cache.set('menu', user_menu, 60)

        if not cache_menu:
            cache.set('menu', user_menu, 60)

        if not genres:
            genres = Genre.objects.annotate(Count('books'))
            cache.set('genres', genres, 60)
        # authors = Author.objects.annotate(Count('books'))

        if not books_list:
            books_list = Books.objects.annotate(Count('user'))
            cache.set('books_list', books_list, 60)

        # if not wish_books:
        #     for b in books:
        #         for w in wish_list:
        #             if b.slug == w.book_slug:
        #                 wish_books = Books.objects.annotate(Count('slug'))
        #                 cache.set('wish_books', wish_books)
            # books = Books.objects.annotate(Count('slug'))
            # cache.set('books', books, 60)

        context['menu'] = cache_menu
        context['genres'] = genres
        context['books_list'] = books_list
        # context['wish_books'] = wish_books
        # context['authors'] = authors
        # context['post'] = post
        if 'genre_selected' not in context:
            context['genre_selected'] = 0
        # if 'author_selected' not in context:
            # context['author_selected'] = 0
        return context