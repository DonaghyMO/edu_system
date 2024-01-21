from django.db import models

# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    # 子类别列表，json存储
    child_category = models.CharField(max_length=500)
    # 描述
    description = models.CharField(max_length=300, null=True)