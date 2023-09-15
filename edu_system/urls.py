from django.contrib import admin

from user_manage import views as user_views
from index import views as index_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from resource_manage import views as resource_view
from chenlu import views as chenlu_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # 登录页
    path('',user_views.login, name='login'),
    path('login/',user_views.login, name='login_index'),
    # 登出
    path('logout/',user_views.logout, name='logout'),
    # 首页
    path('index/', index_views.index, name='index'),
    # 学生管理
    path('user_manage/students_index/', user_views.student_index, name='student_index'),
    path('user_manage/students_register/', user_views.student_register, name='student_register'),
    path('user_manage/students_update/<int:stu_id>',user_views.student_update,name='student_update'),
    path('user_manage/students_delete/<int:stu_id>/',user_views.student_delete,name='student_delete'),
    # 教师管理
    path('user_manage/teachers_index/', user_views.teacher_index, name='teacher_index'),
    path('user_manage/teacher_register/', user_views.teacher_register, name='teacher_register'),
    path('user_manage/teacher_update/<int:teacher_id>', user_views.teacher_update, name='teacher_update'),
    path('user_manage/teacher_delete/<int:teacher_id>/', user_views.teacher_delete, name='teacher_delete'),
    # 视频管理
    path('video/upload/', resource_view.upload_video, name='upload_video'),
    path('videos/',resource_view.list_videos,name='video_list'),
    path('videos/<int:video_id>',resource_view.video_detail,name='video_detail'),
    path('video/delete/<int:video_id>/',resource_view.delete_video,name='delete_video'),
    # 音频管理
    path('audio/upload/', resource_view.upload_audio, name='upload_audio'),
    path('audios/', resource_view.list_audios, name='audio_list'),
    path('audios/<int:audio_id>', resource_view.audio_detail, name='audio_detail'),
    path('audio/delete/<int:audio_id>/', resource_view.delete_audio, name='delete_audio'),
    # 教案管理
    path('text/upload/', resource_view.upload_text, name='upload_text'),
    path('texts/', resource_view.list_texts, name='text_list'),
    path('text/update/<int:text_id>', resource_view.text_update, name='text_update'),
    path('text/delete/<int:text_id>/', resource_view.delete_text, name='delete_text'),
    path('resource/download/<int:resource_type>/<str:resource_name>',resource_view.download_resource,name='download_resource'),
    path('chenlu/',chenlu_view.chenlu_empty_page,name='chenlu_page')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
