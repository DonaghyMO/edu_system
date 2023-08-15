from django.contrib import admin

from login import views as login_views
from index import views as index_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from resource_manage import views as resource_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_views.index, name='index'),
    path('index/', index_views.index, name='index'),
    path('login/', login_views.login, name='login_page'),
    path('video/upload/', resource_view.upload_video, name='upload_video'),
    path('videos/',resource_view.list_videos,name='video_list'),
    path('videos/<int:video_id>',resource_view.video_detail,name='video_detail'),
    path('video/delete/<int:video_id>/',resource_view.delete_video,name='delete_video')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)