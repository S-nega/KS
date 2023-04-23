from django.utils.datetime_safe import datetime
from rest_framework import serializers
from social_book.models import *
from datetime import datetime


class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.HiddenField(default=datetime.now)
    no_of_likes = serializers.HiddenField(default=0)
    class Meta:
        model = Post
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Profile
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Comment
        fields = "__all__"


class FollowersCountSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = FollowersCount
        fields = "__all__"


class LikePostSerializer(serializers.ModelSerializer):
    username = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = LikePost
        fields = "__all__"
