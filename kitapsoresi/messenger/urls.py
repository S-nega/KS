from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('registration/', registrationPage, name='registrationPage'),
    path('login/', loginPage, name='loginPage'),
    path('searchPage/', searchPage, name='searchPage'),

    path('books/', MainPage.as_view(), name='booksPage'),
    path('books/author/<slug:author_slug>', BooksAuthor.as_view(), name='author'),
    path('books/genre/<slug:genre_slug>', BooksGenre.as_view(), name='genre'),
    # path('category/<slug:cat_slug>/', BooksCategory.as_view(), name='category'),

    path('addBookPage/', AddBookPage.as_view(), name='addBookPage'),
    path('book/<slug:book_slug>', ShowBook.as_view(), name='book'),
]

# urlpatterns = [
#     path('registration/', registrationPage, name='registrationPage'),
# ]
