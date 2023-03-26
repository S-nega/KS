from django import template
from messenger.models import *

register = template.Library()

@register.simple_tag(name='getgenre')
def get_genre(filter=None):
    if not filter:
        return Genre.objects.all()
    else:
        return Genre.objects.filter(pk=filter)

@register.inclusion_tag('messenger/tags/list_genres.html')
def show_genres(sort=None, genre_selected=0):
    if not sort:
        genres = Genre.objects.all()
    else:
        genres = Genre.objects.order_by(sort)
    return {"genres": genres, "genre_selected": genre_selected}

@register.inclusion_tag('messenger/tags/list_authors.html')
def show_authors(sort=None, author_selected=0):
    if not sort:
        authors = Author.objects.all()
    else:
        authors = Author.objects.order_by(sort)

    return {"authors": authors, "author_selected": author_selected}


