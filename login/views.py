from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from login.models import Teacher

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
        if not check_password(name,password):
            template = loader.get_template("login/login.html")
            return HttpResponse(template.render())
        else:
            response = HttpResponseRedirect('/index')
            response.set_cookie('user', name)
            return response
    template = loader.get_template("login/login.html")
    return HttpResponse(template.render())

def check_password(name,password):
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
