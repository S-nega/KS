from django.db.models import Count

from .models import *

menu = [
    {'title': "Книги", 'url_name': '/books'},
    {'title': "Поисковик", 'url_name': '/searchPage'},
    {'title': "Добавить книгу", 'url_name': '/addBookPage'},
    {'title': "О нас", 'url_name': '/about'},
    {'title': "Войти", 'url_name': '/login'},
]

class DataMixin:
    paginate_by = 3
    def get_user_context(self, **kwargs):
        context = kwargs
        genres = Genre.objects.annotate(Count('books'))
        # authors = Author.objects.annotate(Count('books'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(2)

        context['menu'] = user_menu

        context['genres'] = genres
        # context['authors'] = authors
        if 'genre_selected' not in context:
            context['genre_selected'] = 0
        # if 'author_selected' not in context:
            # context['author_selected'] = 0
        return context