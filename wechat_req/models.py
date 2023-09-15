from django.db import models

# Create your models here.
USER_CHOICES = (
    (1,'老师'),
    (0,'学生')
)
NOTIFICATION_STATUS_CHOICES = (
    (1,'撤回'),
    (0,'已传达')
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