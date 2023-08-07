from django.db import models
from backend.const import ADMIN_CHOICES

class Teacher(models.Model):
    # 教师用户表
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    is_admin = models.IntegerField(choices=ADMIN_CHOICES)
    wechat_id = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13)
    # json形式存储课程列表
    courses = models.CharField(max_length=2000)

    """
    增删改查
    """
    def save(self,*args,**kwargs):
        # 保存方法，暂时参数不变
        super().save(*args,**kwargs)

# class Student(models.Model):
#     # 教师用户表
#     id = models.AutoField(primary_key=True)
#     # json格式存储教师id列表
#     # TODO：删除教师时级联删除列表中的教师id
#     teachers_id = models.TextField(null=True)
#     # 最近课程的时间，可以为空
#     scheduled_time = models.DateTimeField(null=True)
#     # json格式表示预定的课程id
#     # TODO:删除课程时级联删除学生预定的课程
#     scheduled_class = models.TextField(null=True)
#     phone_number = models.CharField(max_length=13)
#     """
#     增删改查
#     """
#     def save(self,*args,**kwargs):
#         # 保存方法，暂时参数不变
#         super().save(*args,**kwargs)
