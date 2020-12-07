import os
from django.db import models
from django.core.files import File
from pathlib import Path
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.auth.models import AbstractUser
from video_encoding.fields import VideoField
from video_encoding.backends import get_backend
from video_encoding.models import Format
from sorl.thumbnail import ImageField
from django.contrib.contenttypes.fields import GenericRelation


class User(AbstractUser):
    allTags = ArrayField(models.CharField(max_length=30), default=list)
    start_recording_key = models.IntegerField(default=83)
    end_recording_key = models.IntegerField(default=32)
    cancel_recording_key = models.IntegerField(default=67)

    def __str__(self):
        return self.username

    def boards(self):
        return BoardModel.objects.filter(User=self)

    def gen_all_tags(self):
        all_tags = list()

        for i in self.boards():
            all_tags = all_tags + list(set(i.primaryTags) - set(all_tags))

        self.allTags = all_tags
        self.save()


class BoardModel(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    Name = models.CharField(max_length=50)

    Description = models.CharField(max_length=500, null=True, blank=True)

    primaryTags = ArrayField(models.CharField(max_length=30), default=list)

    videoFile = VideoField(upload_to='users/videos')

    thumbnail = ImageField(upload_to='users/thumbnails',
                           default='images/default-thumbnail.jpg')

    format_set = GenericRelation(Format)

    def __str__(self):
        return self.Name

    def snippets(self):
        return SnippetModel.objects.filter(Board=self)

    def get_mpd_videofile_url(self):
        path = self.videoFile.path

        path = os.path.splitext(path)[0] + '_dash.mpd'

        if os.path.isfile(path):
            return os.path.splitext(self.videoFile.url)[0] + '_dash.mpd'
        else:
            return False

    def get_thumbnail_url(self):
        return self.thumbnail.url

    def create_thumbnail(self):

        if not self.videoFile:
            # no video file attached
            return

        new_video = self.videoFile

        encoding_backend = get_backend()

        duration = new_video.duration

        if duration < 1:
            at_time = 0.5
        elif duration < 5:
            at_time = 2.5
        elif duration < 10:
            at_time = 5
        elif duration < 30:
            at_time = 15
        else:
            at_time = 30

        thumbnail_path = encoding_backend.get_thumbnail(
            new_video.path, at_time=at_time)
        filename = Path(new_video.name).stem
        # + '.jpg'

        old_path = self.thumbnail.path
        base_url = settings.MEDIA_ROOT + '/images/default-thumbnail.jpg'

        try:
            if old_path != base_url:
                os.unlink(old_path)
        except FileNotFoundError:
            pass

        try:

            with open(thumbnail_path, 'rb') as file_handler:
                thumbnail_name = self.thumbnail.storage.get_alternative_name(
                    filename, '.jpg')
                self.thumbnail.save(thumbnail_name, File(file_handler))

        finally:
            os.unlink(thumbnail_path)


class SnippetModel(models.Model):
    Board = models.ForeignKey(BoardModel, on_delete=models.CASCADE)

    Name = models.CharField(max_length=50)

    Tags = ArrayField(models.CharField(max_length=30), default=list)

    videoFile = VideoField(upload_to='users/snippets', blank=True, null=True)

    thumbnail = ImageField(upload_to='users/thumbnails',
                           default='images/ulti-skye-bg.jpg')

    format_set = GenericRelation(Format)

    def __str__(self):
        return self.Name

    def get_thumbnail_url(self):
        return self.thumbnail.url

    def not_tag_blank(self):
        if self.Tags == list() or self.Tags == [""]:
            return False

        else:
            return True

    def create_thumbnail(self):

        if not self.videoFile:
            # no video file attached
            return

        new_video = self.videoFile

        encoding_backend = get_backend()

        thumbnail_path = encoding_backend.get_thumbnail(
            new_video.path)
        filename = Path(new_video.name).stem

        try:

            with open(thumbnail_path, 'rb') as file_handler:
                thumbnail_name = self.thumbnail.storage.get_alternative_name(
                    filename, '.jpg')
                self.thumbnail.save(thumbnail_name, File(file_handler))

        finally:
            os.unlink(thumbnail_path)

# Create your models here.
