from .models import Video, Audio, Text

from django import forms
from django.forms import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    initial_text = '当前文件'  # 修改 "Currently" 的文本
    input_text = '选择新文件'  # 修改 "Change" 按钮的文本
    template_name = 'resource_manage/text/text_list.html'  # 指定自定义模板


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'video_file', 'description', "degree", "category")


class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = ('title', 'audio_file', 'degree', 'category', 'description')


class TextUploadForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ('title', 'text_file', 'degree', 'category', 'description')


class TextUpdateForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ('id', 'title', 'text_file', 'degree', 'category', 'description')


class TextMultipleUploadForm(forms.Form):
    degree = forms.CharField()
    description = forms.CharField()
    category_id = forms.CharField(widget=forms.HiddenInput())
    resource_type = forms.CharField(widget=forms.HiddenInput())
    text_files = forms.FileField()


class VideoMultipleUploadForm(forms.Form):
    degree = forms.CharField()
    description = forms.CharField()
    category_id = forms.CharField(widget=forms.HiddenInput())
    resource_type = forms.CharField(widget=forms.HiddenInput())
    video_files = forms.FileField()


class AudioMultipleUploadForm(forms.Form):
    degree = forms.CharField()
    description = forms.CharField()
    category_id = forms.CharField(widget=forms.HiddenInput())
    resource_type = forms.CharField(widget=forms.HiddenInput())
    audio_files = forms.FileField()
