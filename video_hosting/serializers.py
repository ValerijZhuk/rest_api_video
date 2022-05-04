from rest_framework import serializers
from .models import Video, Comment


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'likes_count', 'user', 'comments', 'title', 'link')
        model = Video


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('owner', 'video', 'content', 'likes_count')
        model = Comment
