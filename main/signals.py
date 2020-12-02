import os
import django_rq
from functools import wraps
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from video_encoding.tasks import convert_all_videos
from .models import BoardModel
from .tasks import auto_delete_onchange, auto_delete_ondelete


@receiver(post_save, sender=BoardModel)
def convert_video(sender, instance, **kwargs):

    queue = django_rq.get_queue('high')
    queue.enqueue(convert_all_videos,
                  instance._meta.app_label,
                  instance._meta.model_name,
                  instance.pk)


@receiver(pre_delete, sender=BoardModel)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `BoardModel` object is deleted.
    """
    auto_delete_ondelete(instance)


@receiver(pre_save, sender=BoardModel)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `BoardModel` object is updated
    with new file.
    """
    auto_delete_onchange(instance)
