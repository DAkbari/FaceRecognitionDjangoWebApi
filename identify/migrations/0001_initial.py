# Generated by Django 2.1.1 on 2018-09-04 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=200)),
                ('lastName', models.CharField(max_length=200)),
                ('faceEncode', models.FileField(upload_to='')),
                ('facePicture', models.FileField(upload_to='')),
                ('lastLoginPicture', models.FileField(upload_to='')),
                ('code', models.CharField(max_length=100)),
            ],
        ),
    ]
