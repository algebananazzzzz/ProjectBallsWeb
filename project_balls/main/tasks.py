import os
import glob
import uuid
from django.conf import settings
from django.core.files import File
from .models import BoardModel, SnippetModel
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.video.fx.all as vfx


def create_snippet(board, data):
    video_path = board.videoFile.path
    snippet_path = settings.MEDIA_ROOT + \
        '/users/snippets/' + data['name'] + '/'

    if not os.path.exists(snippet_path):
        os.makedirs(snippet_path)

    tag_list = data['tags']

    for i in tag_list:
        snippet_path += i
        snippet_path += '_'

    start_time = float(data['start_time'])
    end_time = float(data['end_time'])
    speed = float(data['speed'])

    new_snippet_path = snippet_path + uuid.uuid4().hex + '.mp4'

    with VideoFileClip(video_path) as video:
        new = video.subclip(start_time, end_time).fx(vfx.speedx, speed)
        new.write_videofile(new_snippet_path, audio_codec='aac')

        with open(new_snippet_path, 'rb') as file_handler:
            snippet = SnippetModel.objects.create(Board=board, videoFile=File(
                file_handler), Name=data['name'], Tags=tag_list, Speed=speed)

        os.remove(new_snippet_path)

        snippet.create_thumbnail()

    board_tags = board.primaryTags
    snippet_statistics = dict()

    for x in board_tags:
        snippet_count = SnippetModel.objects.filter(
            Board=board, Tags__contains=x.split()).count()
        if x in snippet_statistics:
            snippet_statistics[x] += snippet_count
        else:
            snippet_statistics[x] = snippet_count

    board.snippetStatistics = snippet_statistics
    board.save()


def generate_dash_video(path):

    command = 'MP4Box -dash 4000 -frag 4000 -rap -bs-switching no -profile live ' + \
        path + '#video ' + path + '#audio'

    os.chdir(settings.MEDIA_ROOT + '/users/videos')

    os.system(command)


def auto_update_onsave(instance):
    user = instance.User
    board_tags = instance.primaryTags
    all_tags = user.allTags
    all_tags.extend(x for x in board_tags if x not in all_tags)
    user.allTags = all_tags

    tag_statistics = dict()
    snippet_statistics = dict()
    boards = user.boards()

    for b in boards:
        board_tags = b.primaryTags
        for x in board_tags:
            if x in tag_statistics:
                tag_statistics[x] += 1
            else:
                tag_statistics[x] = 1
            snippet_count = SnippetModel.objects.filter(
                Board=b, Tags__contains=x.split()).count()
            if x in snippet_statistics:
                snippet_statistics[x] += snippet_count
            else:
                snippet_statistics[x] = snippet_count

    user.tagStatistics = tag_statistics
    user.snippetStatistics = snippet_statistics
    user.save()


def auto_delete_ondelete(instance):
    user = instance.User
    all_tags = list()
    for b in user.boards():
        all_tags.extend(x for x in b.primaryTags if x not in all_tags)
    user.allTags = all_tags
    user.save()

    if instance.videoFile:
        if os.path.isfile(instance.videoFile.path):
            os.remove(instance.videoFile.path)

    dash_path = instance.get_mpd_videofile_url()

    if dash_path:
        dash_path = os.path.splitext(instance.videoFile.path)[0]
        file_list = glob.glob(dash_path + '*', recursive=True)

        for f in file_list:
            os.remove(f)

    old_path = instance.thumbnail.path
    base_url = settings.MEDIA_ROOT + '/images/default-thumbnail.jpg'

    try:
        if old_path != base_url:
            os.unlink(old_path)
    except FileNotFoundError:
        pass

    board_tags = instance.primaryTags
    snippet_statistics = dict()

    for x in board_tags:
        snippet_count = SnippetModel.objects.filter(
            Board=instance, Tags__contains=x.split()).count()
        if x in snippet_statistics:
            snippet_statistics[x] += snippet_count
        else:
            snippet_statistics[x] = snippet_count

    instance.snippetStatistics = snippet_statistics
    instance.save()


def auto_delete_onchange(instance):
    user = instance.User
    all_tags = list()
    for b in user.boards():
        all_tags.extend(x for x in b.primaryTags if x not in all_tags)
    user.allTags = all_tags
    user.save()

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
    board = instance.Board
    board_tags = board.primaryTags
    snippet_tags = instance.Tags
    snippet_statistics = dict()

    for x in board_tags:
        snippet_count = SnippetModel.objects.filter(
            Board=board, Tags__contains=x.split()).count()
        if x in snippet_statistics:
            snippet_statistics[x] += snippet_count
        else:
            snippet_statistics[x] = snippet_count
        if x in snippet_tags:
            snippet_statistics[x] -= 1
    board.snippetStatistics = snippet_statistics
    board.save()


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
