import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import Notification
from my_decorater import check_login
from resource_manage.models import Audio, Text, Video
from user_manage.models import Teacher, Student
from django.db.models import Q
import requests
from edu_system.settings import BASE_DIR
import os

# Create your views here.
"""
首页
"""


@check_login
def get_notifications(request):
    """
    获取通知列表
    """
    notifications = Notification.objects.all().order_by('-create_time')
    for item in notifications:
        user = json.loads(item.target_users)
        # 先查教师名
        teachers = user.get('teacher')
        query = Q()
        for id in teachers:
            query |= Q(id=id)
        results = Teacher.objects.filter(query)
        teacher_names = [i.username for i in results]
        # 再查学生
        students = user.get('student')
        query = Q()
        for id in students:
            query |= Q(id=id)
        results = Student.objects.filter(query)
        student_names = [i.username for i in results]
        item.teachers = teacher_names
        item.students = student_names
    return render(request, 'notification/notifications.html', {'notifications': notifications})


@check_login
def publish_notification(request):
    """
    发布通知
    """
    if request.method == 'POST':
        if 'content' not in request.POST.keys() or len(request.POST.keys()) < 2:
            return redirect('get_notifications')

        # TODO:这里应该有更好的实现
        teachers = []
        students = []
        for key, value in request.POST.items():
            if "teacher" in key:
                teachers.append(int(value))
            elif "student" in key:
                students.append(int(value))
        content = request.POST.get('content')
        user_dic = {'teacher': teachers, 'student': students}
        dic2str = json.dumps(user_dic)
        notification = Notification(content=content, target_users=dic2str)
        notification.save()
        return redirect('get_notifications')

    teachers = [{'username': i.username, "id": i.id} for i in Teacher.objects.all()]
    students = [{'username': i.username, "id": i.id} for i in Student.objects.all()]
    users = {'teacher': teachers, 'student': students}
    return render(request, 'notification/notification_publish.html', {'users': users})


@check_login
def withdraw_notification(request):
    """
    撤回通知
    """
    if request.method == 'POST':
        id = int(request.POST.get('withdraw_id'))
        notification = Notification.objects.get(id=id)
        notification.status = 1
        notification.save()
    return redirect('get_notifications')


def wc_login(request):
    """
    直接用微信登录+注册
    """
    if request.method != 'POST':
        return HttpResponse("请求方式有误", status=400)
    data = json.loads(request.body.decode('utf-8'))
    nick_name = data.get("nick_name")
    code = data.get("code")
    user_type = data.get("user_type")
    # 向微信服务器发送请求以获取用户信息
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid=wxd44159a044a585ad&secret=bc0363f718cdfb030d6d867f32b6d521&js_code={code}&grant_type=authorization_code'
    response = requests.get(url)
    data = response.json()
    # 从微信服务器返回的数据中获取用户的唯一标识 openid
    openid = data.get('openid')

    # 检查用户是否已经存在，如果不存在，则创建用户
    try:
        # TODO：校验是否是老师用户
        user = Teacher.objects.get(openid=openid) if user_type == "teacher" else Student.objects.get(openid=openid)
    except Teacher.DoesNotExist:
        user = Teacher(username=nick_name,
                       openid=openid,
                       is_admin=0,
                       wechat_name=nick_name)
        user.save()
    except Student.DoesNotExist:
        user = Student(username=nick_name, nick_name=nick_name, openid=openid, wechat_name=nick_name)
        user.save()
    # 创建用户会话，处理用户登录状态
    # 这里需要自行实现用户登录逻辑，例如使用 Token 或 Session 等方式
    rejson = {"user_id": user.id, "user_type": user_type, "openid": openid}
    return JsonResponse(rejson, status=200)


def wc_get_notifications(request):
    """
    为新获得通知接口
    """
    user_id = int(request.GET.get("user_id"))
    user_type = request.GET.get('user_type')
    notifications = Notification.objects.all()
    tmp = []
    for item in notifications:
        # 1是老师，0是学生
        users = json.loads(item.target_users)['teacher'] if user_type == 'teacher' else json.loads(item.target_users)[
            'student']
        # 这个学生收到了这个消息
        if user_id in users:
            tmp.append(item)
    notifications = [item.content for item in tmp]
    return JsonResponse(data=notifications, safe=False)


"""
搜索页面
"""
"""
我页面
"""


def wc_get_resource_list(request):
    """
    资源列表页
    """
    resource_type = request.GET.get("resource_type")
    # 根据资源类型获取资源名列表
    resource_list = []
    if resource_type == "video":
        resource_list = [{"title": item.title, "resource_id": item.id} for item in Video.objects.all()]
    if resource_type == "audio":
        resource_list = [{"title": item.title, "resource_id": item.id} for item in Audio.objects.all()]
    if resource_type == "text":
        resource_list = [{"title": item.title, "resource_id": item.id} for item in Text.objects.all()]
    return JsonResponse({"resource_list": resource_list}, status=200)


def wc_resource_detail(request):
    """
    资源详情页
    """
    resource_type = request.GET.get("resource_type")
    resource_id = int(request.GET.get("resource_id"))
    if resource_type == "video":
        resource = Video.objects.get(id=resource_id)
        resource_name = str(resource.video_file).split('videos/')[1]
    elif resource_type == 'audio':
        resource = Audio.objects.get(id=resource_id)
        resource_name = str(resource.audio_file).split('audio/')[1]
    elif resource_type == 'text':
        resource = Text.objects.get(id=resource_id)
        resource_name = str(resource.text_file).split('text/')[1]
        file_path = os.path.join(BASE_DIR, 'upload', 'text', resource_name)
        with open(file_path,'r') as f:
            data = f.read()
        return JsonResponse({
            "content":data,
            "description":resource.description,
            "title": resource.title
        },status=200)
    description = resource.description
    title = resource.title
    resource_url = "resource/download/{}/{}".format(resource_type, resource_name)
    data = {
        "url": resource_url,
        "description": description,
        "title": title
    }
    return JsonResponse(data, status=200)

def wc_get_user_info(request):
    """
    获取微信用户信息
    """
    user_id = request.GET.get("user_id")
    user_type = request.GET.get("user_type")
    user = Teacher.objects.get(id=user_id) if user_type == "teacher" else Student.objects.get(id=user_id)
    return JsonResponse({"user_name":user.username})
