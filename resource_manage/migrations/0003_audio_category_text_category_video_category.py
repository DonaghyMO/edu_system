# Generated by Django 4.2.4 on 2023-08-20 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource_manage', '0002_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='category',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='text',
            name='category',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='video',
            name='category',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]