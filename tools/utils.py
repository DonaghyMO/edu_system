from category.models import Category
from resource_manage.models import Video, Audio, Text


def list_category(search_id=None, search_list=None, not_in=None):
    """
    查找类别
    """
    if search_id:
        return Category.objects.get(id=search_id)
    elif search_list:
        return Category.objects.filter(id__in=search_list)
    elif not_in:
        return Category.objects.exclude(id__in=not_in)
    return Category.objects.all()


def list_videos_with_category_id(category_id):
    """
    获取指定类别下的视频资源
    """
    videos = Video.objects.filter(category_id=category_id)
    return videos


def list_audios_with_category_id(category_id):
    """
    获取指定类别下的音频资源
    """
    audios = Audio.objects.filter(category_id=category_id)
    return audios


def list_text_with_category_id(category_id):
    """
    获取指定类别下的文本资源
    """
    texts = Text.objects.filter(category_id=category_id)
    return texts
