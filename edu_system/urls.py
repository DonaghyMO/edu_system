from django.contrib import admin

from user_manage import views as user_views
from index import views as index_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from resource_manage import views as resource_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_views.index, name='index'),
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
    path('video/delete/<int:video_id>/',resource_view.delete_video,name='delete_video')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)