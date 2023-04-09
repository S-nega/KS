from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    # path('', Index.as_view(), name='home'),
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('userPage/', userPage, name='userPage'),
    path('registration/', RegisterUser.as_view(), name='registrationPage'),
    path('login/', LoginUser.as_view(), name='loginPage'),
    path('logout/', logoutUser, name='logout'),
    path('searchPage/', searchPage, name='searchPage'),

    path('books/', MainPage.as_view(), name='booksPage'),
    path('books/author/<slug:author_slug>', BooksAuthor.as_view(), name='author'),
    path('books/genre/<slug:genre_slug>', BooksGenre.as_view(), name='genre'),

    path('addBookPage/', AddBookPage.as_view(), name='addBookPage'),
    path('book/<slug:book_slug>', ShowBook.as_view(), name='book'),
    path('addCommentPage/', AddCommentPage.as_view(), name='addCommentPage'),
]