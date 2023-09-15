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
    return render(request,"chenlu/chenlu.html")