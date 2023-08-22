from django.db import models
from resource_manage.const import DEGREE_CHOICES


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    # 第一个用户默认自建管理员
    upload_user = models.IntegerField(default=1)
    degree = models.IntegerField(choices=DEGREE_CHOICES,default=1)
    comment_id = models.JSONField(null=True)
    # 类别字段
    category = models.CharField(blank=True,max_length=50)


class Audio(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to='audio/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    upload_user = models.IntegerField(default=1)
    degree = models.IntegerField(choices=DEGREE_CHOICES,default=1)
    # json存储评论id
    comment_id = models.JSONField(null=True)
    # 类别字段
    category = models.CharField(blank=True,max_length=50)

    def __str__(self):
        return self.title


class Text(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    text_file = models.FileField(upload_to='text/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    upload_user = models.IntegerField(default=1)
    degree = models.IntegerField(choices=DEGREE_CHOICES, default=1)
    comment_id = models.JSONField(null=True)
    # 类别字段
    category = models.CharField(blank=True,max_length=50)
