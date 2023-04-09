from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'get_html_photo', 'description', 'price', 'is_published')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    prepopulated_fields = {"slug": ("name",)}
    fields = ('name', 'slug', 'genre', 'author', 'description', 'photo', 'get_html_photo', 'price', 'is_published')
    readonly_fields = ('get_html_photo',)
    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Миниатюра"

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

admin.site.site_title = 'Админ панель'
admin.site.site_header = 'Админ панель'