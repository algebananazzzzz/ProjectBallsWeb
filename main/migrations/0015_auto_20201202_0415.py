# Generated by Django 3.1.3 on 2020-12-02 04:15

from django.db import migrations
import sorl.thumbnail.fields
import video_encoding.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20201201_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippetmodel',
            name='thumbnail',
            field=sorl.thumbnail.fields.ImageField(default='images/ulti-skye-bg.jpg', upload_to='users/thumbnails'),
        ),
        migrations.AddField(
            model_name='snippetmodel',
            name='videoFile',
            field=video_encoding.fields.VideoField(default='', upload_to='users/videos'),
            preserve_default=False,
        ),
    ]
