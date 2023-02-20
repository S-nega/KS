from django.db import models


# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        return self.name


class Books(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    price = models.IntegerField(blank=False)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name


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
