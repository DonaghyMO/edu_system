from django.db import models

# Create your models here.
USER_CHOICES = (
    (1,'老师'),
    (0,'学生')
)
NOTIFICATION_STATUS_CHOICES = (
    (1,'撤回'),
    (0,'已传达'),
    (2,'已读')
)


class Notification(models.Model):
    class Meta:
        # 自定义表名为 "my_custom_table"
        db_table = 'notification'
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=200, default="")
    # 用户类型
    target_user_type = models.IntegerField(choices=USER_CHOICES,default=0)
    # 目标用户列表
    target_users = models.CharField(max_length=2000)
    # 消息状态
    status = models.IntegerField(choices=NOTIFICATION_STATUS_CHOICES,default=0)
    create_time = models.DateTimeField(auto_now=True)


class ChatContent(models.Model):
    class Meta:
        db_table = "chat_content"
    id = models.AutoField(primary_key=True)
    teacher_id = models.IntegerField(null=False)
    student_id = models.IntegerField(null=False)
    # TODO:这里实现有误，可以改进聊天内容的存储方案
    content = models.TextField(max_length=20000)
    create_time = models.DateTimeField(auto_now=True)
    new_flag = models.BooleanField(default=True)