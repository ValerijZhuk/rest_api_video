from django.urls import path
from video_hosting.views import VideoList, VideoDetail, CommentList, CommentDetail

urlpatterns = [

    path('video/', VideoList.as_view(), name='video-list'),
    path('video/<int:pk>', VideoDetail.as_view(), name='video'),
    path('comment/', CommentList.as_view(), name='video-list'),
    path('comment/<int:pk>', CommentDetail.as_view(), name='video'),

]
