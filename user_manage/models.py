from django.db import models
from backend.const import ADMIN_CHOICES

# 课程项目，用id存储表示
COURSE_CONST = {"video":[],"audio":[],"content":[]}


class Teacher(models.Model):
    # 教师用户表
    id = models.AutoField(primary_key=True)
    # 默认微信
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50,null=True)
    is_admin = models.IntegerField(choices=ADMIN_CHOICES)
    phone_number = models.CharField(max_length=13,default="")
    # json形式存储课程列表
    courses = models.JSONField(null=True)
    # 微信openid，一个用户和一个小程序对应一个openid
    openid = models.CharField(max_length=200,default="")
    wechat_name = models.CharField(max_length=200,default="")

    """
    增删改查
    """
    def save(self,*args,**kwargs):
        # 保存方法，暂时参数不变
        super().save(*args,**kwargs)


class Student(models.Model):
    # 教师用户表
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    # 默认为openid
    password = models.CharField(max_length=50, null=True)
    # 昵称 默认为为新名
    nick_name = wechat_name = models.CharField(max_length=50,null=True)
    # json格式存储教师id列表
    # TODO：删除教师时级联删除列表中的教师id
    teachers_id = models.TextField(null=True)
    # 最近课程的时间，可以为空
    scheduled_time = models.DateTimeField(null=True)
    # json格式表示预定的课程id
    # TODO:删除课程时级联删除学生预定的课程
    scheduled_class = models.TextField(null=True)
    phone_number = models.CharField(max_length=13,null=True)
    # 用json格式存储课程COURSE_CONST
    courses = models.JSONField(null=True)
    # 微信相关
    # 微信openid，一个用户和一个小程序对应一个openid
    openid = models.CharField(max_length=200,default="")
    wechat_name = models.CharField(max_length=200,default="")

