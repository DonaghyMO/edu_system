import os
from django.shortcuts import render, redirect
from resource_manage.forms import VideoUploadForm, AudioUploadForm, TextUploadForm, TextUpdateForm
from resource_manage.models import Video, Audio, Text
from my_decorater import check_login
from django.http import JsonResponse, FileResponse


# Create your views here.
@check_login
def index(request):
    # return redirect("index:shop",permanent=True)
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
    category_search = request.GET.get("category_search")
    videos = Video.objects.filter(category=category_search) if category_search else Video.objects.all()
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


@check_login
def list_audios(request):
    category_search = request.GET.get("category_search")
    audios = Audio.objects.filter(category=category_search) if category_search else Audio.objects.all()
    return render(request, 'resource_manage/audio/audio_list.html', {'audios': audios})


@check_login
def upload_audio(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('audio_list')  # Redirect to a page showing the list of uploaded videos
    else:
        form = AudioUploadForm()
    return render(request, 'resource_manage/audio/upload_audio.html', {'form': form})


@check_login
def audio_detail(request, video_id):
    video = Video.objects.get(id=video_id)
    return render(request, 'resource_manage/video/audio_manage.html', {'video_url': video.video_file.url,
                                                                       'video_title': video.title,
                                                                       'video_id': video.id})


@check_login
def delete_audio(request, audio_id):
    if request.method == 'DELETE':
        try:
            resource = Audio.objects.get(id=audio_id)
            # 删除数据库记录
            resource.delete()
            # 删除本地文件
            os.remove(resource.audio_file.path)
            return JsonResponse({'message': '资源删除成功', 'success': 1})
        except Audio.DoesNotExist:
            return JsonResponse({'error': '资源不存在'}, status=404)
    else:
        return JsonResponse({'error': '无效的请求方法'}, status=400)


@check_login
def list_texts(request):
    text_list = []
    if request.method == 'GET':
        category_search = request.GET.get('category_search')
        if category_search:
            texts = Text.objects.filter(category=category_search)
        else:
            texts = Text.objects.all()
        for text in texts:
            with open(text.text_file.path) as f:
                content = f.read()
            form = TextUploadForm(instance=text)
            tmp = {
                "title": text.title,
                "content": content,
                "id": text.id,
                "description": text.description,
                "form": form,
            }

            text_list.append(tmp)
    elif request.method == 'POST':
        text_id = request.POST.get("text_id")
        instance = Text.objects.get(id=text_id)
        new_form = TextUploadForm(request.POST, request.FILES, instance=instance)
        if new_form.is_valid():
            new_form.save()
        return redirect('text_list')

    return render(request, 'resource_manage/text/text_list.html', {'texts': text_list})


@check_login
def upload_text(request):
    if request.method == 'POST':
        form = TextUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('text_list')  # Redirect to a page showing the list of uploaded videos
    else:
        form = TextUploadForm()
    return render(request, 'resource_manage/text/upload_text.html', {'form': form})


@check_login
def text_update(request, text_id):
    if request.method == 'POST':
        name = "content_" + str(text_id)
        content = request.POST.get(name)
        text = Text.objects.get(id=text_id)
        with open(text.text_file.path, "w") as f:
            f.write(content)
    else:
        text = Text.objects.get(id=text_id)
        form = TextUploadForm(instance=text)
        return render(request, 'resource_manage/text/text_update.html', {'form': form})
    return redirect("text_list")


@check_login
def delete_text(request, text_id):
    if request.method == 'DELETE':
        try:
            resource = Text.objects.get(id=text_id)
            # 删除数据库记录
            resource.delete()
            # 删除本地文件
            os.remove(resource.text_file.path)
            return JsonResponse({'message': '资源删除成功', 'success': 1})
        except Text.DoesNotExist:
            return JsonResponse({'error': '资源不存在'}, status=404)
    else:
        return JsonResponse({'error': '无效的请求方法'}, status=400)


# @ check_login
def download_resource(request, resource_type, resource_name):
    from edu_system.settings import BASE_DIR
    if resource_type == 'video':  # 视频类型
        file_path = os.path.join(BASE_DIR, 'upload', 'videos', resource_name)
    elif resource_type == 'audio':  # 音频类型
        file_path = os.path.join(BASE_DIR, 'upload', 'audio', resource_name)
    elif resource_type == 'text':  # 文本类型
        file_path = os.path.join(BASE_DIR, 'upload', 'text', resource_name)
    elif resource_type == 'language': # 页面语言json文件
        file_path = os.path.join(BASE_DIR,'upload','language',resource_name)
    else:
        file_path = os.path.join(BASE_DIR, 'static', 'card_pic.jpg', )
    file = open(file_path, 'rb')
    response = FileResponse(file)
    if resource_type == 4:
        response['Content-Type'] = "image/jpeg"
    return response

