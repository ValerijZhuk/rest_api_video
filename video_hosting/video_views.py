from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from rest_framework import status, generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from video_hosting.models.models import Video
from .models import Channel
from .serializers import VideoSerializer, VideoFullSerializer, ChannelsSerializer
from rest_api_video.celery import delete_video, block_user_for_abuse_comments


class VideoView(APIView):

    def post(self, request):
        video_data = request.data
        video = Video.objects.create(**video_data)
        serialized_video = VideoSerializer(video).data
        return Response(serialized_video)

    @method_decorator(cache_page(60 * 2))
    @method_decorator(vary_on_cookie)
    def get(self, request, pk=None):
        try:
            if not pk:
                videos = Video.objects.all()
                serialized_video = VideoSerializer(videos, many=True).data
                block_user_for_abuse_comments.delay()
                delete_video.delay()
                return Response(serialized_video)
            user = request.user
            if user:
                video = Video.objects.filter(id=pk, user=user)
                serialized_video = VideoSerializer(video).data
                return Response(serialized_video)
            video = Video.objects.get(id=pk)
            serialized_video = VideoSerializer(video).data
            return Response(serialized_video)
        except ObjectDoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        data = request.data
        Video.objects.filter(id=pk).update(**data)
        video_updated = Video.objects.get(id=pk)
        serialized_video = VideoSerializer(video_updated).data
        return Response(serialized_video)

    def delete(self, request, pk):
        Video.objects.get(id=pk).delete()
        return Response(status=status.HTTP_200_OK)


class OnlyMyVideoView(generics.ListAPIView):
    serializer_class = VideoFullSerializer

    def get_queryset(self):
        user = self.request.user
        videos = Video.objects.filter(user=user)
        return videos


@permission_classes((IsAuthenticated,))
class ChannelView(APIView):
    def post(self, request):
        channel_name = request.data.get("name")
        channel_owner = request.user
        channel = Channel.objects.create(name=channel_name, owner=channel_owner)
        channel_serialized = ChannelsSerializer(channel).data
        return Response(channel_serialized)

    def get(self, request, pk=None):
        try:
            if not pk:
                channels = Channel.objects.all()
                channels_serialized = ChannelsSerializer(channels, many=True).data
                return Response(channels_serialized)
            channel = Channel.objects.get(id=pk)
            channel_serialized = ChannelsSerializer(channel).data
            return Response(channel_serialized)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        channel = Channel.objects.get(id=pk)
        serializer = ChannelsSerializer(channel, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            channel = Channel.objects.get(id=pk)

        except Channel.DoesNotExist:
            raise Http404
        channel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
