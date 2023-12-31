# Generated by Django 4.2.4 on 2023-08-16 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50, null=True)),
                ('nick_name', models.CharField(max_length=50, null=True)),
                ('teachers_id', models.TextField(null=True)),
                ('scheduled_time', models.DateTimeField(null=True)),
                ('scheduled_class', models.TextField(null=True)),
                ('phone_number', models.CharField(max_length=13)),
                ('courses', models.JSONField(null=True)),
                ('wechat_id', models.CharField(max_length=50)),
                ('wechat_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('is_admin', models.IntegerField(choices=[(1, 'admin'), (0, 'not_admin')])),
                ('wechat_id', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=13)),
                ('courses', models.JSONField(null=True)),
            ],
        ),
    ]
