from django.contrib import admin
from .models import *

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'photo', 'description', 'price', 'is_published')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    prepopulated_fields = {"slug": ("name",)}


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Books, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Author, AuthorAdmin)