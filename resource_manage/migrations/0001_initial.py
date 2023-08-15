# Generated by Django 4.2.4 on 2023-08-13 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('video_file', models.FileField(upload_to='videos/')),
            ],
        ),
    ]
