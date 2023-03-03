from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('registration/', registrationPage, name='registrationPage'),
    path('addBookPage/', addBookPage, name='addBookPage'),
    path('book/<slug:book_slug>/', show_book, name='book'),
    path('category/<slug:cat_slug>/', show_category, name='category'),
]
