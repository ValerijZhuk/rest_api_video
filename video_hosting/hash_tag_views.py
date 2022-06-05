from rest_framework import generics

from video_hosting.models.models import HashTag
from video_hosting.pagination import HashTagPagination
from video_hosting.serializers import HashTagSerializer


class HashTagListCreateView(generics.ListCreateAPIView):
    serializer_class = HashTagSerializer
    queryset = HashTag.objects.all()
    pagination_class = HashTagPagination


class HashTagRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HashTagSerializer
    queryset = HashTag.objects.all()

    # def get_queryset(self):
    #     id = self.kwargs["id"]
    #     hast_tags = HashTag.objects.filter(id=id)
    #     return hast_tags
