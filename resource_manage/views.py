import os, base64
from django.shortcuts import render, redirect
from resource_manage.forms import VideoUploadForm, AudioUploadForm, TextUploadForm, TextUpdateForm, \
    TextMultipleUploadForm,VideoMultipleUploadForm,AudioMultipleUploadForm
from resource_manage.models import Video, Audio, Text
from my_decorater import check_login
from django.http import JsonResponse, FileResponse
from django.core.exceptions import ObjectDoesNotExist
from category.exception import NotValidCategory
from .excptions import *
import traceback
from tools.utils import list_category


# Create your views here.
@check_login
def index(request):
    # return redirect("index:shop",permanent=True)
    return render(request, "index/index.html")


@check_login
def upload_video(request):
    if request.method == 'POST':
        try:
            form = VideoUploadForm(request.POST, request.FILES)
            if form.is_valid():
                form_instance = form.save(commit=False)
                # 转码
                uploaded_file = form_instance.video_file
                video_name = form_instance.video_file.name
                video_name = str(base64.b64encode(video_name.encode("utf-8"))) + ".mp4"
                uploaded_file.name = video_name
                form.instance.category = list_category(search_id=int(request.POST.get("category_id"))).name
                form.instance.category_id = int(request.POST.get("category_id"))
                form.save()

                return redirect('video_list')  # Redirect to a page showing the list of uploaded videos
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("类别{}不存在".format(form.cleaned_data["category_id"]))
    else:
        form = VideoUploadForm()
        cats = [(item.id, item.name) for item in list_category(not_in=[-1])]
    return render(request, 'resource_manage/video/upload_video.html', {'form': form, "cats": cats})


@check_login
def list_videos(request):
    category_search = request.GET.get("category_search")
    name_search = request.GET.get("name_search")
    if category_search:
        videos = Video.objects.filter(category__contains=category_search)
    elif name_search:
        videos = Video.objects.filter(title__contains=name_search)
    else:
        videos = Video.objects.all()
    # for video in videos:
    #     video.category =
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
    name_search = request.GET.get("name_search")
    if category_search:
        audios = Audio.objects.filter(category__contains=category_search)
    elif name_search:
        audios = Audio.objects.filter(title__contains=name_search)
    else:
        audios = Audio.objects.all()

    return render(request, 'resource_manage/audio/audio_list.html', {'audios': audios})


@check_login
def upload_audio(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.category_id = int(request.POST.get("category_id"))
            form.instance.category = list_category(search_id=int(request.POST.get("category_id"))).name
            form.save()
            return redirect('audio_list')  # Redirect to a page showing the list of uploaded videos
    else:
        form = AudioUploadForm()
        cats = [(item.id, item.name) for item in list_category(not_in=[-1])]
    return render(request, 'resource_manage/audio/upload_audio.html', {'form': form, "cats": cats})


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
        category_search = request.GET.get("category_search")
        name_search = request.GET.get("name_search")
        if category_search:
            texts = Text.objects.filter(category__contains=category_search)
        elif name_search:
            texts = Text.objects.filter(title__contains=name_search)
        else:
            texts = Text.objects.all()
        for text in texts:
            text_type = os.path.splitext(text.text_file.path)[1]
            if text_type in [".doc", ".docx"]:
                from tools import doc_reader
                content = doc_reader.transfer_doc2string(text.text_file.path)

            else:
                with open(text.text_file.path) as f:
                    content = f.read()
            form = TextUploadForm(instance=text)
            tmp = {
                "title": text.title,
                "content": content,
                "id": text.id,
                "description": text.description,
                "form": form,
                "category": text.category,
                "category_id": text.category_id,
            }
            text_list.append(tmp)
        cats = [(item.id, item.name) for item in list_category(not_in=[-1])]
    elif request.method == 'POST':
        if not request.POST.get("category_id"):
            raise NotValidCategory()
        text_id = request.POST.get("text_id")
        category_id = int(request.POST.get("category_id"))
        category = list_category(search_id=category_id).name
        instance = Text.objects.get(id=text_id)
        new_form = TextUploadForm(request.POST, request.FILES, instance=instance)
        if new_form.is_valid():
            new_form.instance.category_id = category_id
            new_form.instance.category = category
            new_form.save()
        return redirect('text_list')

    return render(request, 'resource_manage/text/text_list.html', {'texts': text_list, 'cats': cats})


@check_login
def upload_text(request):
    if request.method == 'POST':
        form = TextUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if not (request.POST.get("category_id")):
                raise NotValidCategory()
            form.instance.category_id = int(request.POST.get("category_id"))
            form.instance.category = list_category(search_id=int(request.POST.get("category_id"))).name
            form.save()
            return redirect('text_list')  # Redirect to a page showing the list of uploaded videos
    else:
        form = TextUploadForm()
        cats = [(item.id, item.name) for item in list_category(not_in=[-1])]
    return render(request, 'resource_manage/text/upload_text.html', {'form': form, "cats": cats})


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


def handle_uploaded_file(file_path, file):
    from django.conf import settings
    media_root = settings.MEDIA_ROOT
    # 构建保存路径
    save_path = os.path.join(media_root, file_path, file.name)
    print(save_path)
    # 打开一个文件，写入上传文件的内容
    with open(save_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return os.path.join(file_path, file.name)


@check_login
def multiple_upload(request):
    """
    批量上传
    """
    if request.method == "GET":
        resource_type = request.GET.get("resource_type")
        category_id = request.GET.get("category_id")
        cat = list_category(search_id=int(category_id))
        if resource_type == "text":
            form = TextUploadForm()
            return render(request, "resource_manage/multiple_upload_text.html", {"form": form, "cat": cat})
        elif resource_type == "audio":
            form = AudioUploadForm()
            return render(request, "resource_manage/multiple_upload_audio.html", {"form": form, "cat": cat})
        elif resource_type == "video":
            form = VideoUploadForm()
            return render(request, "resource_manage/multiple_upload_video.html", {"form": form, "cat": cat})
        else:
            raise Exception("不支持的批量上传类别")
    else:
        resource_type = request.POST.get("resource_type")
        category_id = int(request.POST.get("category_id"))
        category = list_category(search_id=category_id).name
        if resource_type == "text":
            try:
                form = TextMultipleUploadForm(request.POST, request.FILES)
                if form.is_valid():
                    uploaded_files = request._files.getlist('text_files')
                    degree = form.cleaned_data['degree']
                    description = form.cleaned_data['description']

                    for file in uploaded_files:

                        file_path = handle_uploaded_file("text", file)
                        text = Text(title=file.name, text_file=file_path, degree=degree,
                                    description=description, category=category, category_id=category_id)
                        text.save()
                        # Text(degree=degree, description=description,title=file.)
                        # with open('path/to/uploaded/files/' + file.name, 'wb') as destination:
                        #     for chunk in file.chunks():
                        #         destination.write(chunk)
                    return redirect("text_list")
            except Exception as e:
                traceback.print_exc()
                raise e
        elif resource_type == "video":
            form = VideoMultipleUploadForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_files = request._files.getlist('video_files')
                degree = form.cleaned_data['degree']
                description = form.cleaned_data['description']
                for file in uploaded_files:
                    file_path = handle_uploaded_file("videos", file)
                    video = Video(title=file.name, video_file=file_path, degree=degree,
                                description=description, category=category, category_id=category_id)
                    video.save()
            return redirect("video_list")
        elif resource_type == "audio":
            form = AudioMultipleUploadForm(request.POST, request.FILES)
            print(form.errors)
            if form.is_valid():
                uploaded_files = request._files.getlist('audio_files')
                degree = form.cleaned_data['degree']
                description = form.cleaned_data['description']
                for file in uploaded_files:
                    file_path = handle_uploaded_file("audio", file)
                    audio = Audio(title=file.name, audio_file=file_path, degree=degree,
                                  description=description, category=category, category_id=category_id)
                    audio.save()
            return redirect("audio_list")
        return redirect("text_list")


# @ check_login
def download_resource(request, resource_type, resource_name):
    from edu_system.settings import BASE_DIR
    if resource_type == 'video':  # 视频类型
        file_path = os.path.join(BASE_DIR, 'upload', 'videos', resource_name)
    elif resource_type == 'audio':  # 音频类型
        file_path = os.path.join(BASE_DIR, 'upload', 'audio', resource_name)
    elif resource_type == 'text':  # 文本类型
        file_path = os.path.join(BASE_DIR, 'upload', 'text', resource_name)
    elif resource_type == 'language':  # 页面语言json文件
        file_path = os.path.join(BASE_DIR, 'upload', 'language', resource_name)
    else:
        file_path = os.path.join(BASE_DIR, 'static', 'card_pic.jpg', )
    print(resource_type)
    print(resource_name)
    file = open(file_path, 'rb')
    response = FileResponse(file)
    if resource_type == 4:
        response['Content-Type'] = "image/jpeg"
    return response
