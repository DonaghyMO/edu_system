import os

from django.http import HttpResponse

import os
from django.shortcuts import render, redirect
from resource_manage.forms import VideoUploadForm
from resource_manage.models import Video
from my_decorater import check_login
from django.http import JsonResponse


# Create your views here.
@check_login
def index(request):
    # return redirect("index:shop",permanent=True)
    return render(request, "index/index.html")


@check_login
def upload(request):
    # 请求方法为POST时，执行文件上传
    if request.method == "POST":
        # 获取上传的文件，如果没有文件，就默认为None
        myFile = request.FILES.get("myfile", None)
        if not myFile:
            return HttpResponse("no files for upload")
        # 打开特定的文件进行二进制的写操作
        f = open(os.path.join("/home/mo/videos/test", myFile.name), "wb+")
        # 分块写入文件
        for chunk in myFile.chunks():
            f.write(chunk)
        f.close()
        # 上传完成后支持文件预览
        return HttpResponse("upload over!")
    else:
        # 请求方法为get时，生成文件上传页面
        return render(request, "index/index.html")


@check_login
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('video_list')  # Redirect to a page showing the list of uploaded videos
    else:
        form = VideoUploadForm()
    return render(request, 'resource_manage/video/upload_video.html', {'form': form})


@check_login
def list_videos(request):
    videos = Video.objects.all()
    return render(request, 'resource_manage/video/videos_list.html', {'videos': videos})


@check_login
def video_detail(request, video_id):
    video = Video.objects.get(id=video_id)
    return render(request, 'resource_manage/video/video_manage.html', {'video_url': video.video_file.url,
                                                                       'video_title': video.title,
                                                                       'video_id': video.id})


@check_login
def delete_video(request, video_id):
    if request.method == 'DELETE':
        try:
            resource = Video.objects.get(id=video_id)
            # 删除数据库记录
            resource.delete()
            # 删除本地文件
            os.remove(resource.video_file.path)
            return JsonResponse({'message': '资源删除成功', 'success': 1})
        except Video.DoesNotExist:
            return JsonResponse({'error': '资源不存在'}, status=404)
    else:
        return JsonResponse({'error': '无效的请求方法'}, status=400)
