import json
from tools import doc_reader
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import Notification, ChatContent
from my_decorater import check_login
from anytree.exporter import JsonExporter
from resource_manage.models import Audio, Text, Video
from user_manage.models import Teacher, Student
from category.models import Category
import requests
from anytree import find, PreOrderIter, Node,RenderTree
from backend.dir_tree import get_category_tree_dic, get_category_tree,get_category_node
from .utils import check_invite_code
from edu_system.settings import BASE_DIR
import os
from django.core.exceptions import ObjectDoesNotExist

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
        # teacher_names = []
        results = Teacher.objects.filter(id__in=teachers)
        teacher_names = [i.username for i in results]
        # 再查学生
        students = user.get('student')
        results = Student.objects.filter(id__in=students)
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


def delete_notification(request):
    """
    撤回通知
    """
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        delete_id = int(data.get('delete_id'))
        notification = Notification.objects.get(id=delete_id)
        notification.status = 2
        notification.save()
    return HttpResponse("已删除", status=200)


def wc_login(request):
    """
    直接用微信登录+注册
    """
    if request.method != 'POST':
        return HttpResponse("请求方式有误", status=400)
    data = json.loads(request.body.decode('utf-8'))
    user_type = data.get("user_type")
    password = data.get("password")
    username = data.get("username")

    # 检查用户是否已经存在，如果不存在，则创建用户
    try:
        # TODO：校验是否是老师用户
        user = Teacher.objects.get(username=username) if user_type == "teacher" else Student.objects.get(
            username=username)
        if user.password != password:
            return JsonResponse({"message": "密码错误", "status": "fail"}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "用户不存在", "status": "fail"}, status=200)
    # 这里需要自行实现用户登录逻辑，例如使用 Token 或 Session 等方式
    rejson = {"message": "登录成功", "status": "success", "user_id": user.id, "user_type": user_type,
              "openid": user.openid}
    return JsonResponse(rejson, status=200)


def wc_register(request):
    """
    注册功能
    """
    if request.method != 'POST':
        return HttpResponse("请求方式有误", status=400)
    data = json.loads(request.body.decode('utf-8'))
    username = data.get("username")
    password = data.get("password")
    wechat_name = data.get("wechat_name")
    invite_code = data.get("invite_code")
    code = data.get("code")
    # 获取openid
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid=wxd44159a044a585ad&secret=bc0363f718cdfb030d6d867f32b6d521&js_code={code}&grant_type=authorization_code'
    response = requests.get(url)
    rdata = response.json()
    # 从微信服务器返回的数据中获取用户的唯一标识 openid
    openid = rdata.get('openid')
    # 学生用户注册
    if not invite_code:
        try:
            Student.objects.get(username=username)
            return JsonResponse({"message": "用户名已注册", "status": "fail"}, status=200)
        except Student.DoesNotExist:
            if Student.objects.filter(openid=openid):
                return JsonResponse({"message": "此微信号已经进行过注册", "status": "fail"}, status=200)
            stu = Student(username=username,
                          password=password,
                          nick_name=wechat_name,
                          wechat_name=wechat_name,
                          openid=openid
                          )
            stu.save()
    # 教师用户注册
    else:
        # 邀请吗校验
        if not check_invite_code(invite_code):
            return JsonResponse({"message": "邀请码错误", "status": "fail"}, status=200)
        try:
            Teacher.objects.get(username=username)
            return JsonResponse({"message": "用户名已注册", "status": "fail"}, status=200)
        except Teacher.DoesNotExist:
            if Teacher.objects.filter(openid=openid):
                return JsonResponse({"message": "此微信号已经进行过注册", "status": "fail"}, status=200)
            tea = Teacher(username=username,
                          password=password,
                          nick_name=wechat_name,
                          wechat_name=wechat_name,
                          openid=openid)
            tea.save()

    return JsonResponse({"message": "注册成功", "status": "fail"}, status=200)


def wc_get_notifications(request):
    """
    微信获得通知接口
    """
    user_id = int(request.GET.get("user_id"))
    user_type = request.GET.get('user_type')
    notifications = Notification.objects.filter(status=0)
    tmp = []
    for item in notifications:
        # 1是老师，0是学生
        users = json.loads(item.target_users)['teacher'] if user_type == 'teacher' else json.loads(item.target_users)[
            'student']
        # 这个学生收到了这个消息
        if user_id in users:
            tmp.append(item)
    notifications = [{"content": item.content,
                      "id": item.id} for item in tmp]
    return JsonResponse(notifications, safe=False)


new_root = None


def gen_wx_dir_tree(resource_list,resource_type):
    """
    创建微信小程序用的目录树
    """
    root = get_category_tree()
    preorder_reconstruct(root, resource_list,resource_type)
    exporter = JsonExporter(indent=2, sort_keys=True)
    exporter.export(new_root)
    return exporter.export(new_root)


def preorder_reconstruct(node, resource_list, resource_type,parent=None):
    global new_root
    resources = []
    for res in resource_list:
        if node.name == res["category_id"]:
            res["resource_type"] = resource_type
            resources.append(res)
    new_node = Node(name=node.name, category_name=node.category_name, resources=resources, resource_type=resource_type,parent=parent)
    if new_root is None:
        new_root = new_node
    for child in node.children:
        preorder_reconstruct(child, resource_list, resource_type,new_node)


def wc_get_resource_list(request):
    """
    资源列表页
    """
    resource_type = request.GET.get("resource_type")
    # 根据资源类型获取资源名列表
    resource_list = []
    if resource_type == "video":
        resource_list = [{"title": item.title, "resource_id": item.id, "category_id": item.category_id} for item in
                         Video.objects.all()]
    if resource_type == "audio":
        resource_list = [{"title": item.title, "resource_id": item.id, "category_id": item.category_id} for item in
                         Audio.objects.all()]
    if resource_type == "text":
        resource_list = [{"title": item.title, "resource_id": item.id, "category_id": item.category_id} for item in
                         Text.objects.all()]
    resource_tree = gen_wx_dir_tree(resource_list,resource_type)
    global new_root
    new_root = None
    return JsonResponse({"resource_list": resource_list, "resource_tree": resource_tree}, status=200)

def has_resource(node):
    """
    判断有没有资源
    """
    child_resource_flag = False
    if node.children:
        for child in node.children:
            # 子树中有资源就不删
            if has_resource(child):
                return True
            else:
                pass
    cat_id = int(node.name)

    if Video.objects.filter(category_id=cat_id) or Audio.objects.filter(category_id=cat_id) or Text.objects.filter(category_id=cat_id):
        return True
    return False


def wc_search_resource(request):
    """
    按关键字搜索资源
    """
    keyword = request.GET.get("keyword")
    resource_list = []
    if not keyword:
        return JsonResponse({"resource_list": resource_list})
    # 音频
    for item in Audio.objects.filter(title__icontains=keyword):
        resource_list.append({"type": "audio", "title": item.title, "resource_id": item.id})
    for item in Text.objects.filter(title__icontains=keyword):
        resource_list.append({"type": "text", "title": item.title, "resource_id": item.id})
    for item in Video.objects.filter(title__icontains=keyword):
        resource_list.append({"type": "video", "title": item.title, "resource_id": item.id})
    categories = [{"id": item.id,"category_name": item.name} for item in Category.objects.filter(name__contains=keyword)]
    new_cats = []
    for cate in categories:
        cate_node = get_category_node(cate["id"])
        if has_resource(cate_node):
            new_cats.append(cate)
    return JsonResponse({"resource_list": resource_list,"category_list":new_cats}, status=200)


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

        # # 判断文件类型
        text_type = os.path.splitext(file_path)[1]
        if text_type in [".doc", ".docx"]:
            data = doc_reader.transfer_doc2string(file_path)
        else:
            with open(file_path, 'r') as f:
                data = f.read()
        return JsonResponse({
            "content": data,
            "description": resource.description,
            "title": resource.title
        }, status=200)
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
    return JsonResponse({"user_name": user.username})


def wc_get_chat_list(request):
    """
    获取教师列表
    """
    # 请求用户的类别，教师用户获取所有用户列表，学生用户只能获取教师列表
    user_type = request.GET.get("user_type")
    data = []
    if user_type == "teacher":
        students = Student.objects.all()
        for stu in students:
            data.append({"username": stu.username, 'user_id': stu.id, "user_type": "student"})
    else:
        teachers = Teacher.objects.all()
        for t in teachers:
            data.append({
                "username": t.username,
                "user_id": t.id,
                "user_type": "teacher"
            })
    return JsonResponse(data, status=200, safe=False)


def wc_get_chat_content(request):
    """
    获取聊天内容
    return [{"user_id":user_id,"content":content}]
    """
    if request.method == "GET":
        teacher_id = request.GET.get("teacher_id")
        student_id = request.GET.get("student_id")
        try:
            chat_content = ChatContent.objects.get(teacher_id=teacher_id, student_id=student_id)
        except ChatContent.DoesNotExist:
            chat_content = ChatContent(teacher_id=teacher_id, student_id=student_id, content=json.dumps({}))
            chat_content.save()
        content = json.loads(chat_content.content)
        return JsonResponse({"content": content, "id": chat_content.id}, status=200)


def delete_empty_tree(node, resource_type):
    """
    将目录树中没有资源的摘掉
    """
    child_resource_flag = False
    if node.children:
        for child in node.children:
            # 子树中有资源就不删
            if delete_empty_tree(child, resource_type):
                child_resource_flag = True
            else:
                child.parent = None
    cat_id = int(node.name)
    if resource_type == "video":
        resource_ob = Video
    elif resource_type == "audio":
        resource_ob = Audio
    else:
        resource_ob = Text

    resources = resource_ob.objects.filter(category_id=cat_id)
    if not resources and not child_resource_flag:
        node.parent = None
        return False
    return True
def wc_get_category(request):
    """
    获取目录
    """
    if request.method == "GET":
        resource_type = request.GET.get("resource_type")
        category_id = request.GET.get("category_id")
        if category_id == "-1":
            category_id = -1
        else:
            category_id = int(category_id)
        resources = "video"
        if resource_type == "video":
            resources = [{"id":item.id,"name":item.title} for item in Video.objects.filter(category_id=category_id)]
        elif resource_type == "audio":
            resources = [{"id":item.id,"name":item.title} for item in Audio.objects.filter(category_id=category_id)]
        elif resource_type == "text":
            resources = [{"id":item.id,"name":item.title} for item in Text.objects.filter(category_id=category_id)]

        # 获取当前目录在树中节点
        root = get_category_node(category_id)
        # 只保留有资源的子树
        delete_empty_tree(root, resource_type)
        full_nodes = []
        for pre, fill, node in RenderTree(root):
            full_nodes.append(int(node.name))
        cats = Category.objects.get(id=category_id)
        child_category = [int(i) for i in cats.child_category.split(",") if i!='']
        children = Category.objects.filter(id__in=child_category)
        child_category = [{"id":i.id,"category_name":i.name} for i in children if i.id in full_nodes]

        return JsonResponse({"resources":resources,"child_category":child_category})


def wc_post_chat_content(request):
    """
    上传聊天内容
    """
    return HttpResponse("上传成功", status=200)
