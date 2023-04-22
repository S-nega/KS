from django.contrib.auth.mixins import *
import random
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.core.serializers import json
from django.db.models import JSONField
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, FormView, DetailView
from itertools import chain
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from messenger.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from social_book.forms import CommentForm, ChatMessageForm
from social_book.models import *
from social_book.serializers import *
from .utils import *

#
class Feed(LoginRequiredMixin, DataMixin, ListView):
    model = Post
    template_name = 'social_book/feed.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Новости")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Post.objects.all()
        # сделать сортировку по обратному времени
#
# class ProfilePage(LoginRequiredMixin, DataMixin, DetailView):
#     model = User
#     template_name = 'social_book/profile.html'
#     slug_url_kwarg = 'username'
#     context_object_name = 'user'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Профиль")
#         context = dict(list(context.items()) + list(c_def.items()))
#         return context
#
#     def get_queryset(self):
#         return Post.objects.all()


@login_required(login_url='signin')
def profile(request, user):
    # user_object = User.objects.get(username=pk)
    # user_profile = Profile.objects.get(user=user_object)
    # user_posts = Post.objects.filter(user=user.id)
    # user_posts_length = len(user_posts)
    user = User.objects.get(username=user)
    # profile = Profile.objects.get(user=user.id)
    # posts = Post.objects.get(user=user.id)
    user_menu = menu.copy()


    if not request.user.is_authenticated:
        user_menu.pop(3)


    follower = request.user.username
    user = user

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
        button_style = 'btn-danger'
    else:
        button_text = 'Follow'
        button_style = 'btn-outline-danger'

    user_followers = len(FollowersCount.objects.filter(user=user.id))
    user_following = len(FollowersCount.objects.filter(follower=user.id))

    context = {
        # 'user_object': user_object,
        # 'user_profile': user_profile,
        # 'user_posts': user_posts,
        # 'user_posts_length': user_posts_length,
        'button_text': button_text,
        'button_style': button_style,
        'user_followers': user_followers,
        'user_following': user_following,
        'user': user,
        # 'profile': profile,
        # 'posts': posts,
        'menu': user_menu
    }

    return render(request, 'social_book/profile.html', context=context)


#
# @login_required(login_url='signin')
# def feed(request):
#     # user_object = User.objects.get(username=request.user.username)
#     # user_profile = Profile.objects.get(user=user_object)
#     posts = Post.objects.all()
#     user_menu = menu.copy()
#     login_url = reverse_lazy('login')
#     raise_exception = True
#
#
#     if not request.user.is_authenticated:
#         user_menu.pop(3)
#
#     context = {
#         'title': "Новости",
#         'posts': posts,
#         # 'user_profile': user_profile,
#         'menu': user_menu
#     }
#
#     return render(request, 'social_book/feed.html', context=context)
#

@login_required(login_url='signin')
def subs_posts(request):
    # user_object = User.objects.get(username=request.user.username)
    # user_profile = Profile.objects.get(user=user_object)
    user_menu = menu.copy()

    if not request.user.is_authenticated:
        user_menu.pop(3)


    user_following_list = []

    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    posts = Post.objects.all()

    context = {
        'posts': feed_list,
        # 'user_profile': user_profile,
        'menu': user_menu
    }

    return render(request, 'social_book/subs_post.html', context=context)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')

        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'social_book/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect('signin')

    return render(request, 'social_book/signin.html')


def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def Settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') is None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            number = request.POST['number']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.number = number
            user_profile.save()

        if request.FILES.get('image') is not None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            number = request.POST['number']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.number = number
            user_profile.save()
        messages.info(request, 'Information updated')
        return redirect('settings')

    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(3)

    context = {
        'title': 'Main Page',
        'menu': user_menu,
        'user_profile': user_profile
    }
    return render(request, 'social_book/settings.html', context=context)


@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        try:
            new_post = Post.objects.create(user=user, image=image, caption=caption)
            new_post.save()
        except IntegrityError:
            messages.error(request, 'An error occurred while saving your post. Please try again later.')
            return redirect(request.META['HTTP_REFERER'])

        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter is None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect(request.META['HTTP_REFERER'])
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect(request.META['HTTP_REFERER'])



@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/' + user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/' + user)
    else:
        return render(request, 'social_book/profile.html', )


@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'social_book/search.html',
                  {'user_profile': user_profile, 'username_profile_list': username_profile_list})



class AddCommentPage(LoginRequiredMixin, DataMixin, FormView):
    form_class = CommentForm
    template_name = 'social_book/addCommentPage.html'
    success_url = reverse_lazy('feed')
    login_url = reverse_lazy('login')
    raise_exception = True

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Оставить комментарий")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('feed')


# class PostAPIList(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
# class PostAPIUpdate(generics.UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
# class PostAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )
    # permission_classes = (IsOwnerOrReadOnly, )

class PostAPIList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, )

class PostAPIUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)
#
# class PostAPIUpdate(generics.RetrieveUpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = (IsOwnerOrReadOnly, )

class PostAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAdminOrReadOnly, )
    # permission_classes = (IsAdminOrOwnerOrReadOnly, ) #or admin
    # permission_classes = (IsAdminOrReadOnly, ) #or admin

#
    # def get_queryset(self):
    #     pk = self.kwargs.get("pk")
    #
    #     if not pk:
    #         return Post.objects.all()[:3]
    #
    #     return Post.objects.filter(pk=pk)




#
#
# @login_required(login_url='signin')
# def feed(request):
#     user_object = User.objects.get(username=request.user.username)
#     user_profile = Profile.objects.get(user=user_object)
#
#     all_user = User.objects.all()
#     user_following_all = []
#
#     for user in user_following_all:
#         user_list = User.objects.get(username=user.user)
#         user_following_all.append(user_list)
#
#     new_suggestions_list = [x for x in list(all_user) if (x not in list(user_following_all))]
#     current_user = User.objects.filter(username=request.user.username)
#     final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
#     random.shuffle(final_suggestions_list)
#
#     username_profile = []
#     username_profile_list = []
#
#     for users in final_suggestions_list:
#         username_profile.append(users.id)
#
#     for ids in username_profile:
#         profile_lists = Profile.objects.filter(id_user=ids)
#         username_profile_list.append(profile_lists)
#
#     suggestions_username_profile_list = list(chain(*username_profile_list))
#
#     posts = Post.objects.all()
#
#     context = {
#         'posts': posts,
#         'user_profile': user_profile,
#         'suggestions_username_profile_list': suggestions_username_profile_list[:4],
#     }
#
#     return render(request, 'social_book/feed.html', context=context)
#
#
# @login_required(login_url='signin')
# def friends(request):
#     friends = Friend.objects.all()
#
#     context = {
#         'friends': friends
#     }
#
#     return render(request, 'social_book/friends.html', context=context)
#
#
# @login_required(login_url='signin')
# def friend(request, pk):
#     friend = Friend.objects.get(profile_id=pk)
#     user = Profile.objects.get(user=request.user)
#     profile = Profile.objects.get(id=friend.profile.id)
#     chats = ChatMessage.objects.all()
#     rec_chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user, seen=False)
#     rec_chats.update(seen=True)
#     form = ChatMessageForm()
#     if request.method == "POST":
#         form = ChatMessageForm(request.POST)
#         if form.is_valid():
#             chat_message = form.save(commit=False)
#             chat_message.msg_sender = user
#             chat_message.msg_receiver = profile
#             chat_message.save()
#             return redirect("friend", pk=friend.profile.id)
#     context = {
#         "friend": friend,
#         "form": form,
#         "user": user,
#         "profile": profile,
#         "chats": chats,
#         "num": rec_chats.count()}
#     return render(request, "social_book/friend.html", context)
#
#
# def sentMessages(request, pk):
#     data = json.loads(request.body)
#     user = Profile.objects.get(user=request.user)
#     friend = Friend.objects.get(profile_id=pk)
#     profile = Profile.objects.get(id=friend.profile.id)
#     new_chat = data["msg"]
#     new_chat_message = ChatMessage.objects.create(body=new_chat, msg_sender=user, msg_receiver=profile, seen=False)
#     print(new_chat)
#     return JsonResponse(new_chat_message.body, safe=False)
#
#
# def receivedMessages(request, pk):
#     user = Profile.objects.get(user=request.user)
#     friend = Friend.objects.get(profile_id=pk)
#     profile = Profile.objects.get(id=friend.profile.id)
#     arr = []
#     chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
#
#     for chat in chats:
#         arr.append(chat.body)
#
#     return JsonResponse(arr, safe=False)
#
#
#
# @login_required(login_url='signin')
# def subs_posts(request):
#     user_object = User.objects.get(username=request.user.username)
#     user_profile = Profile.objects.get(user=user_object)
#
#     user_following_list = []
#
#     feed = []
#
#     user_following = FollowersCount.objects.filter(follower=request.user.username)
#
#     for users in user_following:
#         user_following_list.append(users.user)
#
#     for usernames in user_following_list:
#         feed_lists = Post.objects.filter(user=usernames)
#         feed.append(feed_lists)
#
#     feed_list = list(chain(*feed))
#
#     all_user = User.objects.all()
#     user_following_all = []
#
#     for user in user_following_all:
#         user_list = User.objects.get(username=user.user)
#         user_following_all.append(user_list)
#
#     new_suggestions_list = [x for x in list(all_user) if (x not in list(user_following_all))]
#     current_user = User.objects.filter(username=request.user.username)
#     final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
#     random.shuffle(final_suggestions_list)
#
#     username_profile = []
#     username_profile_list = []
#
#     for users in final_suggestions_list:
#         username_profile.append(users.id)
#
#     for ids in username_profile:
#         profile_lists = Profile.objects.filter(id_user=ids)
#         username_profile_list.append(profile_lists)
#
#     suggestions_username_profile_list = list(chain(*username_profile_list))
#
#     context = {
#         'posts': feed_list,
#         'user_profile': user_profile,
#         'suggestions_username_profile_list': suggestions_username_profile_list[:4],
#     }
#
#     return render(request, 'social_book/subs_post.html', context=context)
#
#
# def signup(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         password2 = request.POST['password2']
#         if password == password2:
#             if User.objects.filter(email=email).exists():
#                 messages.info(request, 'Email taken')
#                 return redirect('signup')
#             elif User.objects.filter(username=username).exists():
#                 messages.info(request, 'Username Taken')
#                 return redirect('signup')
#             else:
#                 user = User.objects.create_user(username=username, email=email, password=password)
#                 user.save()
#
#                 user_login = auth.authenticate(username=username, password=password)
#                 auth.login(request, user_login)
#
#                 user_model = User.objects.get(username=username)
#                 new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
#                 new_profile.save()
#                 return redirect('settings')
#
#         else:
#             messages.info(request, 'Password Not Matching')
#             return redirect('signup')
#     else:
#         return render(request, 'social_book/signup.html')
#
#
# def signin(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#
#         user = auth.authenticate(username=username, password=password)
#
#         if user is not None:
#             auth.login(request, user)
#             return redirect('/')
#         else:
#             messages.info(request, 'Credentials invalid')
#             return redirect('signin')
#
#     return render(request, 'social_book/signin.html')
#
#
# def logout(request):
#     auth.logout(request)
#     return redirect('signin')
#
#
# @login_required(login_url='signin')
# def Settings(request):
#     user_profile = Profile.objects.get(user=request.user)
#
#     if request.method == 'POST':
#         if request.FILES.get('image') is None:
#             image = user_profile.profileimg
#             bio = request.POST['bio']
#             location = request.POST['location']
#             number = request.POST['number']
#
#             user_profile.profileimg = image
#             user_profile.bio = bio
#             user_profile.location = location
#             user_profile.number = number
#             user_profile.save()
#
#         if request.FILES.get('image') is not None:
#             image = request.FILES.get('image')
#             bio = request.POST['bio']
#             location = request.POST['location']
#             number = request.POST['number']
#
#             user_profile.profileimg = image
#             user_profile.bio = bio
#             user_profile.location = location
#             user_profile.number = number
#             user_profile.save()
#         messages.info(request, 'Information updated')
#         return redirect('settings')
#
#     return render(request, 'social_book/settings.html', {'user_profile': user_profile})
#
#
# @login_required(login_url='signin')
# def like_post(request):
#     username = request.user.username
#     post_id = request.GET.get('post_id')
#
#     post = Post.objects.get(id=post_id)
#
#     like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
#
#     if like_filter is None:
#         new_like = LikePost.objects.create(post_id=post_id, username=username)
#         new_like.save()
#         post.no_of_likes = post.no_of_likes + 1
#         post.save()
#         return redirect(request.META['HTTP_REFERER'])
#     else:
#         like_filter.delete()
#         post.no_of_likes = post.no_of_likes - 1
#         post.save()
#         return redirect(request.META['HTTP_REFERER'])
#
#
# @login_required(login_url='signin')
# def upload(request):
#     if request.method == 'POST':
#         user = request.user.username
#         image = request.FILES.get('image_upload')
#         caption = request.POST['caption']
#
#         try:
#             new_post = Post.objects.create(user=user, image=image, caption=caption)
#             new_post.save()
#         except IntegrityError:
#             messages.error(request, 'An error occurred while saving your post. Please try again later.')
#             return redirect(request.META['HTTP_REFERER'])
#
#         return redirect(request.META['HTTP_REFERER'])
#     else:
#         return redirect(request.META['HTTP_REFERER'])
#
#
# @login_required(login_url='signin')
# def updatepost(request):
#     if request.method == 'POST':
#         pk = request.POST['pk']
#         post = Post.objects.get(id=pk)
#
#         if request.FILES.get('image') is None:
#             image = post.image
#             caption = request.POST['caption']
#
#             post.image = image
#             post.caption = caption
#             post.save()
#             messages.info(request, 'Изменения сохранены')
#             return redirect(request.META['HTTP_REFERER'], )
#         if request.FILES.get('image') is not None:
#             image = request.FILES.get('image')
#             caption = request.POST['caption']
#             post.image = image
#             post.caption = caption
#             post.save()
#             messages.info(request, 'Изменения сохранены')
#             return redirect(request.META['HTTP_REFERER'], )
#     return redirect(request.META['HTTP_REFERER'], )
#
#
# @login_required(login_url='signin')
# def deletepost(request):
#     if request.method == 'POST':
#         pk = request.POST['pk']
#         posts = Post.objects.filter(id=pk)
#         posts.delete()
#         messages.info(request, 'Публикация удалена')
#         return redirect(request.META['HTTP_REFERER'], )
#     messages.info(request, 'Публикация удалена')
#     return redirect(request.META['HTTP_REFERER'], )
#
#
# @login_required(login_url='signin')
# def profile(request, pk):
#     user_object = User.objects.get(username=pk)
#     print(pk)
#     user_profile = Profile.objects.get(user=user_object)
#     user_posts = Post.objects.filter(user=pk)
#     user_posts_length = len(user_posts)
#
#     follower = request.user.username
#     user = pk
#
#     if FollowersCount.objects.filter(follower=follower, user=user).first():
#         button_text = 'Unfollow'
#         button_style = 'btn-danger'
#     else:
#         button_text = 'Follow'
#         button_style = 'btn-outline-danger'
#
#     user_followers = len(FollowersCount.objects.filter(user=pk))
#     user_following = len(FollowersCount.objects.filter(follower=pk))
#
#     context = {
#         'user_object': user_object,
#         'user_profile': user_profile,
#         'user_posts': user_posts,
#         'user_posts_length': user_posts_length,
#         'button_text': button_text,
#         'button_style': button_style,
#         'user_followers': user_followers,
#         'user_following': user_following,
#     }
#
#     return render(request, 'social_book/profile.html', context=context)
#
#
# @login_required(login_url='signin')
# def follow(request):
#     if request.method == 'POST':
#         follower = request.POST['follower']
#         user = request.POST['user']
#
#         if FollowersCount.objects.filter(follower=follower, user=user).first():
#             delete_follower = FollowersCount.objects.get(follower=follower, user=user)
#             delete_follower.delete()
#             return redirect('/profile/' + user)
#         else:
#             new_follower = FollowersCount.objects.create(follower=follower, user=user)
#             new_follower.save()
#             return redirect('/profile/' + user)
#     else:
#         return render(request, 'social_book/profile.html', )
#
#
# @login_required(login_url='signin')
# def search(request):
#     user_object = User.objects.get(username=request.user.username)
#     user_profile = Profile.objects.get(user=user_object)
#
#     if request.method == 'POST':
#         username = request.POST['username']
#         username_object = User.objects.filter(username__icontains=username)
#
#         username_profile = []
#         username_profile_list = []
#
#         for users in username_object:
#             username_profile.append(users.id)
#
#         for ids in username_profile:
#             profile_lists = Profile.objects.filter(id_user=ids)
#             username_profile_list.append(profile_lists)
#
#         username_profile_list = list(chain(*username_profile_list))
#     return render(request, 'social_book/search.html',
#                   {'user_profile': user_profile, 'username_profile_list': username_profile_list})
#
#
# def post(request, pk):
#     post_detail = Post.objects.get(id=pk)
#
#     context = {
#         'post': post_detail,
#     }
#
#     return render(request, 'social_book/post.html', context)
#
#
# def addcomment(request):
#     if request.method == 'POST':
#         user = request.user.username
#
#         comment_body = request.POST['comment_body']
#         pk = request.POST['pk']
#         posts = Post.objects.get(id=pk)
#
#         c = Comment(post=posts, commenter_name=user, comment_body=comment_body, date_added=datetime.now())
#         c.save()
#
#         print(user)
#         print(comment_body)
#         return redirect(request.META['HTTP_REFERER'])
#
#     return redirect(request.META['HTTP_REFERER'], )
#
#
# def deletecomment(request):
#     if request.method == 'POST':
#         pk = request.POST['pk']
#         comment = Comment.objects.filter(id=pk)
#         comment.delete()
#         return redirect(request.META['HTTP_REFERER'], )
#     return redirect(request.META['HTTP_REFERER'], )
#
#
# class PostAPIView(APIView):
#
#     def get(self, request):
#         p = Post.objects.all()
#         return Response({'posts': PostSerializer(p, many=True).data})
#
#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'post': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method put not allowed"})
#
#         try:
#             instance = Post.objects.get(pk=pk)
#         except:
#             return Response({"error": "oBject doesnt not exists"})
#
#         serializer = PostSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"post": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"})
#
#         try:
#             record = Post.objects.get(pk=pk)
#             record.delete()
#         except:
#             return Response({"error": "Object does not exists"})
#
#         return Response({"post": "delete post " + str(pk)})
#
#
# class ProfileAPIView(APIView):
#
#     def get(self, request):
#         p = Profile.objects.all()
#         return Response({'profile': ProfileSerializer(p, many=True).data})
#
#     def post(self, request):
#         serializer = ProfileSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'profile': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method put not allowed"})
#
#         try:
#             instance = Profile.objects.get(pk=pk)
#         except:
#             return Response({"error": "oBject doesnt not exists"})
#
#         serializer = ProfileSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"post": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"})
#
#         try:
#             record = Profile.objects.get(pk=pk)
#             record.delete()
#         except:
#             return Response({"error": "Object does not exists"})
#
#         return Response({"post": "delete post " + str(pk)})
#
#
# class CommentAPIView(APIView):
#
#     def get(self, request):
#         p = Comment.objects.all()
#         return Response({'comment': CommentSerializer(p, many=True).data})
#
#     def post(self, request):
#         serializer = CommentSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'comment': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method put not allowed"})
#
#         try:
#             instance = Comment.objects.get(pk=pk)
#         except:
#             return Response({"error": "oBject doesnt not exists"})
#
#         serializer = CommentSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"Comment": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"})
#
#         try:
#             record = Comment.objects.get(pk=pk)
#             record.delete()
#         except:
#             return Response({"error": "Object does not exists"})
#
#         return Response({"post": "delete post " + str(pk)})
#
#
# class FollowersCountAPIView(APIView):
#
#     def get(self, request):
#         p = FollowersCount.objects.all()
#         return Response({'FollowersCount': FollowersCountSerializer(p, many=True).data})
#
#     def post(self, request):
#         serializer = FollowersCountSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'FollowersCount': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method put not allowed"})
#
#         try:
#             instance = FollowersCount.objects.get(pk=pk)
#         except:
#             return Response({"error": "oBject doesnt not exists"})
#
#         serializer = FollowersCountSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"FollowersCount": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"})
#
#         try:
#             record = FollowersCount.objects.get(pk=pk)
#             record.delete()
#         except:
#             return Response({"error": "Object does not exists"})
#
#         return Response({"post": "delete post " + str(pk)})
#
#
# class LikePostAPIView(APIView):
#
#     def get(self, request):
#         p = LikePost.objects.all()
#         return Response({'LikePost': LikePostSerializer(p, many=True).data})
#
#     def post(self, request):
#         serializer = LikePostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'LikePost': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method put not allowed"})
#
#         try:
#             instance = LikePostSerializer.objects.get(pk=pk)
#         except:
#             return Response({"error": "oBject doesnt not exists"})
#
#         serializer = LikePostSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"LikePost": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"})
#
#         try:
#             record = LikePost.objects.get(pk=pk)
#             record.delete()
#         except:
#             return Response({"error": "Object does not exists"})
#
#         return Response({"post": "delete post " + str(pk)})
