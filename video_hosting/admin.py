from django.contrib import admin

from video_hosting.models.models import Video, Comment, User, HashTag

admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(HashTag)
