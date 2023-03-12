from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    path('registration/', registrationPage, name='registrationPage'),
    path('addBookPage/', AddBookPage.as_view(), name='addBookPage'),
    path('book/<slug:book_slug>/', ShowBook.as_view(), name='book'),
    path('category/<slug:cat_slug>/', BooksCategory.as_view(), name='category'),
]
