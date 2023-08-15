from django.db import models

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')
