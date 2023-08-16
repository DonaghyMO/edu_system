from django.http import HttpResponseRedirect

def check_login(func):
    def wrapper(req,*args,**kwargs):
        if 'user' not in req.COOKIES:
            return HttpResponseRedirect('/user_manage/')  #用于记录访问历史页面，便于登录后跳转
        else:
            return func(req,*args,**kwargs)
    return wrapper