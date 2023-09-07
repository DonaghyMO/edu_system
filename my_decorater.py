from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

def check_login(func):
    def wrapper(req,*args,**kwargs):
        if 'user' not in req.COOKIES:
            return redirect('login')  #用于记录访问历史页面，便于登录后跳转
        else:
            return func(req,*args,**kwargs)
    return wrapper