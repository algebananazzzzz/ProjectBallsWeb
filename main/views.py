from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import signupForm, BoardModelForm, configureUserForm
from .models import User, BoardModel


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
                return redirect("/dashboard")
        else:
            form_message = "Invalid username or password."
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"form_message": form_message})


def logout(request):
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
            user = authenticate(username=username, password=raw_password)
            auth.login(request, user)

            return redirect('/dashboard')

        else:
            error_message = "Username already exists. Login instead?"

    return render(request=request, template_name="main/signup.html", context={'error_message': error_message})


def dashboard(request):
    board_list = request.user.boards()
    return render(request=request, template_name="main/dashboard.html", context={'board_list': board_list})


def board(request, boardPk):
    board = BoardModel.objects.get(pk=boardPk)
    return render(request=request, template_name="main/board.html", context={'board': board})


def board_config(request, boardPk=None):

    if request.method == "POST":
        if 'delete' in request.POST:
            instance = BoardModel.objects.get(pk=boardPk)
            instance.delete()
            return redirect('dashboard')
        else:
            print(request.POST)
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
    return redirect('board', boardPk)


def video(request, boardPk):
    board = BoardModel.objects.get(pk=boardPk)
    return render(request=request, template_name="main/video.html", context={'board': board})


def snippets(request, boardPk, snippetPk):
    return render(request=request, template_name="main/snippets.html", context={'boardPk': boardPk})


def configure(request):
    if request.method == "POST":
        form = configureUserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    form = configureUserForm(instance=request.user)

    return render(request=request, template_name="main/configure.html", context={'form': form})
# Create your views here.
