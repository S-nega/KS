from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('registration/', registrationPage, name='registrationPage'),
    path('cats/<int:catid>/', categories, name='cats'),  # http://127.0.0.1:8000/library/cats/
]
