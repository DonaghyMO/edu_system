from django.http import HttpResponse
from django.template import loader
from my_decorater import check_login


@check_login
def index(request):
    """
    首页
    :param request:
    :return:
    """
    if request.method == 'POST':
        template = loader.get_template("index/index.html")
        return HttpResponse(template.render())
    else:
        template = loader.get_template("index/index.html")
        return HttpResponse(template.render())
