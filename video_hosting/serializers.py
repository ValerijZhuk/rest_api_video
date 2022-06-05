from rest_framework import serializers

from video_hosting.models import Channel
from video_hosting.models.models import Video, Comment, HashTag, VideoRecommendation, User
from djoser.serializers import UserCreateSerializer


class UserCreateCustomSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'likes_count', 'user', 'comments', 'title', 'link')
        model = Video


class VideoFullSerializer(serializers.ModelSerializer):
    class Meta:
        # fields = ('__all__')
        exclude = ('link',)
        model = Video


class CommentSerializer(serializers.ModelSerializer):
    # video = VideoSerializer(many=False)

    class Meta:
        fields = ('id', 'owner', 'video', 'content', 'likes_count')
        model = Comment


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("__all__")
        model = HashTag


class VideoRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "videos", "recommendation_name", "is_top_rated")
        model = VideoRecommendation


class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        read_only_fields = ('email',)


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name", "subscribers", "owner")
        model = Channel


class UserSubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "email", "subscriptions")
        model = User


class ChannelsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "owner")
        model = Channel
