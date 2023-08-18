from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from user_manage.models import Teacher, Student
from user_manage.forms import StudentRegisterForm,TeacherRegisterForm,TeacherUpdateForm
from django.http import JsonResponse
from my_decorater import check_login


def login(request):
    """
    登录页面操作
    :param request:
    :return:
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        # 校验错误，返回登录页面
        if not check_password(name, password):
            template = loader.get_template("user_manage/login.html")
            return HttpResponse(template.render())
        else:
            response = HttpResponseRedirect('/index/')
            response.set_cookie('user', name)
            return response
    template = loader.get_template("user_manage/login.html")
    return HttpResponse(template.render())


def check_password(name, password):
    """
    校验密码
    :param name:
    :param password:
    :return:
    """
    user = Teacher.objects.get(username=name)
    # 没有此用户
    if not user:
        return False
    if user.password == password:
        return True
    return False


@check_login
def student_index(request):
    """
    学生用户管理页
    """

    # 按条件搜索
    if request.GET.get is not None:
        students = Student.objects.all()
        for i in students:
            print(i.username)
    else:
        students = Student.objects.all()
        for i in students:
            print(i.username)
    return render(request, 'user_manage/student_manage_index.html', {'students': students})


@check_login
def student_register(request):
    """
    添加学生
    """
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_index')
    else:
        form = StudentRegisterForm()
        return render(request, 'user_manage/student_register.html', {'form': form})


@check_login
def student_update(request, stu_id):
    """
    修改学生
    """
    stu = Student.objects.get(pk=stu_id)
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST, instance=stu)
        if form.is_valid():
            form.save()
            initial_data = {'username': stu.username,
                            'password': stu.password, 'nick_name': stu.nick_name,
                            'phone_number': stu.phone_number, 'wechat_id': stu.wechat_id,
                            'wechat_name': stu.wechat_name
                            }

    else:
        initial_data = {'username': stu.username,
                        'password': stu.password, 'nick_name': stu.nick_name,
                        'phone_number': stu.phone_number, 'wechat_id': stu.wechat_id,
                        'wechat_name': stu.wechat_name
                        }
        form = StudentRegisterForm(request.GET)
    return render(request, 'user_manage/student_update.html', {"form": form,
                                                               'initial_data': initial_data,
                                                               'stu_id': stu_id})


@check_login
def student_delete(request, stu_id):
    """
    删除学生
    """
    if request.method == 'DELETE':
        try:
            instance = Student.objects.get(id=stu_id)
            # 删除数据库记录
            instance.delete()
            return JsonResponse({'message': '学生删除成功', 'success': 1})
        except Student.DoesNotExist:
            return JsonResponse({'error': '学生不存在'}, status=404)
    else:
        return JsonResponse({'error': '无效的请求方法'}, status=400)


@check_login
def teacher_index(request):
    """
    教师用户管理页
    """
    teachers = Teacher.objects.all()
    return render(request, 'user_manage/teacher_manage_index.html', {'teachers': teachers})

@check_login
def teacher_update(request, teacher_id):
    """
    修改老师
    """
    teacher = Teacher.objects.get(pk=teacher_id)
    initial_data = {'username': teacher.username,
                    'password': teacher.password,
                    'phone_number': teacher.phone_number,
                    }
    if request.method == 'POST':
        form = TeacherUpdateForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            teacher = Teacher.objects.get(pk=teacher_id)
            initial_data = {'username': teacher.username,
                            'password': teacher.password,
                            'phone_number': teacher.phone_number,
                            }

    else:
        form = TeacherUpdateForm(request.GET)
    return render(request, 'user_manage/teacher_update.html', {"form": form,
                                                               'initial_data': initial_data,
                                                               'teacher_id': teacher_id})

@check_login
def teacher_delete(request, teacher_id):
    """
    删除老师
    """
    if request.method == 'DELETE':
        try:
            instance = Teacher.objects.get(pk=teacher_id)
            # 删除数据库记录
            instance.delete()
            return JsonResponse({'message': '老师删除成功', 'success': 1})
        except Teacher.DoesNotExist:
            return JsonResponse({'error': '老师不存在'}, status=404)
    else:
        return JsonResponse({'error': '无效的请求方法'}, status=400)



@check_login
def teacher_register(request):
    """
    添加学生
    """
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_index')
    else:
        form = TeacherRegisterForm()
        return render(request, 'user_manage/teacher_register.html', {'form': form})

