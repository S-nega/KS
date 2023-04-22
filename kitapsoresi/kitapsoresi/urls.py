"""kitapsoresi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import messenger
import social_book

from kitapsoresi import settings
s = settings
from messenger.views import *
from social_book.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'book', BookViewSet, basename='book')
# router.register(r'post', PostViewSet, basename='post')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha', include('captcha.urls')),
    path('main/', include('messenger.urls')),
    path('', include('social_book.urls')),

    path('api/v1/', include(router.urls)),
    # path('api/v1/bookslist/', BookViewSet.as_view({'get': 'list'})),
    # path('api/v1/bookslist/<int:pk>/', BookViewSet.as_view({'put': 'update'})),
    #
    path('api/v1/postslist/', PostAPIList.as_view()),
    path('api/v1/postslist/<int:pk>/', PostAPIUpdateDestroy.as_view()),
    path('api/v1/postslist/d/<int:pk>/', PostAPIDestroy.as_view()),
    # path('api/v1/postsdetail/<int:pk>/', PostAPIDetailView.as_view()),
]


if s.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = error400
handler403 = error403
handler404 = error404
handler500 = error500
