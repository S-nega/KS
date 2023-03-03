from django import forms
from .models import *

class AddBookForm(forms.Form):
    name = forms.CharField(max_length=255, label="Название ")
    slug = forms.SlugField(max_length=255, label="URL ")
    author = forms.CharField(max_length=255, label="Автор ")
    description = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 60, 'rows': 10}),
        label="Описание ")
    is_published = forms.BooleanField(label="Публикация ",
                                      required=False,
                                      initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 label="Категория/Жанр ",
                                 empty_label="Категория не выбрана")


