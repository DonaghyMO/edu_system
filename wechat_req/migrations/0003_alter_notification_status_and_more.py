# Generated by Django 4.2.4 on 2023-09-15 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_req', '0002_alter_notification_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.IntegerField(choices=[(1, '撤回'), (0, '已传达')], default=0),
        ),
        migrations.AlterField(
            model_name='notification',
            name='target_user_type',
            field=models.IntegerField(choices=[(1, '老师'), (0, '学生')], default=0),
        ),
    ]