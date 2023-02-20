from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from messenger.models import Books


# menu = ["Messenger", "My Page", "Search", ...]
# Create your views here.

def index(request):
    books = Books.objects.all()
    context = {
        'title': 'General leaf',
        'books': books,
        # 'menu':menu
    }
    return render(request, 'messenger/index.html', context=context)


def registrationPage(request):
    context = {
        'title': 'Registration Page',
        # 'menu':menu
    }
    return HttpResponseNotFound('<h1>Reg page</h1>')
    # return render(request, 'messenger/registrationPage.html', context=context)


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
