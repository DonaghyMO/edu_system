from django.db import models

MESSAGE_STATUS = (
    (1, '已发送'),
    (2, '已读'),
    (3, '撤回')
)


class ChatMessage(models.Model):
    """
    咨询信息表
    """
    id = models.AutoField(primary_key=True)
    teacher_id = models.IntegerField()
    stu_id = models.IntegerField()
    # 咨询内容
    content = models.CharField(max_length=200)
    # 咨询时间
    create_time = models.DateTimeField(auto_now=True)
    message_status = models.IntegerField(choices=MESSAGE_STATUS)


class Interact(models.Model):
    """
    互动信息表
    """
    id = models.AutoField(primary_key=True)
    teacher_id = models.IntegerField()
    stu_id = models.IntegerField()
    # 互动内容
    content = models.CharField(max_length=200)
    # 互动时间
    create_time = models.DateTimeField(auto_now=True)
    message_status = models.IntegerField(choices=MESSAGE_STATUS)


class Notification(models.Model):
    """
    通知表
    """
    id = models.AutoField(primary_key=True)
    # 发送的教师id
    teachers = models.JSONField()
    # 发送的学生id
    students = models.JSONField()
    content = models.CharField(max_length=200)
    # 创建用户，只能为老师
    create_user = models.IntegerField()
    # 创建时间
    create_time = models.DateTimeField(auto_now=True)
    # 发送时间
    send_time = models.DateTimeField(auto_now=True)
