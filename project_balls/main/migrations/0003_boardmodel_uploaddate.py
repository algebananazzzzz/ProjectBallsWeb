# Generated by Django 3.1.4 on 2021-04-29 11:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210214_0306'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardmodel',
            name='UploadDate',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2021, 4, 29, 11, 37, 9, 685941, tzinfo=utc)),
            preserve_default=False,
        ),
    ]