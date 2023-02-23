from django.contrib import admin
from .models import *

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'photo')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    # list_editable = ('is_published',)
    # list_filter = ('is_published', 'time_create')
    list_filter = ('photo', )

# class CategoryAdmin(admin.CategoryAdmin):
#     list_display = ('id', 'name', 'author')
#     list_display_links = ('id', 'name')
#     search_fields = ('name',)

admin.site.register(Books, BookAdmin)
# admin.site.register(Category, CategoryAdmin)