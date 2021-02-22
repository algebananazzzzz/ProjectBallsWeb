import os
import django_rq
from functools import wraps
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .models import BoardModel, SnippetModel
from .tasks import auto_update_onsave, generate_dash_video, auto_delete_onchange, auto_delete_ondelete, auto_delete_snippet_onchange, auto_delete_snippet_ondelete


@receiver(post_save, sender=BoardModel)
def convert_video(sender, instance, **kwargs):

    queue = django_rq.get_queue('high')
    queue.enqueue(generate_dash_video,
                  os.path.basename(instance.videoFile.name))
    queue.enqueue(auto_update_onsave, instance)

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


@receiver(pre_delete, sender=SnippetModel)
def auto_delete_snippet_file_ondelete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `SnippetModel` object is deleted.
    """
    auto_delete_snippet_ondelete(instance)


@receiver(pre_save, sender=SnippetModel)
def auto_delete_snippet_file_onchange(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `SnippetModel` object is updated
    with new file.
    """
    auto_delete_snippet_onchange(instance)
