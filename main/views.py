import json
import os
from django.conf import settings
import django_rq
import zipfile
import io
from pathlib import Path
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib import auth
from urllib.parse import unquote
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import signupForm, BoardModelForm, configureUserForm
from .models import User, BoardModel, SnippetModel
from .tasks import create_snippet


def download(request, snippetPk):
    object = SnippetModel.objects.get(pk=snippetPk)
    filename = object.videoFile.name.split('/')[-1]
    response = HttpResponse(object.videoFile, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


def download_board(request, boardPk):
    board = BoardModel.objects.get(pk=boardPk)
    filenames = list()

    for i in board.snippets():
        filenames.append(i.videoFile.path)

    zip_subdir = board.Name
    zip_filename = "%s.zip" % zip_subdir

    # Open BytesIO to grab in-memory ZIP contents
    s = io.BytesIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path, compress_type=zipfile.ZIP_DEFLATED)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(
        s.getvalue(), content_type="application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp


def home(request):
    return render(request=request, template_name="main/home.html")


def login(request):
    form_message = None
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username, password)
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                # messages.info(request, f"Hello, {username}")
                messages.add_message(
                    request, messages.INFO, 'Welcome back!! :)')

                return redirect("/dashboard")
        else:
            form_message = "Invalid username or password."
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"form_message": form_message})


def logout(request):
    messages.add_message(request, messages.WARNING, 'You have logged out :o')
    auth.logout(request)
    return redirect("/")


def signup(request):
    error_message = None
    if request.method == 'POST':

        form = signupForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            form.save()
            user = auth.authenticate(username=username, password=raw_password)
            auth.login(request, user)
            messages.add_message(
                request, messages.INFO, 'Welcome here!! :)')

            return redirect('/dashboard')

        else:
            error_message = "Username already exists. Login instead?"

    return render(request=request, template_name="main/signup.html", context={'error_message': error_message})


def dashboard(request):
    if request.method == "POST":
        query = request.POST['query'].strip('][').split(', ')
        snippets = SnippetModel.objects.filter(Tags__contains=query)
        messages.add_message(request, messages.SUCCESS,
                             'Query successful!! :)')

        return render(request=request, template_name="main/snippets.html", context={'snippets': snippets})

    board_list = request.user.boards()
    tag_autocomplete_data = request.user.allTags
    return render(request=request, template_name="main/dashboard.html", context={'board_list': board_list, 'tag_autocomplete_data': tag_autocomplete_data, 'board_count': board_list.count()})


def board(request, boardPk):
    board = BoardModel.objects.get(pk=boardPk)

    if request.method == "POST":
        query = request.POST['query'].strip('][').split(', ')
        snippets = SnippetModel.objects.filter(
            Board=board, Tags__contains=query)
        messages.add_message(request, messages.SUCCESS,
                             'Query successful!! :)')

        return render(request=request, template_name="main/snippets.html", context={'boardPk': boardPk, 'snippets': snippets})

    return render(request=request, template_name="main/board.html", context={'board': board, 'snippets': board.snippets()})


def board_config(request, boardPk=None):

    if request.method == "POST":
        if 'delete' in request.POST:
            instance = BoardModel.objects.get(pk=boardPk)
            instance.delete()
            return redirect('dashboard')
        else:
            if boardPk:
                instance = BoardModel.objects.get(pk=boardPk)
                form = BoardModelForm(
                    request.POST, request.FILES, instance=instance)
            else:
                form = BoardModelForm(request.POST, request.FILES)
                boardPk = False

            if form.is_valid():
                new_instance = form.save(commit=False)
                new_instance.User = request.user
                new_instance.save()
                boardPk = new_instance.pk

                messages.add_message(
                    request, messages.INFO, 'It may take a while to configure... (converting your file from mp4 to mpd for DASH streaming)')

                return redirect('board', boardPk)

    else:
        if boardPk:
            instance = BoardModel.objects.get(pk=boardPk)
            form = BoardModelForm(instance=instance)
        else:
            form = BoardModelForm(initial={'thumbnail': 'default'})
            boardPk = False

    return render(request=request, template_name="main/configure.html", context={'context': 'Board', 'boardPk': boardPk, 'form': form})


def generate_thumbnail(request, boardPk):
    BoardModel.objects.get(pk=boardPk).create_thumbnail()
    messages.add_message(request, messages.WARNING,
                         "I'm working really hard here, gimme a moment :o")

    return redirect('board', boardPk)


def delete_snippet(request, boardPk, snippetPk):
    SnippetModel.objects.get(pk=snippetPk).delete()
    return redirect('board', boardPk)


def video(request, boardPk):
    user = request.user
    board = BoardModel.objects.get(pk=boardPk)

    if request.method == "POST":
        data = json.loads(unquote(unquote(request.POST['data'])))

        for i in data:
            django_rq.enqueue(create_snippet, board, i)
            messages.add_message(request, messages.INFO,
                                 "Creating snippet of " + i['name'])

        messages.add_message(request, messages.WARNING,
                             "Hmmmm, this may take a moment so don't freak out!! (Encoding ur snippets at the backend!!)")

        return redirect('board', boardPk)

    video_path = board.get_mpd_videofile_url()

    return render(request=request, template_name="main/video.html", context={'board': board, 'video_path': video_path, 'start_recording_key': user.start_recording_key, 'end_recording_key': user.end_recording_key, 'cancel_recording_key': user.cancel_recording_key})


def snippet_video(request, boardPk, snippetPk):
    snippet = SnippetModel.objects.get(pk=snippetPk)

    for i in snippet.Tags:
        print(i)

    video_path = '/media/users/snippets/' + \
        Path(snippet.videoFile.name).stem + '.mp4'

    thumbnail_url = snippet.get_thumbnail_url()

    return render(request=request, template_name="main/snippet-video.html", context={'boardPk': boardPk, 'thumbnail_url': thumbnail_url, 'video_path': video_path})


def configure(request):
    if request.method == "POST":
        form = configureUserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    form = configureUserForm(instance=request.user)

    return render(request=request, template_name="main/configure.html", context={'form': form})
# Create your views here.
