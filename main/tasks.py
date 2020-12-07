import os
import uuid
from django.conf import settings
from pathlib import Path
from django.core.files import File
from video_encoding.backends import get_backend
from .models import BoardModel, SnippetModel
from moviepy.video.io.VideoFileClip import VideoFileClip


def create_snippet(board, data):
    video_path = board.videoFile.path
<<<<<<< HEAD
    snippet_path = settings.MEDIA_ROOT + '/users/snippets/'

    tag_list = data['tags'].strip('][').split(',')

    for i in tag_list:
        print(i)
        snippet_path += i
        snippet_path += '-'

    snippet_path += uuid.uuid4().hex + '.mp4'
=======
    snippet_path = settings.MEDIA_ROOT + '/users/snippets/' + uuid.uuid4().hex + \
        '.mp4'
>>>>>>> 453ccb05972faccbb9801652703c3c4b326096e6

    with VideoFileClip(video_path) as video:
        new = video.subclip(
            float(data['start_time']), float(data['end_time']))
        new.write_videofile(snippet_path, audio_codec='aac')

    with open(snippet_path, 'rb') as file_handler:
        snippet = SnippetModel.objects.create(
<<<<<<< HEAD
            Board=board, videoFile=File(file_handler), Name=data['name'], Tags=tag_list)
=======
            Board=board, videoFile=File(file_handler), Name=data['name'], Tags=data['tags'].strip('][').split(', '))
>>>>>>> 453ccb05972faccbb9801652703c3c4b326096e6

    os.remove(snippet_path)

    snippet.create_thumbnail()

<<<<<<< HEAD

def generate_dash_video(path):

    command = 'MP4Box -dash 10000 -frag 1000 -rap -single-segment {} '.format(
        path)

    os.chdir(settings.MEDIA_ROOT + '/users/videos')

    os.system(command)


=======

def generate_dash_video(path):

    command = 'MP4Box -dash 10000 -frag 1000 -rap -single-segment {} '.format(
        path)

    os.chdir(settings.MEDIA_ROOT + '/users/videos')
    os.system(command)


>>>>>>> 453ccb05972faccbb9801652703c3c4b326096e6
def auto_delete_ondelete(instance):
    if instance.videoFile:
        if os.path.isfile(instance.videoFile.path):
            os.remove(instance.videoFile.path)

    dash_path = instance.get_mpd_videofile_url()

    if dash_path:
<<<<<<< HEAD
        dash_path = os.path.splitext(instance.videoFile.path)[0]
=======
        dash_path = os.path.splitext(board.videoFile.path)[0]
>>>>>>> 453ccb05972faccbb9801652703c3c4b326096e6
        os.unlink(dash_path + '_dash.mpd')
        os.unlink(dash_path + '_dashinit.mp4')

    old_path = instance.thumbnail.path
    base_url = '/images/default-thumbnail.jpg'

    try:
        if old_path != base_url:
            os.unlink(old_path)
    except FileNotFoundError:
        pass


def auto_delete_onchange(instance):
    if not instance.pk:
        return

    try:
        board = BoardModel.objects.get(pk=instance.pk)
        old_file = board.videoFile
        dash_path = board.get_mpd_videofile_url()

    except BoardModel.DoesNotExist:
        return

    new_file = instance.videoFile

    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

        if dash_path:
            dash_path = os.path.splitext(board.videoFile.path)[0]
            os.unlink(dash_path + '_dash.mpd')
            os.unlink(dash_path + '_dashinit.mp4')

        for format in instance.format_set.complete().all():
            if os.path.isfile(format.file.path):
                os.remove(format.file.path)


def auto_delete_snippet_ondelete(instance):

    if instance.videoFile:
        if os.path.isfile(instance.videoFile.path):
            os.remove(instance.videoFile.path)

    old_path = instance.thumbnail.path
    base_url = settings.MEDIA_ROOT + '/images/ulti-skye-bg.jpg'

    try:
        if old_path != base_url:
            os.unlink(old_path)
    except FileNotFoundError:
        pass


def auto_delete_snippet_onchange(instance):
    if not instance.pk:
        return

    try:
        snippet = SnippetModel.objects.get(pk=instance.pk)
        old_file = snippet.videoFile

    except BoardModel.DoesNotExist:
        return

    new_file = instance.videoFile

    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

    old_thumbnail = snippet.thumbnail.path
    base_url = settings.MEDIA_ROOT + '/images/ulti-skye-bg.jpg'

    try:
        if old_thumbnail != base_url:
            os.unlink(old_thumbnail)
    except FileNotFoundError:
        pass
