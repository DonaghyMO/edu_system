# Generated by Django 4.2.4 on 2023-09-15 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_req', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
