# Generated by Django 4.2.4 on 2024-01-20 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('child_category', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=300, null=True)),
            ],
        ),
    ]
