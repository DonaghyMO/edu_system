from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

def chenlu_empty_page(request):
    """
    黄王辰璐
    :param request:
    :return:
    """
    # 判断请求是否为GET方法
    if request.method == "GET":
        user_agent = request.META.get('HTTP_USER_AGENT', '')  # 获取User-Agent
        if 'twitterbot' in user_agent.lower():
            return render(request, "chenlu/chenlu.html")

    # 如果不是GET请求或User-Agent不是twitterbot，渲染foruser.html
    return render(request, "chenlu/foruser.html")