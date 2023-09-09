from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def chenlu_empty_page(request):
    """
    黄王辰璐
    :param request:
    :return:
    """
    return HttpResponse("chenlu's page")