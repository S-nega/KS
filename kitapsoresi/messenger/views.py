from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect

from messenger.forms import *
from messenger.models import *


# menu = ["Messenger", "My Page", "Search", ...]
# Create your views here.

def index(request):
    books = Books.objects.all()
    context = {
        'title': 'General leaf',
        'cat_selected': 0,
        'books': books,
        # 'menu':menu
    }
    return render(request, 'messenger/index.html', context=context)


def registrationPage(request):
    context = {
        'title': 'Registration Page',
        # 'menu':menu
    }
    # return HttpResponseNotFound('<h1>Reg page</h1>')
    return render(request, 'messenger/registrationPage.html', context=context)

def addBookPage(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            try:
                Books.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Error in adding')
    else:
        form = AddBookForm()

    context = {
        'form': form,
        'title': 'Add Book Page',
        # 'menu':menu
    }
    # return HttpResponseNotFound('<h1>Reg page</h1>')
    return render(request, 'messenger/addBookPage.html', context=context)


def categories(request, catid):
    return HttpResponse(f"<h1>Categories<br></h1>  <p>{catid}</p>")


def error400(request, exception):
    return HttpResponseNotFound('<h1>Page not found 400</h1>')
    # return render(request, 'messenger/errors/400.html', status=400)


def error403(request, exception):
    return HttpResponseNotFound('<h1>Page not found 403 </h1>')
    # return render(request, 'messenger/errors/403.html', status=403)


def error404(request, exception):
    return HttpResponseNotFound('<h1>Page not found 404</h1>')


def error500(request):
    return HttpResponseNotFound('<h1>Page not found 500</h1>')
    # return render(request, 'messenger/errors/500.html', status=500)

def show_book(request, book_slug):
    book = get_object_or_404(Books, slug=book_slug)

    context = {
        'book': book,
        # 'menu': menu,
        'title': book.name,
        'cat_selected': book.cat_id,
    }

    return render(request, 'messenger/book.html', context=context)
def show_category(request, cat_slug):
    cat = get_object_or_404(Category, slug=cat_slug)
    books = Books.objects.filter(cat_id=cat.id)

    if len(books) == 0:
        raise Http404()

    context = {
        'books': books,
        'title': cat.name,
        'cat_selected': cat.id,
    }
    return render(request, 'messenger/index.html', context=context)
    # return HttpResponse(f"Отображение категории с id = {cat_id}")