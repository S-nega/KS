from django.contrib import admin
from .models import *

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'photo')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    # list_editable = ('is_published',)
    # list_filter = ('is_published', 'time_create')
    list_filter = ('photo', )
    prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Books, BookAdmin)
admin.site.register(Category, CategoryAdmin)