from django.urls import path

from social_book.views import *

urlpatterns = [
    # path('', Feed.as_view(), name='feed'),
    # path('posts/', Posts.as_view(), name='postsPage'),
    # path('post/<slug:post_slug>', ShowPost.as_view(), name='post'),
    # path('addPostPage/', AddPostPage.as_view(), name='addPostPage'),

    path('', feed, name='feed'),
    path('signup', signup, name='signup'),
    path('signin', signin, name='signin'),
    path('profile/<str:pk>', profile, name='profile'),
    path('logout', logout, name='logout'),
    path('Settings/', Settings, name='Settings'),
    path('like-post', like_post, name='like-post'),
    path('follow', follow, name='follow'),
    path('search', search, name='search'),
    path('upload', upload, name='upload'),
    path('subs-posts', subs_posts, name='subs_posts'),
    path('addCommentPage', AddCommentPage.as_view(), name='addCommentPage'),
    # path('addCommentPage/<slug:post_slug>', AddCommentPage.as_view(), name='addCommentPage'),
]
