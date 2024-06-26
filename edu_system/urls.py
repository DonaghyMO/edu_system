from django.contrib import admin

from user_manage import views as user_views
from index import views as index_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from resource_manage import views as resource_view
from wechat_req import views as wechat_view
from chenlu import views as chenlu_view
from chat import views as chat_view
from category import views as category_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # 登录页
    path('', user_views.login, name='login'),
    path('login/', user_views.login, name='login_index'),
    # 登出
    path('logout/', user_views.logout, name='logout'),
    # 首页
    path('index/', index_views.index, name='index'),
    # 学生管理
    path('user_manage/students_index/', user_views.student_index, name='student_index'),
    path('user_manage/students_register/', user_views.student_register, name='student_register'),
    path('user_manage/students_update/<int:stu_id>', user_views.student_update, name='student_update'),
    path('user_manage/students_delete/<int:stu_id>/', user_views.student_delete, name='student_delete'),
    # 教师管理
    path('user_manage/teachers_index/', user_views.teacher_index, name='teacher_index'),
    path('user_manage/teacher_register/', user_views.teacher_register, name='teacher_register'),
    path('user_manage/teacher_update/<int:teacher_id>', user_views.teacher_update, name='teacher_update'),
    path('user_manage/teacher_delete/<int:teacher_id>/', user_views.teacher_delete, name='teacher_delete'),
    # 批量处理
    path('resource/multiple_upload', resource_view.multiple_upload, name='multiple_upload'),

    # 视频管理
    path('video/upload/', resource_view.upload_video, name='upload_video'),
    path('videos/', resource_view.list_videos, name='video_list'),
    path('videos/<int:video_id>', resource_view.video_detail, name='video_detail'),
    path('video/delete/<int:video_id>/', resource_view.delete_video, name='delete_video'),
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
    path('resource/download/<str:resource_type>/<str:resource_name>', resource_view.download_resource,
         name='download_resource'),
    path('chenlu/', chenlu_view.chenlu_empty_page, name='chenlu_page'),
    # 类别管理
    path('category/list', category_view.list_categories, name="list_category"),
    path('category/create', category_view.create_category, name='create_category'),
    path('category/delete/<slug:object_id>/', category_view.delete_category, name='delete_category'),
    path('category/update', category_view.update_category, name='update_category'),

    # 微信相关
    path('wechat/notification/', wechat_view.get_notifications, name='get_notifications'),
    path('wechat/notification/publish', wechat_view.publish_notification, name='post_notification'),
    path('wechat/notification/withdraw', wechat_view.withdraw_notification, name='withdraw_notification'),
    path('wechat/notification/delete', wechat_view.delete_notification, name='delete_notification'),
    path('wechat/notification/wx_notification', wechat_view.wc_get_notifications),
    path('wechat/login', wechat_view.wc_login, name='wc_login'),
    path('wechat/get_user_info',wechat_view.wx_get_user_info,name="wc_user_info"),
    path('wechat/resource_list', wechat_view.wc_get_resource_list, name='wc_resource_list'),
    path('wechat/wc_search_resource', wechat_view.wc_search_resource, name='wc_search_resource'),
    path('wechat/resource_detail', wechat_view.wc_resource_detail, name='wc_resource_detail'),
    path('wechat/register', wechat_view.wc_register, name='wc_register'),
    path('wechat/user_info', wechat_view.wc_get_user_info, name='wc_get_user_info'),
    path('wechat/get_chat_list', wechat_view.wc_get_chat_list, name='wc_get_teacher_list'),
    path('wechat/get_chat_content', wechat_view.wc_get_chat_content, name="wc_get_chat_content"),
    path('wechat/get_category',wechat_view.wc_get_category,name="wc_get_category"),
    path('chat/', chat_view.index, name='index'),
    path('chat/<str:room_name>/', chat_view.room, name='room'),
    path('chat/get_chat_logs/<str:room_id>/', chat_view.get_chat_log, name='get_chat_logs')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
