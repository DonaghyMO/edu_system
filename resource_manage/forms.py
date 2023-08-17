# forms.py

from django import forms
from .models import Video,Audio

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'video_file')

class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = ('title', 'audio_file', 'degree')