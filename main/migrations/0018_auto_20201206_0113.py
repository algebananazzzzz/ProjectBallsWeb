# Generated by Django 3.1.3 on 2020-12-06 01:13

from django.db import migrations
import video_encoding.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20201206_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippetmodel',
            name='videoFile',
            field=video_encoding.fields.VideoField(blank=True, upload_to='users/snippets'),
        ),
    ]