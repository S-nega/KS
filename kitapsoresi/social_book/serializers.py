from django.utils.datetime_safe import datetime
from rest_framework import serializers
from social_book.models import Post
from datetime import datetime


class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.HiddenField(default=datetime.now)
    no_of_likes = serializers.HiddenField(default=0)
    class Meta:
        model = Post
        fields = "__all__"
        # fields = ("id", "user", "image", "caption", "created_at", "no_of_likes")


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.HiddenField(default=datetime.now)
    no_of_likes = serializers.HiddenField(default=0)
    class Meta:
        model = Post
        fields = "__all__"
        # fields = ("id", "user", "image", "caption", "created_at", "no_of_likes")


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.HiddenField(default=datetime.now)
    no_of_likes = serializers.HiddenField(default=0)
    class Meta:
        model = Post
        fields = "__all__"
        # fields = ("id", "user", "image", "caption", "created_at", "no_of_likes")


class FollowersCountSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.HiddenField(default=datetime.now)
    no_of_likes = serializers.HiddenField(default=0)
    class Meta:
        model = Post
        fields = "__all__"
        # fields = ("id", "user", "image", "caption", "created_at", "no_of_likes")


class LikePostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.HiddenField(default=datetime.now)
    no_of_likes = serializers.HiddenField(default=0)
    class Meta:
        model = Post
        fields = "__all__"
        # fields = ("id", "user", "image", "caption", "created_at", "no_of_likes")
