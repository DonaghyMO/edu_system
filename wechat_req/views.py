import json

from django.shortcuts import render,redirect
from .models import Notification,NOTIFICATION_STATUS_CHOICES

from user_manage.models import Teacher,Student
from django.db.models import Q
# Create your views here.
"""
首页
"""
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
    return render(request,'notification/notifications.html',{'notifications':notifications})

def publish_notification(request):
    """
    发布通知
    """
    if request.method == 'POST':
        if 'content' not in request.POST.keys() or len(request.POST.keys())<2:
            return redirect('get_notifications')

        # TODO:这里应该有更好的实现
        teachers = []
        students = []
        for key,value in request.POST.items():
            if "teacher" in key:
                teachers.append(int(value))
            elif "student" in key:
                students.append(int(value))
        content = request.POST.get('content')
        user_dic = {'teacher':teachers,'student':students}
        dic2str = json.dumps(user_dic)
        notification = Notification(content=content,target_users=dic2str)
        notification.save()
        return redirect('get_notifications')

    teachers = [{'username': i.username, "id": i.id} for i in Teacher.objects.all()]
    students = [{'username': i.username, "id": i.id} for i in Student.objects.all()]
    users = {'teacher': teachers, 'student': students}
    return render(request, 'notification/notification_publish.html', {'users': users})

def withdraw_notification(request):
    """
    撤回通知
    """
    if request.method=='POST':
        id = int(request.POST.get('withdraw_id'))
        notification =Notification.objects.get(id=id)
        notification.status=1
        notification.save()
    return redirect('get_notifications')


"""
搜索页面
"""
"""
我页面
"""
"""
资源列表页
"""
"""
音频资源详情页
"""
"""
视频资源详情页
"""
"""
文本资源详情页
"""