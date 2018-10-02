# Generated by Django 2.1.2 on 2018-10-02 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('identify', '0006_auto_20180909_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='associatedUser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]