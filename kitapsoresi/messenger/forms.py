from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import *

class AddBookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre'].empty_label = "Жанр не выбран"
        self.fields['author'].empty_label = "Автор не выбран"

    class Meta:
        model = Books
        fields = ['name', 'slug', 'description', 'photo', 'author', 'genre', 'price', 'is_published', 'user']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': ''}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'genre': forms.CheckboxSelectMultiple(attrs={'class': ''}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            # 'user': forms.TextInput(attrs={'class': ''}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 100:
            raise ValidationError('Длинна превышает 100 символов')
        return name


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    number = forms.CharField(label='Number', widget=forms.NumberInput(attrs={'class ': 'form-input'}))
    location = forms.CharField(label='Location', widget=forms.TextInput(attrs={'class': 'form-input'}))
    bio = forms.CharField(label='bio', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'number', 'location', 'bio', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()