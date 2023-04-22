from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.

# class Genre(models.Model):
#     name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")
#
#     def __str__(self):
#         return self.name


class Books(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название книги")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    author = models.CharField(max_length=255, verbose_name="Автор")
    photo = models.ImageField(blank=True, upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    description = models.TextField(blank=True, verbose_name="Описание")
    genre = models.ManyToManyField('Genre', default='не выбрано', help_text="Select a genre for this book", verbose_name="Жанр книги")
    price = models.IntegerField(blank=False, verbose_name="Цена")
    is_published = models.BooleanField(default=True, verbose_name="Опубликованность")
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('book', kwargs={'book_slug': self.slug})

    class Meta:
        verbose_name = 'Имеющиеся книги'
        verbose_name_plural = 'Имеющиеся книги'
        ordering = ['name']

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_slug': self.slug})

    class Meta:
        verbose_name = 'Жанр книги'
        verbose_name_plural = 'Жанры книг'
        ordering = ['name']

class Author(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book Author")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author', kwargs={'author_slug': self.slug})

    class Meta:
        verbose_name = 'Авторы книг'
        verbose_name_plural = 'Автор книги'
        ordering = ['name']


class Friends(models.Model):
    user_id = models.IntegerField(blank=False)  # обязательно к заполнению, заполняется автоматически в бэке
    follower_id = models.IntegerField(blank=False)  # обязательно к заполнению, заполняется автоматически в бэке


class News(models.Model):
    author_id = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to="newsPhotos/%Y/%m/%d")
    text = models.TextField(blank=True)  # не обязательно к заполнению
    bookId = models.IntegerField(blank=True)  # не обязательно к заполнению
    saveStatus = models.BooleanField(default=False)


class StarList(models.Model):
    user_id = models.IntegerField()
    post_id = models.IntegerField(blank=True)  # не обязательно к заполнению, заполняется автоматически в бэке
    book_id = models.IntegerField(blank=True)  # не обязательно к заполнению, заполняется автоматически в бэке


class WishList(models.Model):
    user_id = models.IntegerField()
    book_id = models.IntegerField()
    comment = models.TextField(blank=True)


class Messages(models.Model):
    author_id = models.IntegerField()
    reader_id = models.IntegerField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)


class UserLib(models.Model):
    user_id = models.IntegerField()
    book_id = models.IntegerField()
    comment = models.TextField(blank=True)
    price = models.IntegerField(blank=False)
