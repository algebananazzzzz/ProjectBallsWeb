import os
from django.conf import settings
from video_encoding.backends import get_backend
from .models import BoardModel


def auto_delete_ondelete(instance):

    for format in instance.format_set.complete().all():
        if os.path.isfile(format.file.path):
            os.remove(format.file.path)

    if instance.videoFile:
        if os.path.isfile(instance.videoFile.path):
            os.remove(instance.videoFile.path)

    old_path = instance.thumbnail.path
    base_url = settings.MEDIA_ROOT + '/images/default-thumbnail.jpg'

    try:
        if old_path != base_url:
            os.unlink(old_path)
    except FileNotFoundError:
        pass


def auto_delete_onchange(instance):
    if not instance.pk:
        return

    try:
        old_file = BoardModel.objects.get(pk=instance.pk).videoFile
    except BoardModel.DoesNotExist:
        return

    new_file = instance.videoFile

    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

        for format in instance.format_set.complete().all():
            if os.path.isfile(format.file.path):
                os.remove(format.file.path)
