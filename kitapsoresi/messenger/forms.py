from django import forms
from django.core.exceptions import ValidationError

from .models import *

class AddBookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre'].empty_label = "Жанр не выбран"
        self.fields['author'].empty_label = "Автор не выбран"

    class Meta:
        model = Books
        fields = ['name', 'slug', 'description', 'photo', 'author', 'genre', 'price', 'is_published', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': ''}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'genre': forms.CheckboxSelectMultiple(attrs={'class': ''}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 200:
            raise ValidationError('Длинна превышает 200 символов')
        return name